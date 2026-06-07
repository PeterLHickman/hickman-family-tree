# Hickmans of Back Creek — Family History Website

Live site: **https://hickmansofbackcreek.org**

This is the complete source for a family history website about the Hickman family of Back
Creek, Bath County, Virginia — interactive family tree, individual profiles with
biographies, photographs, and transcribed letters, and a map of family locations. It was
built and is maintained by **Peter Lightner Hickman II**.

This README is for **anyone who wants to continue the project** — a family member, a web
developer, or an AI assistant. You do **not** need to be a programmer to make simple
edits, and you do **not** need any special software.

---

## The most important thing to understand

**Everything the website needs is in this one GitHub repository.** The whole site is a
single file, `index.html`. There is no database, no server code, no build step. When you
change `index.html` and save it back to GitHub, the live website updates automatically
within about a minute (it's hosted free by *GitHub Pages*).

That means: as long as someone has access to this GitHub repository, the site can be
maintained forever, from any computer, with no special setup.

## How to make a simple edit — using only a web browser

You can fix a typo or change text without installing anything:

1. Go to the repository on GitHub and click **`index.html`**.
2. Click the **pencil icon** (✏️ "Edit this file") near the top right.
3. Use **Ctrl+F** (Cmd+F on Mac) to find the text you want to change.
4. Make your change.
5. Scroll down, click **Commit changes**, and confirm.
6. Wait ~1 minute, then refresh https://hickmansofbackcreek.org to see it live.

That's it. GitHub keeps a full history, so nothing can be permanently lost — any change
can be undone.

## For bigger changes (new people, photos, page layout)

Read **[`MAINTENANCE.md`](MAINTENANCE.md)** — the detailed maintainer's guide. It explains
how the family tree connects to the pop-up profiles, how to add photos, the safety checks
to run, and the mistakes to avoid. It's written so that a careful person (or an AI
assistant) can pick up the work correctly.

If you use an AI assistant (like Claude), just tell it: *"Read MAINTENANCE.md, then help
me ..."* and it will come up to speed.

Optional time-saving scripts live in **[`tools/`](tools/)** (see `tools/README.md`). They
are not required.

## What keeps the site alive (the non-code parts)

The website files are safe in GitHub and backed up to Dropbox. But two things outside the
code must be kept up for the public site to stay online:

1. **The GitHub account** that owns this repository (`PeterLHickman`). Whoever continues
   the project needs access to it, or a copy of the repository under their own account.
2. **The domain name** `hickmansofbackcreek.org`, which is registered with a domain
   registrar and must be renewed (usually paid yearly). If it lapses, the custom address
   stops working — though the site would still be reachable at the GitHub Pages address.

> **Owner action:** record where the domain is registered, the renewal date, and who
> else has GitHub access, so the project can survive a handoff. See the "Succession"
> section of `MAINTENANCE.md`.

## Repository contents

| Path | What it is |
|------|------------|
| `index.html` | The entire website (text, styling, and interactivity, all in one file). |
| `about.html` | Secondary "about" page. |
| `photos/` | All images used on the site. |
| `audio/` | Narrated audio excerpts. |
| `CNAME` | Connects the custom domain — do not delete. |
| `MAINTENANCE.md` | Detailed guide for maintainers. |
| `tools/` | Optional Python helper scripts. |

---

*A family record, kept for the generations that come after.*
