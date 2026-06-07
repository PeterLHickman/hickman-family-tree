# tools/

Optional helper scripts for maintaining the site. **None of these are required** to make
edits — they just save time and catch mistakes. All are plain Python 3.

| Script | What it does | Needs |
|--------|--------------|-------|
| `check_integrity.py` | **Run before every commit.** Checks `<div>` balance, that every referenced photo exists, and that no `alt=""` has broken quotes. | Python 3 only |
| `extract_tags.py` | Reads Lightroom keyword tags embedded in the archive JPEGs and lists who's in each photo. | `pip install pillow` |
| `find_dupes.py` | Scans `photos/` (and the Dropbox archive) for exact and near-duplicate images. | `pip install pillow imagehash` |

## Usage

From the repo root:
```bash
python tools/check_integrity.py     # the important one — run before committing
python tools/extract_tags.py        # writes a tag report to a temp file
python tools/find_dupes.py          # writes a duplicate report
```

`extract_tags.py` and `find_dupes.py` have hard-coded paths to Peter's Dropbox photo
archive near the top of each file — edit those paths if the archive moves or you're on a
different machine.

## Background: Lightroom tags

Peter labels family photos in Lightroom Classic. Those keywords get written into the JPEG
files themselves (as embedded XMP metadata), so `extract_tags.py` can read who's in a
photo without needing the Lightroom catalog. This is how ~60 correctly-identified photos
were added to the site in June 2026. See `../MAINTENANCE.md` §5.
