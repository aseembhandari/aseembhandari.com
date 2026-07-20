# Article workflow

This folder is the source of truth for everything you publish — so a `netlify deploy`
(which just re-uploads the site folder as-is) never loses anything. It also has
nothing to do with comments: those live in GitHub Discussions via giscus, entirely
outside this folder, for the same reason.

## How to publish something new

1. Drop your raw notes / draft / voice-memo transcript into a new file here:
   `content/YYYY-MM-DD-slug.md` (copy `_template.md` to start). Doesn't need to be
   polished — bullet points are fine.
2. Ask Claude (in this project) to "publish this as an article" and point it at the
   file. It will:
   - Write the full site post as `blog-<slug>.html`, matching the existing template,
     voice, and brand (Fraunces/Plex, copper accents, `.detail-body` structure).
   - Add the entry to `posts.js` (title, date, tag, excerpt) so it shows up on
     `blog.html` and the homepage Knowledge Hub automatically.
   - Write a separate LinkedIn-optimized version to
     `content/YYYY-MM-DD-slug.linkedin.txt` — shorter, hook-first, short line-broken
     paragraphs (LinkedIn strips most formatting), ending with a link back to the
     full post on aseembhandari.com. You copy/paste that into LinkedIn yourself —
     nothing here posts on your behalf.
3. Review both, then ask Claude to deploy (`netlify deploy --prod --dir .` from the
   site root), or run it yourself.
4. Post the `.linkedin.txt` content to LinkedIn whenever you're ready — it doesn't
   have to be the same day as the site publish.

## Why markdown source files, not just the HTML

The HTML pages are the *rendered* output, not the source. Keeping the original
markdown here means:
- You can regenerate or edit the HTML without reconstructing your original notes.
- If a post ever needs the LinkedIn version rewritten differently, the raw content
  is still there.
- Nothing about publishing depends on remembering exact HTML structure — that's
  Claude's job each time, driven from this file.

## Naming

`YYYY-MM-DD-slug.md` — the date is when you *start* the draft, not necessarily
publish date (the real publish date goes in the post's frontmatter / `posts.js`
entry and can differ).
