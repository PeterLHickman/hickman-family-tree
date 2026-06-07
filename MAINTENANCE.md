# Hickman Family Tree — Website Maintenance Guide

This is the authoritative reference for how **hickmansofbackcreek.org** is built and
maintained. It is written for **any maintainer — a family member, a web developer, or an
AI assistant** — picking up the project, possibly years from now, on a different computer,
with no prior context. Read it first. It lives inside the repository so it can never drift
away from the code it describes.

> New here and just want to make a small text fix? See **[`README.md`](README.md)** — you
> can edit directly in your web browser with no software installed. This file is for
> deeper changes.

**Guiding principle:** everything needed to maintain this site must live *inside this
repository*. Do not rely on notes stored on one person's computer, scripts in a temp
folder, or any one tool. If you discover something the next maintainer will need, add it
here and commit it.

---

## 1. What this is

A single-page interactive family history site for the Hickmans of Back Creek, Bath
County, Virginia. Visitors browse a family tree, click any person to open a detailed
profile ("modal") with biography, photos, and transcribed letters, and explore an
interactive map of family locations.

- **Live URL:** https://hickmansofbackcreek.org
- **GitHub repo:** `PeterLHickman/hickman-family-tree` (GitHub Pages)
- **Custom domain:** set by the `CNAME` file (`hickmansofbackcreek.org`)
- **Owner:** Peter Lightner Hickman II
- **Local working copy:** `C:\Users\hickm\hickman-family-tree\`

## 2. File layout

```
index.html        ← THE ENTIRE SITE: HTML + inline <style> CSS + inline <script> JS.
                     Almost all work happens here. ~9,000+ lines.
about.html        ← secondary "about" page
photos/           ← all images (356+ files). Naming conventions below.
audio/            ← narrated excerpts (.mp3) + excerpts.json index
hanna_art.png     ← one art image referenced from root (not in photos/)
CNAME             ← custom domain config — do not delete
favicon.ico, apple-touch-icon.png
MAINTENANCE.md    ← this file
```

There is no build step, framework, or dependencies. Edit `index.html`, commit, push —
GitHub Pages serves it directly. CSS and JS are inline (5 `<style>`/`<script>` blocks).

## 3. How the tree → modal system works

This is the core mechanism. Three pieces must stay in sync:

### a. Tree cards (what you see on the page)
Each person on the tree is a `.person` div containing a `.name` div:
```html
<div class="person male small-person deceased">
  <div class="photo"><img src="photos/foo.jpg" alt="..."></div>   <!-- or initials like "RH" -->
  <div class="name">Roger Hickman</div>
  <div class="dates">1813–1889</div>
  <div class="note">...</div>
</div>
```

### b. The modal (the popup profile)
Each profile is a `.modal-overlay` with a unique id:
```html
<div class="modal-overlay" id="modal-wrh">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-wrh')">&times;</button>
    <div class="modal-header"> photo + <h2>name</h2> + bio </div>
    ... bio sections, photo-gallery, correspondence ...
  </div>
