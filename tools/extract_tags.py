"""Extract Lightroom XMP keywords from every photo in the archive."""
import os, re
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

root = r"D:\Dropbox\Family Room\13 - Hickman Family History\2 - Photos"
IMG_EXT = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}

def get_keywords(path):
    try:
        img = Image.open(path)
    except Exception:
        return None
    xmp = img.info.get('xmp')
    if not xmp:
        return []
    x = xmp.decode('utf-8', 'ignore') if isinstance(xmp, bytes) else str(xmp)
    # Extract dc:subject bag specifically (flat keywords)
    subj = re.search(r'<dc:subject>(.*?)</dc:subject>', x, re.DOTALL)
    region = subj.group(1) if subj else x
    kws = re.findall(r'<rdf:li[^>]*>([^<]+)</rdf:li>', region)
    # dedupe preserving order
    seen = set(); out = []
    for k in kws:
        k = k.strip()
        if k and k not in seen:
            seen.add(k); out.append(k)
    return out

results = []  # (folder, filename, keywords)
tagged = 0
untagged = 0
for dirpath, dirs, files in os.walk(root):
    if '_originals_archive' in dirpath or '_pdf_originals' in dirpath:
        continue
    for f in sorted(files):
        ext = os.path.splitext(f)[1].lower()
        if ext not in IMG_EXT:
            continue
        full = os.path.join(dirpath, f)
        kws = get_keywords(full)
        if kws is None:
            continue
        rel = os.path.relpath(full, root)
        results.append((rel, kws))
        if kws:
            tagged += 1
        else:
            untagged += 1

# Write report
out = r"C:\tmp\lightroom_tags.txt"
with open(out, 'w', encoding='utf-8') as o:
    o.write("=== LIGHTROOM KEYWORD EXTRACTION ===\n\n")
    o.write(f"Total images scanned: {len(results)}\n")
    o.write(f"Tagged: {tagged}\n")
    o.write(f"Untagged: {untagged}\n\n")
    o.write("=" * 75 + "\n")
    o.write("TAGGED PHOTOS\n")
    o.write("=" * 75 + "\n")
    for rel, kws in results:
        if kws:
            o.write(f"\n{rel}\n")
            o.write(f"    {' | '.join(kws)}\n")

# Also build a keyword frequency table
from collections import Counter
freq = Counter()
for rel, kws in results:
    for k in kws:
        freq[k] += 1
with open(r"C:\tmp\lightroom_keyword_freq.txt", 'w', encoding='utf-8') as o:
    o.write("=== KEYWORD FREQUENCY ===\n\n")
    for k, c in freq.most_common():
        o.write(f"{c:>4}  {k}\n")

print(f"Scanned: {len(results)}, tagged: {tagged}, untagged: {untagged}")
print(f"Unique keywords: {len(freq)}")
print(f"Reports: {out}")
print(f"         C:\\tmp\\lightroom_keyword_freq.txt")
