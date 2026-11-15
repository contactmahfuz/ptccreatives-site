# PTC Creatives — Official Website

Hand-coded static site for [PTC Creatives](https://ptccreatives.com) — a creative
production agency in Dhaka, Bangladesh. *Inspiring Creative Brilliance.*

## Stack
- Static HTML/CSS/JS — no server, no CMS
- GSAP + ScrollTrigger (animation), Lenis (smooth scroll), Tailwind v4 (tokens/utilities)
- Patachitra-inspired design system: day→night palette, hand-drawn motifs, film-grain texture

## Structure
- `index.html`, `about.html`, `services.html`, `case-studies.html`, `contact.html` — the site
- `css/`, `js/`, `img/` — compiled styles, scripts, and image assets
- `src/` — the Python generator and source blocks the site is built from

## Deployment
Served via GitHub Pages from the repository root. Content changes are made
through the generator in `src/` and republished as full builds.

Managed by Claude on behalf of PTC Creatives.
