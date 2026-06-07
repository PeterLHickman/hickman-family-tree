#!/usr/bin/env python3
"""
check_integrity.py — run this before every commit to index.html.

Two safety checks that catch the most common ways the site breaks:
  1. <div> balance — every <div> must have a matching </div>, or the
     page layout collapses.
  2. Missing photos — every src="photos/..." referenced in index.html
     must exist as a real file in photos/.

Usage (from the repo root):
    python tools/check_integrity.py

Exit code 0 = all good, 1 = problems found.
Requires only Python 3 (no external packages).
"""
import re, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_path = os.path.join(HERE, "index.html")
photos_dir = os.path.join(HERE, "photos")

html = open(html_path, encoding="utf-8").read()
problems = 0

# 1. div balance
opens = len(re.findall(r"<div[\s>]", html))
closes = html.count("</div>")
if opens == closes:
    print(f"[OK]  div balance: {opens} open / {closes} close")
else:
    problems += 1
    print(f"[!!]  div balance MISMATCH: {opens} open / {closes} close "
          f"(difference {opens - closes}) — you left a div unclosed/extra")

# 2. referenced photos exist
existing = set(os.listdir(photos_dir)) if os.path.isdir(photos_dir) else set()
refs = set(re.findall(r'src="photos/([^"]+)"', html))
missing = sorted(r for r in refs if r not in existing)
if not missing:
    print(f"[OK]  photos: all {len(refs)} referenced images exist")
else:
    problems += 1
    print(f"[!!]  {len(missing)} referenced photo(s) MISSING from photos/:")
    for m in missing:
        print(f"        photos/{m}")

# 3. broken alt attributes (unescaped quotes inside alt="...")
bad_alt = re.findall(r'alt="[^"]*"[A-Za-z][^"]*"', html)
if not bad_alt:
    print("[OK]  alt attributes: no unescaped quotes")
else:
    problems += 1
    print(f"[!!]  {len(bad_alt)} alt attribute(s) have unescaped quotes "
          f"(use curly quotes inside alt text):")
    for b in bad_alt[:10]:
        print(f"        {b[:80]}")

print()
if problems:
    print(f"FAILED — {problems} problem group(s). Fix before committing.")
    sys.exit(1)
print("PASSED — safe to commit.")
sys.exit(0)
