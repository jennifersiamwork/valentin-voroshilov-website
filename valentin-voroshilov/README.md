# Valentin Voroshilov — Website

Official website for violinist Valentin Voroshilov. Built with [Eleventy (11ty)](https://www.11ty.dev/) as a fast, static, multi-page site, ready to deploy on Netlify.

## Tech stack

- **Eleventy 2.x** — static site generator, outputs plain HTML (no client framework, nothing to break)
- **Nunjucks templates** for layouts and reusable components
- **Vanilla CSS** — single design-system stylesheet at `src/assets/css/style.css` using CSS custom properties (colors, type scale, spacing)
- **Vanilla JS** — `src/assets/js/main.js` (mobile nav, scroll reveals, gallery filter + lightbox, booking form)
- **Netlify Forms** for the booking inquiry form — no backend/server required

## Local development

```bash
npm install
npm start      # serves the site locally with live reload at http://localhost:8080
npm run build  # builds the static site into _site/
```

## Deploying

1. Push this project to a GitHub repository.
2. In Netlify: **Add new site → Import an existing project → GitHub**, select the repo.
3. Build command: `npm run build`. Publish directory: `_site`. (Already configured in `netlify.toml`.)
4. Deploy. Netlify will automatically detect the booking form (`data-netlify="true"` on the `<form>` in `src/contact.njk`) and start collecting submissions under **Site → Forms** in the Netlify dashboard — no extra setup needed.
5. Optional: connect a custom domain in Netlify's Domain settings.

## Editing content

Almost everything a non-developer needs to update lives in `src/_data/*.json` — plain data files, no template editing required.

| What to change | File |
|---|---|
| Contact email, WhatsApp number, TikTok handle, social links, nav labels | `src/_data/site.json` |
| Gallery photos & categories | `src/_data/gallery.json` (add image files to `src/assets/images/gallery/` and reference them) |
| Video embeds (Instagram / TikTok / YouTube / uploaded) | `src/_data/videos.json` — set `embedUrl` once you have a real embeddable link |
| Selected Work / portfolio entries | `src/_data/events.json` — duplicate the template entry to add a new event |
| Testimonials | `src/_data/testimonials.json` — replace placeholder entries with real quotes and set `isPlaceholder: false` |
| Page copy (About bio, Performances descriptions, etc.) | The relevant `.njk` file in `src/` (e.g. `src/about.njk`) |

After editing any file, run `npm run build` locally to preview, or just push to GitHub — Netlify rebuilds automatically.

## ⚠️ Placeholders that must be replaced before launch

This site was built strictly from the facts provided. Nothing was invented. The following are clearly marked placeholders and **must** be replaced with real information before the site goes live:

- **Photography & video** — every image on the site is an elegant abstract placeholder graphic (charcoal/ivory, labeled), not a stock photo. Replace files referenced in `src/_data/gallery.json`, `src/_data/events.json`, `src/_data/videos.json`, and the `heroImage`/`headerImage` front matter in each page with real photography and video.
- **Booking email address** — `site.email` / `site.emailHref` in `src/_data/site.json`.
- **Phone / WhatsApp number** — `site.phone` / `site.whatsappHref` in `src/_data/site.json`.
- **TikTok handle & URL** — `site.tiktokHandle` / `site.tiktokUrl` in `src/_data/site.json`.
- **YouTube / Facebook URLs** — only add these if applicable; currently placeholders in `site.json`.
- **Domain name** — replace `https://www.valentinvoroshilov.com` in `src/_data/site.json` (`site.url`) and in `src/robots.txt` once a real domain is chosen. This value drives canonical URLs, Open Graph tags, structured data and the sitemap.
- **LEPAS L6 event date** — marked "exact date to be confirmed" in `src/_data/events.json`. Only the fact provided (performance at the LEPAS L6 presentation event in Thailand, with orchestra) was used; no additional details were invented.
- **Testimonials** — all four cards on the Testimonials page are explicitly marked placeholders. No testimonials were invented. Add real, attributed client quotes when available.
- **Estonian competition result** — per instructions, this has intentionally **not** been added anywhere on the site pending verification. Once documentation is confirmed, it can be added to `src/about.njk` (Education & Experience) and `src/_data/site.json`.

## Adding future content

- **New gallery image:** drop the file in `src/assets/images/gallery/`, add an entry to `gallery.json` with a `category` (`weddings`, `corporate`, `concerts`, `events`, `bts`) and a `size` (`lg`, `md`, `sm`) for the editorial grid layout.
- **New event/portfolio piece:** duplicate an entry in `events.json`.
- **New testimonial:** duplicate an entry in `testimonials.json`, fill in the quote/name/event type/location, set `"isPlaceholder": false`.
- **New video:** add an entry to `videos.json`. For YouTube, `embedUrl` is `https://www.youtube.com/embed/VIDEO_ID`. For Instagram/TikTok, use their official embed/oEmbed URLs once available, or continue linking out from the platform icons in the footer.

## Regenerating placeholder artwork

All placeholder imagery (the abstract charcoal/ivory graphics standing in for real photography) is generated by two small Python scripts, not hand-drawn files:

```bash
python3 scripts/gen_svg_placeholders.py   # regenerates src/assets/images/ph/*.svg
python3 scripts/gen_og_image.py           # regenerates src/assets/images/og-default.jpg
```

You don't need to run these unless you want to change the placeholder style — once real photography is added, these placeholder files are simply no longer referenced.

## SEO

- Unique title + meta description per page (front matter `title` / `description`)
- Open Graph + Twitter Card metadata on every page (`src/_includes/partials/seo.njk`)
- JSON-LD structured data: sitewide `Person` schema, `BreadcrumbList` per page, `Event` schema for each Selected Work entry
- `sitemap.xml` generated automatically from all published pages (`src/sitemap.njk`)
- `robots.txt` at the site root
- Clean, descriptive URLs (`/about/`, `/performances/`, `/gallery/`, etc.)
- Descriptive `alt` text on every image, including a note that current images are placeholders

## Accessibility notes

- Skip-to-content link, visible focus states, semantic headings
- Reduced-motion media query disables scroll reveals/animations for users who request it
- Lightbox and mobile menu are keyboard-operable (Escape to close, arrow keys to navigate the lightbox)
- Form fields are labeled; the honeypot field is hidden from assistive tech via layout only (not `display:none`, per Netlify's spam-filter requirements) — this is expected and does not affect real users
