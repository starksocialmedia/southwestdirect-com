#!/usr/bin/env python3
"""
Minify assets/css/site.css to assets/css/site.min.css.

Usage:  python3 tools/build-css.py

Deliberately conservative — no new dependencies, and it only does things that
cannot change computed styles: strip comments, collapse runs of whitespace,
drop space around structural punctuation, and remove the final semicolon in a
block. Strings and url() values are protected first so quoted content and data
URIs survive untouched.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "css", "site.css")
DEST = os.path.join(ROOT, "assets", "css", "site.min.css")


def minify(css):
    # 1. park strings and url() so nothing inside them is touched
    vault = []
    def park(m):
        vault.append(m.group(0))
        return f"\x00{len(vault) - 1}\x00"
    css = re.sub(r'"[^"\n]*"|\'[^\'\n]*\'|url\([^)]*\)', park, css)

    # 2. comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)

    # 3. whitespace
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,>~+])\s*', r'\1', css)
    css = re.sub(r';}', '}', css)

    # 4. a space is meaningful in descendant selectors and between values,
    #    but never right after an opening brace or before a closing one
    css = re.sub(r'{\s+', '{', css)
    css = re.sub(r'\s+}', '}', css)

    # 5. restore
    def unpark(m):
        return vault[int(m.group(1))]
    css = re.sub(r'\x00(\d+)\x00', unpark, css)
    return css.strip()


def main():
    src = open(SRC, encoding="utf-8").read()
    out = minify(src)
    open(DEST, "w", encoding="utf-8").write(out + "\n")
    a, b = len(src.encode()), len(out.encode())
    print(f"  {SRC.split('/')[-1]}: {a:,} bytes -> {b:,} bytes  ({100 - b * 100 // a}% smaller)")
    # sanity: braces must still balance and no rule may have been swallowed
    assert out.count("{") == out.count("}"), "brace mismatch after minify"
    assert out.count("@media") == src.count("@media"), "media query lost"
    assert out.count("@font-face") == src.count("@font-face"), "font-face lost"
    print(f"  braces balanced, {out.count('@media')} media queries and "
          f"{out.count('@font-face')} font-faces preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
