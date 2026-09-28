#!/usr/bin/env python3
"""Save Lemon manual figures fetched with the MCP get_image tool to disk.

get_image returns the picture to Claude as an image block; it does not write a
file. Claude Code keeps every tool result in the session transcript
(~/.claude/projects/<project>/<session-id>.jsonl) as base64, next to the
tool call that asked for it. This script pairs each get_image call with its
result and writes the image out, so no second download is needed.

Usage, from the repo root, after calling get_image in this session:

  python3 tools/save-figures.py <guide-name> [ID=name ...]

  ID    the last segment of the image path, e.g. 364989686 for
        /images/IMP68Q313/euro650/364989686/
  name  file name without extension; the extension comes from the image type

With no ID=name pairs, every get_image result in the session is saved under
its ID. Files go to guides/img/<guide-name>/. Pass --transcript FILE to read a
specific transcript instead of finding the current one.
"""
import base64
import glob
import json
import os
import re
import sys

EXT = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif", "image/webp": "webp"}


def find_transcript():
    root = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if sid:
        hits = glob.glob(os.path.join(root, "*", sid + ".jsonl"))
        if hits:
            return hits[0]
    # Fall back to the newest transcript for this checkout.
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    slug = re.sub(r"[^A-Za-z0-9]", "-", repo)
    hits = glob.glob(os.path.join(root, slug, "*.jsonl")) or glob.glob(os.path.join(root, "*", "*.jsonl"))
    if not hits:
        sys.exit("No session transcript found; pass --transcript FILE.")
    return max(hits, key=os.path.getmtime)


def image_id(path):
    return path.strip("/").split("/")[-1]


def collect(transcript):
    calls, images = {}, {}
    with open(transcript) as f:
        for line in f:
            try:
                msg = json.loads(line).get("message")
            except ValueError:
                continue
            if not isinstance(msg, dict) or not isinstance(msg.get("content"), list):
                continue
            for block in msg["content"]:
                if block.get("type") == "tool_use" and block.get("name", "").endswith("get_image"):
                    calls[block["id"]] = image_id(block.get("input", {}).get("image_path", ""))
                elif block.get("type") == "tool_result" and isinstance(block.get("content"), list):
                    for part in block["content"]:
                        if part.get("type") == "image":
                            images[block["tool_use_id"]] = part["source"]
    # Later fetches of the same ID win.
    out = {}
    for tid, iid in calls.items():
        if tid in images:
            out[iid] = images[tid]
    return out


def main(argv):
    transcript = None
    if "--transcript" in argv:
        i = argv.index("--transcript")
        transcript = argv[i + 1]
        del argv[i:i + 2]
    if not argv or "=" in argv[0]:
        sys.exit(__doc__)
    guide, pairs = argv[0], argv[1:]
    wanted = dict(p.split("=", 1) for p in pairs)

    found = collect(transcript or find_transcript())
    targets = wanted or {iid: iid for iid in found}
    outdir = os.path.join("guides", "img", guide)
    os.makedirs(outdir, exist_ok=True)

    missing = []
    for iid, name in targets.items():
        src = found.get(iid)
        if not src:
            missing.append(iid)
            continue
        path = os.path.join(outdir, "%s.%s" % (name, EXT.get(src.get("media_type"), "bin")))
        with open(path, "wb") as f:
            f.write(base64.b64decode(src["data"]))
        print(path)
    if missing:
        sys.exit("Not in this session's get_image results: " + ", ".join(missing))


if __name__ == "__main__":
    main(sys.argv[1:])
