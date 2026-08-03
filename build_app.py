#!/usr/bin/env python3
"""
Build the standalone multi-step calculator (site/index.html).

The calculator's math is verified across 12,097,278+ profiles against an
independent evidence oracle. To keep that guarantee, this script does NOT
reimplement any of it: it lifts the engine <script> verbatim out of the built
guide and injects it into a new UI shell whose markup exposes every element id
the engine reads. The engine is byte-identical between the two artifacts.

Usage:
    python3 build_html.py     # builds the guide (source of the verified engine)
    python3 build_app.py      # builds site/index.html
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, "Healthiest-Diet-Guide.html")
TEMPLATE = os.path.join(HERE, "src", "app.template.html")
OUT = os.path.join(HERE, "index.html")  # repo root — GitHub Pages serves this


def engine_script(path):
    """Return the <script> body that defines the calculator engine."""
    html = open(path, encoding="utf-8").read()
    blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    cands = [b for b in blocks if "function calc(" in b]
    if not cands:
        sys.exit("ERROR: no engine <script> found in %s — run build_html.py first." % path)
    return max(cands, key=len)


def main():
    if not os.path.exists(GUIDE):
        sys.exit("ERROR: %s not found. Run `python3 build_html.py` first." % GUIDE)

    engine = engine_script(GUIDE)
    template = open(TEMPLATE, encoding="utf-8").read()

    if "<!--ENGINE-->" not in template:
        sys.exit("ERROR: template is missing the <!--ENGINE--> placeholder.")

    page = template.replace("<!--ENGINE-->", "<script>\n" + engine + "\n</script>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)

    # Prove the shipped engine is the verified one.
    # (the injected block gains a surrounding newline, so compare the payload)
    digest = hashlib.sha256(engine.strip().encode("utf-8")).hexdigest()
    shipped = engine_script(OUT).strip()
    ok = hashlib.sha256(shipped.encode("utf-8")).hexdigest() == digest

    print("wrote %s  (%d KB)" % (os.path.relpath(OUT, HERE), len(page) // 1024))
    print("engine sha256 : %s" % digest[:32])
    print("engine size   : %d bytes" % len(engine))
    print("identical to verified guide engine: %s" % ("YES" if ok else "NO"))
    if not ok:
        sys.exit("ERROR: engine mismatch after injection.")


if __name__ == "__main__":
    main()
