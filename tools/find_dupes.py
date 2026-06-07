import os, hashlib
from collections import defaultdict

root = r"D:\Dropbox\Family Room\13 - Hickman Family History\2 - Photos"

def md5_of(path, chunk=65536):
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                buf = f.read(chunk)
                if not buf:
                    break
                h.update(buf)
        return h.hexdigest()
    except Exception:
        return None

# Walk all files
all_files = []
for dirpath, dirs, files in os.walk(root):
    # Skip _originals_archive (those are kept intentionally)
    if '_originals_archive' in dirpath:
        continue
    for f in files:
        if f.startswith('.') or f in ('PHOTO_INVENTORY.txt', 'PHOTO_TAGS.csv', '_BATCH_RENAME_PLAN.txt'):
            continue
        full = os.path.join(dirpath, f)
        try:
            size = os.path.getsize(full)
        except Exception:
            continue
        all_files.append((full, f, size))

print(f"Scanning {len(all_files)} files...")

# Group by size first (cheap pre-filter)
by_size = defaultdict(list)
for full, name, size in all_files:
    by_size[size].append((full, name))

# Compute MD5 only for files that share a size
exact_dupes = defaultdict(list)
for size, items in by_size.items():
    if len(items) < 2:
        continue
    for full, name in items:
        h = md5_of(full)
        if h:
            exact_dupes[h].append((full, name, size))

# Filter to only md5 collisions
exact_dupes = {h: v for h, v in exact_dupes.items() if len(v) >= 2}

# Find near-duplicates: same base name (stripped of _v2/_v3 suffix and EPS/PICT/PNG noise)
import re
def normalize_name(name):
    n = name.lower()
    # Strip _v2, _v3, etc.
    n = re.sub(r'_v\d+(\.|$)', r'\1', n)
    # Strip extension
    n = os.path.splitext(n)[0]
    # Strip common noise
    n = re.sub(r'_(eps|pict|png|jpg|tiff|tif|jpeg|pdf)$', '', n)
    n = re.sub(r'(eps|pict|tiff)_', '', n)
    n = re.sub(r'_+', '_', n)
    n = n.strip('_ ')
    return n

by_norm = defaultdict(list)
for full, name, size in all_files:
    by_norm[normalize_name(name)].append((full, name, size))
near_dupes = {k: v for k, v in by_norm.items() if len(v) >= 2}

# Filter near_dupes to remove exact-duplicate sets (already covered)
exact_full_paths = set()
for items in exact_dupes.values():
    for full, _, _ in items:
        exact_full_paths.add(full)

filtered_near = {}
for k, items in near_dupes.items():
    # If all items in this group are part of one exact-dupe set, skip
    non_exact = [it for it in items if it[0] not in exact_full_paths]
    if len(items) - len(non_exact) >= len(items) - 1:
        # All but possibly one are exact dupes - check if remaining group is interesting
        if len(non_exact) >= 1 and len([it for it in items if it[0] in exact_full_paths]) >= 1:
            # still has near-dupe variation
            filtered_near[k] = items
    else:
        filtered_near[k] = items

out = r"C:\tmp\duplicates_report.txt"
with open(out, 'w', encoding='utf-8') as o:
    o.write("=== PHOTOS DUPLICATE SCAN ===\n\n")
    o.write(f"Files scanned: {len(all_files)}\n")
    o.write(f"Exact MD5 duplicate sets: {len(exact_dupes)}\n")
    o.write(f"Near-duplicate sets (same normalized name): {len(filtered_near)}\n\n")

    o.write("=" * 70 + "\n")
    o.write("EXACT DUPLICATES (identical bytes)\n")
    o.write("=" * 70 + "\n\n")
    total_exact_files = 0
    total_exact_bytes = 0
    for h, items in sorted(exact_dupes.items(), key=lambda kv: -len(kv[1])):
        total_exact_files += len(items) - 1
        total_exact_bytes += items[0][2] * (len(items) - 1)
        o.write(f"--- {len(items)} copies ({items[0][2]} bytes each, md5 {h[:12]}...) ---\n")
        for full, name, size in items:
            rel = os.path.relpath(full, root)
            o.write(f"  {rel}\n")
        o.write("\n")
    o.write(f"\nReclaimable from exact dupes: {total_exact_files} files, ~{total_exact_bytes/1024/1024:.1f} MB\n\n")

    o.write("=" * 70 + "\n")
    o.write("NEAR-DUPLICATES (same normalized name, different bytes)\n")
    o.write("=" * 70 + "\n\n")
    for norm, items in sorted(filtered_near.items()):
        o.write(f"--- normalized: '{norm}' ({len(items)} variants) ---\n")
        for full, name, size in sorted(items, key=lambda x: x[2]):
            rel = os.path.relpath(full, root)
            o.write(f"  {size:>9} bytes  {rel}\n")
        o.write("\n")

print(f"Exact dupe sets: {len(exact_dupes)} ({total_exact_files} reclaimable)")
print(f"Near-dupe sets: {len(filtered_near)}")
print(f"Report: {out}")
