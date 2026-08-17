#!/usr/bin/env python3
"""Manifest and report helpers for the split-and-upload-vdb7 action.

These used to be inline ``python -c "..."`` snippets in action.yml. A YAML
block scalar strips only the indentation common to the whole ``run:`` body,
so a snippet written inside a shell ``for`` loop or function keeps its
*relative* indentation and reaches Python indented — every one of those
died with ``IndentationError: unexpected indent`` before its first
statement. Run 31997633626 shows it: GHCR login succeeded, then the first
per-shard build_id check inside the publish loop took the whole step down,
two and a half hours into the build. (The snippets that sat at the body's
base indentation did run, which is why this went unnoticed.) Values were
also interpolated straight into Python source (``'$BUILD_ID'``), so a shard
name or tag containing a quote would have produced a syntax error rather
than a comparison.

Arguments arrive through argv here, so indentation and quoting stop
mattering, and the file behaves identically in CI and locally.
"""

import argparse
import json
import sys


def _load(path):
    with open(path) as f:
        return json.load(f)


def _write(path, meta):
    with open(path, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)


def check_build_id(args):
    """Every artifact of one build must carry the same build_id (doc 08 §5/§7.1)."""
    meta = _load(args.meta)
    actual = meta.get("build_id")
    if actual != args.build_id:
        print(
            f"ERROR: {args.label} build_id {actual!r} != {args.build_id!r}",
            file=sys.stderr,
        )
        return 1
    print(f"build_id OK ({args.label}): {actual}")
    return 0


def publishable(args):
    """Print one publishable shard per line, and a SKIP line per excluded shard.

    A shard publishes only if it is non-empty and its own gate verdict is
    clean; the caller greps out the ``SKIP `` lines.
    """
    split_report = _load(args.split_report)
    gate_report = _load(args.gate_report)
    empty = {s["shard"] for s in split_report["shards"] if s.get("empty")}
    for name, verdict in sorted(gate_report["shards"].items()):
        if name in empty:
            print(f"SKIP {name}: empty shard (no rows for its types)")
        elif verdict.get("clean"):
            print(name)
        else:
            print(
                f"SKIP {name}: FAILED gate "
                f"(corpus={verdict['corpus']['status']}, "
                f"prefix_probes={verdict['prefix_probes'].get('status')}, "
                f"unsafe_raises={verdict['unsafe_entry_points']['clean']}, "
                f"absent_type={verdict['absent_type'].get('status')})"
            )
    return 0


def stamp(args):
    """Stamp the compression and sibling index onto a vdb.meta before an oras push.

    ``--siblings`` is written verbatim, so passing none clears the list —
    which is what the pre-finalization pushes want: siblings are only
    advertised once every artifact they name has actually pushed
    (doc 08 §7.4).
    """
    meta = _load(args.meta)
    meta["compression"] = args.compression
    meta.setdefault("siblings", {})["available"] = list(args.siblings)
    _write(args.meta, meta)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check-build-id")
    p.add_argument("meta")
    p.add_argument("build_id")
    p.add_argument("--label", default="artifact")
    p.set_defaults(func=check_build_id)

    p = sub.add_parser("publishable")
    p.add_argument("split_report")
    p.add_argument("gate_report")
    p.set_defaults(func=publishable)

    p = sub.add_parser("stamp")
    p.add_argument("meta")
    p.add_argument("--compression", required=True, choices=("xz", "zst"))
    p.add_argument("--siblings", nargs="*", default=[])
    p.set_defaults(func=stamp)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