</div>
```

### c. The wiring (JavaScript, near the bottom of index.html)
A script matches each tree card's `.name` **text** to a modal id via two lookup tables:
- **`exactMap`** (~line 8471): exact full-name → modal id. Used for most modals.
- **`cardMap`** (~line 8561): prefix match → modal id. Used for the original 10 core
  family modals (matches if the card name *starts with* the key).

**THE GOLDEN RULE:** the text inside `<div class="name">…</div>` must match an `exactMap`
key (or `cardMap` prefix) **exactly**, after HTML entities render. The JS reads
`nameEl.textContent.trim()`, so `&ldquo;Patsy&rdquo;` becomes `"Patsy"` (curly quotes).
When you add/rename a tree card, you almost always must add/update its `exactMap` entry.

### Common wiring mistakes (all have bitten us)
- **Renamed a card but forgot exactMap** → card no longer clickable. Fix: add the new
  exact text as an `exactMap` key. (Happened with "Patsy" after adding "Hickman".)
- **Two cards with identical `.name` text** → both open the same modal. Fix: disambiguate
  the card text and the key (e.g. `Arthur Hickman of Missouri` vs the ancestor
  `Arthur Hickman`; `William Hickman of Maryland` vs the Sunrise builder `William Hickman`).
- **Curly vs straight quotes:** card uses `&ldquo;…&rdquo;`; exactMap key must use the
  matching curly unicode `“…”` (renders identically) or the literal curly chars.

## 4. Modal anatomy

Two modal shapes exist:

1. **Simple modal:** header → one or more `.modal-bio-section` → optional `.photo-gallery`
   → optional `.modal-correspondence-section`. Galleries should come **after** the bio.
2. **Tabbed modal** (the 14 richest profiles — PLH, Ollie, Roger, Forrest, Virge, Clare,
   Ruth, Julian, Harry, Bill, Patti, Pete II, Gabe, Doc): content is split into
   `.tab-pane` divs (`data-pane="bio|photos|letters"`) with `.tab-btn` buttons. The
   `showTab()` JS swaps panes. `openModal()` resets to the first tab on open.

Gallery item template:
```html
<div class="gallery-item" onclick="showLightbox(this)">
  <img loading="lazy" src="photos/archive_foo.jpg" alt="Caption text">
  <div class="caption">Caption text</div>
</div>
```
Collapsible letter template uses `.correspondence-item` with a `toggleCorrespondence(this)`
header and a `.correspondence-body`.

## 5. Photo conventions

- **Folder:** all images go in `photos/`. Reference as `src="photos/NAME.ext"`.
- **Naming:**
  - Core portraits: `roger_portrait.jpg`, `ollie_young.jpg`, etc.
  - Archive scans: prefix `archive_` + descriptive slug, e.g.
    `archive_bishop_taylor_horseback.png`, `archive_ollie_portrait_a.jpg`.
- **Source of truth for archival images:** the Dropbox photo archive at
  `D:\Dropbox\Family Room\13 - Hickman Family History\2 - Photos\` (person-named
  subfolders). Copy from there into `photos/` when adding to a modal.
- **Lightroom tags:** Peter tags photos in Lightroom Classic; those keywords are embedded
  in the JPEGs as XMP and are machine-readable (see the helper scripts that were in
  `C:\tmp\`: extract_tags.py, map_tags_to_modals.py, build_contact_sheets.py,
  insert_picks.py). Read tags to identify people before asking. Junk-filter values
  matching `^[-0-9.,\s]+$` (stray develop settings leak into XMP).

## 6. PRIVACY — minors stay off the public site

**Do not** put photos or identifying detail of minor children on the public website
(or public GEDCOMs / published volumes): **Hanna**, **Ollie (b.~2011)**, **Devin**, and
any other minors. Adults (incl. Peter, his dad, Evelyn, Brendan, Ian if adult) are fine.
When bulk-adding tagged photos, exclude these names and also exclude social-media
downloads (`NNNNNNNN_..._n.jpg`) and recent phone files (`IMG_*.JPG`), which often show
living kids.

## 7. The workflow for ANY change

1. Edit `index.html` (and copy any new images into `photos/`).
2. **Verify div balance** (the #1 structural check — an unbalanced tree breaks layout):
   ```bash
   python -c "import re; h=open('index.html',encoding='utf-8').read(); \
   o=len(re.findall(r'<div[\s>]',h)); c=h.count('</div>'); print('Balanced:',o==c,o,c)"
   ```
   Opens must equal closes. If not, you left a div unclosed — fix before committing.
3. **Escape quotes in `alt=\"\"`:** nicknames with straight quotes break the attribute.
   Use curly quotes inside alt text, e.g. `alt="Warren “Doc” Campbell"`. After bulk
   edits, check: `grep -nE 'alt="[^"]*"[A-Za-z]' index.html` should return nothing.
