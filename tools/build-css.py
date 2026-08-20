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
    # calc() must be parked too: CSS requires whitespace around + and - inside
    # it, so collapsing that whitespace silently produces an invalid value.
    css = re.sub(r'"[^"\n]*"|\'[^\'\n]*\'|url\([^)]*\)'
                 r'|calc\((?:[^()]|\([^()]*\))*\)', park, css)

    # 2. comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)

    # 3. whitespace
    css = re.sub(r'\s+', ' ', css)
    # '+' is deliberately absent: it appears in calc() and in nth-child()
    # expressions where the surrounding whitespace is load-bearing.
    css = re.sub(r'\s*([{}:;,>~])\s*', r'\1', css)
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
    # Regression guard: this minifier once stripped the spaces inside calc(),
    # which silently moved the back-to-top button thousands of pixels off screen.
    src_calc = re.findall(r'calc\((?:[^()]|\([^()]*\))*\)', src)
    out_calc = re.findall(r'calc\((?:[^()]|\([^()]*\))*\)', out)
    assert len(src_calc) == len(out_calc), "calc() expression lost"
    for c in out_calc:
        # '+' is always arithmetic inside calc(), so it must be surrounded by
        # space. '-' can also be part of an identifier (safe-area-inset-right),
        # so only flag it where it directly follows a number or a closing paren.
        assert not re.search(r'\S\+|\+\S', c), f"calc() lost spacing around '+': {c}"
        assert not re.search(r'[\d)](?:px|%|ch|em|rem|vh|vw|dvh)?-', c), \
            f"calc() lost spacing around '-': {c}"
    print(f"  braces balanced, {out.count('@media')} media queries, "
          f"{out.count('@font-face')} font-faces and {len(out_calc)} calc() preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