4. **Commit & push** (see §8). GitHub Pages redeploys in ~1 minute.
5. **Update the "What's New" section** for any substantive, visitor-noticeable change
   (new profiles, galleries, tree restructuring, layout). It's near line ~1636 — add a
   card (Month YYYY + headline + 1–2 sentences) at the front; let old cards roll off past
   ~6. Skip this for trivial fixes (typos, single link).
6. **Refresh the Dropbox backup** after major work (see §9).

## 8. Git — and a deletion gotcha

Standard: `git add -A` then commit then push to `main`.

**WARNING — `git add -A` can stage stray deletions.** If a file went missing from
`photos/` for any reason, `git add -A` will commit its deletion. This already deleted a
still-referenced photo once (`seventh_heaven_family_2022.jpg`). **After staging, always:**
```bash
git status --short        # look for unexpected "D " (deleted) lines
```
And before/after big changes, run the integrity check that every referenced photo exists:
```bash
python -c "import re,os; h=open('index.html',encoding='utf-8').read(); \
refs=set(re.findall(r'src=\"photos/([^\"]+)\"',h)); ex=set(os.listdir('photos')); \
print('MISSING:',sorted(refs-ex))"
```
Restore an erroneously deleted file from history: `git checkout <commit> -- photos/<file>`.

## 9. Dropbox backup

GitHub is the primary copy, but a snapshot lives in Dropbox in case of host issues:
`D:\Dropbox\Family Room\13 - Hickman Family History\3 - Family Histories\14 - Website\`
(contains `index.html` + a copy of `photos/`). Refresh by copying the current
`index.html` and new photos there after major updates. **Do not** put the live git repo
inside Dropbox — git + Dropbox sync conflict.

## 10. Succession & access (the non-code lifelines)

The code is safe in GitHub + Dropbox. But the **public** site also depends on two things
that live outside the repository. Keep these recorded somewhere the family can find them
(a password manager, a sealed document with the estate, etc.) — this is the project's
"bus factor."

1. **GitHub account** — the repo is owned by `PeterLHickman`. To continue maintaining the
   *live* site, a successor needs either (a) login access to that account, (b) to be added
   as a collaborator on the repo, or (c) a fork/transfer of the repo to their own account
   (the site can be re-pointed to publish from there). The full history clones with the
   repo, so the content itself is never locked to one account.
2. **Domain name** — `hickmansofbackcreek.org` is registered with a domain registrar and
   renews (typically yearly, paid). If it lapses, the friendly address stops resolving,
   but the site stays online at the GitHub Pages URL
   (`https://peterlhickman.github.io/hickman-family-tree/`) and the domain can be
   re-pointed via the `CNAME` file once re-registered.

> **TODO for the owner — fill in and store securely (not in this public repo):**
> registrar name + login, domain renewal date, GitHub account recovery info, and the
> names of anyone else who should have access. Without these, a handoff after the owner is
> unavailable becomes much harder.

If GitHub Pages or the custom domain ever fails entirely, the site is still fully
recoverable from: (a) any git clone of this repo, or (b) the Dropbox snapshot in
`14 - Website/`. It can be re-hosted on any static host (GitHub Pages, Netlify, Cloudflare
Pages, plain web hosting) by uploading these files — no server required.

## 11. Quick facts (update these as they change)

- ~67 modal profiles; the homepage "interactive profiles" count text is near a
  `Built NN interactive profiles` line — bump it when you add profiles.
- Tree spans William Hickman of Somerset Co., MD (d. 1765) through Generation 9.
- Direct line: Arthur → Roger Sr. → William (built "Sunrise") → Roger (1813–1889) →
  Peter Lightner Hickman → the seven siblings (Roger, Forrest, Virge, Clare, Ruth,
  Julian, Harry) → … → Peter L. Hickman II (the owner).
- Audio narration files are indexed in `audio/excerpts.json`.

---
*Keep this file current. When you discover a new gotcha or convention, add it here so the
next session doesn't rediscover it the hard way.*
