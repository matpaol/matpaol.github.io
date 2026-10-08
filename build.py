"""Build the portfolio from site.json and projects/<slug>/project.json.

Featured and archive projects with "page": true get a case-study page.
Archive projects without a page appear as one line in "More projects".
Run:  python3 build.py
"""
import json, re, html, hashlib
from pathlib import Path

ROOT = Path(__file__).parent
esc = html.escape
SITE = json.loads((ROOT / 'site.json').read_text())
BASE_URL = SITE['base_url'].rstrip('/')
data = sorted((json.loads(p.read_text()) for p in (ROOT / 'projects').glob('*/project.json')), key=lambda p: p['order'])
featured = [p for p in data if p['tier'] == 'featured']
archive = [p for p in data if p['tier'] == 'archive']
paged = [p for p in data if p.get('page', True)]

base = (ROOT / 'verified-base.html').read_text()
style = re.search(r'<style>(.*?)</style>', base, re.S).group(1)
(ROOT / 'styles.css').write_text(style + '\n' + (ROOT / 'additions.css').read_text())
css_version = hashlib.sha256((ROOT / 'styles.css').read_bytes()).hexdigest()[:12]
js_version = hashlib.sha256((ROOT / 'script.js').read_bytes()).hexdigest()[:12]
favicon = re.search(r'<link rel="icon"[^>]*>', base).group(0)
ANALYTICS = '''<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"4b2e7c8361d5458f8de2fc44bc58b2a4"}'></script>'''


def head(title, description, prefix='', image=None, path=''):
    image = image or SITE['og_image']
    url = f'{BASE_URL}/{path}'
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#fff" media="(prefers-color-scheme:light)"><meta name="theme-color" content="#0a0a0b" media="(prefers-color-scheme:dark)">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Matteo Paolini"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(url)}"><meta property="og:image" content="{esc(BASE_URL + '/' + image)}">
<meta name="twitter:card" content="summary_large_image">
{favicon}<link rel="stylesheet" href="{prefix}styles.css?v={css_version}">
{ANALYTICS}'''


def nav(prefix=''):
    return f'''<a class="skip-link" href="#main-content">Skip to content</a><header class="nav wrap"><a class="brand" href="{prefix}index.html">MATTEO PAOLINI</a><nav aria-label="Main navigation"><a href="{prefix}work.html">Work</a><a href="{prefix}index.html#about">About</a><a class="nav-cta" href="{prefix}index.html#contact">Contact</a></nav></header>'''


def profiles():
    return '<nav class="profile-links" aria-label="Professional profiles">' + ''.join(
        f'<a href="{esc(u)}">{esc(n)} <span aria-hidden="true">↗</span></a>' for n, u in SITE['profiles']) + '</nav>'


def footer(prefix=''):
    return f'''<footer id="contact" class="wrap"><p class="label">CONTACT</p><div class="email-container"><a class="email" href="mailto:{SITE['email']}">Let’s talk<span>↗</span></a><button class="copy" id="copy-email" type="button">Copy email</button><div class="toast" id="toast" role="status" aria-live="polite"></div></div><p class="contact-address"><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>{profiles()}<div class="footer-bottom"><span>© 2026 Matteo Paolini</span><a href="{prefix}assets/Matteo-Paolini-CV.pdf">CV (PDF)</a><a href="#top">Back to top ↑</a></div></footer><script src="{prefix}script.js?v={js_version}" defer></script>'''


def tools(p, cls='tool-list'):
    return f'<ul class="{cls}" aria-label="Tools">' + ''.join(f'<li>{esc(t)}</li>' for t in p.get('tools', [])) + '</ul>'


def card(p, prefix='', wide=False):
    cover = p.get('cover')
    img = (f'<div class="card-media"><img src="{prefix}{esc(cover["src"])}" alt="" decoding="async"'
           + (f' style="object-fit:{cover["fit"]}"' if cover.get('fit') else '') + '></div>') if cover else ''
    metric = p['metrics'][0] if p.get('metrics') else None
    metric_html = f'<p class="card-metric"><strong>{esc(metric[0])}</strong> {esc(metric[1])}</p>' if metric else ''
    return f'''<article class="project-card accent-{p['color']}{' card-wide' if wide else ''}" data-category="{esc(p['category'])}"><a class="card-link" href="{prefix}projects/{p['slug']}/index.html">{img}<div class="card-body"><div class="card-top"><span>{esc(p['category'])}</span><span>{esc(p['year'])}</span></div><h2>{esc(p['title'])}</h2><p>{esc(p['summary'])}</p>{metric_html}<div class="card-meta"><span>{esc(p['role'])}</span></div><span class="read-case">View case study <span aria-hidden="true">→</span></span></div></a></article>'''


def archive_row(p, prefix=''):
    title = esc(p['title'])
    if p.get('page', True):
        title = f'<a href="{prefix}projects/{p["slug"]}/index.html">{title} <span aria-hidden="true">→</span></a>'
    elif p.get('links'):
        title = f'<a href="{esc(p["links"][0][1])}">{title} <span aria-hidden="true">↗</span></a>'
    return f'<li><span class="archive-year">{esc(p["year"])}</span><div><h3>{title}</h3><p>{esc(p["summary"])}</p></div><span class="archive-cat">{esc(p["category"])}</span></li>'


def page(title, description, body, prefix='', image=None, path=''):
    return ('<!doctype html><html lang="en"><head>' + head(title, description, prefix, image, path) + '</head><body>'
            + nav(prefix) + '<main id="main-content">' + body + '</main>' + footer(prefix) + '</body></html>\n')


# ---------- Home ----------
hero = SITE['hero']
home_body = f'''<section id="top" class="hero wrap"><div><h1 class="reveal d1">{hero['headline_html']}<button class="nerd" type="button" id="nerd-trigger" aria-label="Discover nerd mode" aria-haspopup="dialog" aria-controls="nerd-dialog">🤓</button></h1><p class="intro reveal d2">{esc(hero['intro'])}</p><p class="scope reveal d3">{esc(hero['scope'])}</p><div class="hero-actions reveal d3"><a class="primary" href="#work">Explore work ↓</a><a class="secondary cv-button" href="assets/Matteo-Paolini-CV.pdf" download="Matteo-Paolini-CV.pdf">Download CV ↓</a></div>{profiles()}</div><div class="bottom reveal d3"><p class="available"><span class="dot"></span>{esc(hero['availability'])}</p><a class="down" href="#work" aria-label="Scroll to work">↓</a></div></section>
<section id="work" class="wrap section"><header class="head"><p class="label">SELECTED WORK</p><a class="text-link" href="work.html">All projects →</a></header><div class="project-grid">{''.join(card(p, wide=(i == 0)) for i, p in enumerate(featured))}</div></section>
<section id="about" class="wrap section"><p class="label">ABOUT</p><p class="statement">An engineer interested in the space between an <span class="blue">idea</span>, a <span class="pink">simulation</span> and a working <span class="yellow">machine</span>.</p><div class="about-grid">{''.join('<p>' + esc(t) + '</p>' for t in SITE['about'])}</div><dl class="about-facts">{''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in SITE['facts'])}</dl><div class="expertise" aria-label="Toolkit">{''.join(f'<span>{esc(t)}</span>' for t in SITE['toolkit'])}</div></section>'''
nerd_dialog = '''<dialog id="nerd-dialog" class="nerd-dialog" aria-labelledby="nerd-title"><button class="dialog-close" type="button" data-close aria-label="Close nerd mode">×</button><div class="nerd-orbit" aria-hidden="true"><span>🤓</span><i></i><i></i><i></i><i></i></div><p class="label">YOU FOUND THE EASTER EGG</p><h2 id="nerd-title">Nerd mode unlocked.</h2><p>Cool ideas don’t build themselves.</p><p class="nerd-log">Curiosity: 100%<br>Prototypes: always in progress<br>Unexpected bugs: part of the process</p><button class="button" type="button" data-close>Back to tinkering ↗</button></dialog>'''
(ROOT / 'index.html').write_text(page(SITE['title'], SITE['description'], home_body).replace('</body>', nerd_dialog + '</body>'))

# ---------- Work ----------
cats = list(dict.fromkeys(p['category'] for p in featured))
work_body = f'''<section class="archive-intro wrap" id="top"><p class="label">WORK</p><h1>Selected projects.</h1><p class="page-lead">{esc(SITE['work_lead'])}</p><div class="filters" role="group" aria-label="Filter projects"><button type="button" aria-pressed="true" data-filter="All">All</button>{''.join(f'<button type="button" aria-pressed="false" data-filter="{esc(c)}">{esc(c)}</button>' for c in cats)}</div><p class="filter-status" role="status" aria-live="polite"></p></section>
<section class="wrap archive-grid" aria-label="Selected projects"><div class="project-grid">{''.join(card(p, wide=(i == 0)) for i, p in enumerate(featured))}</div><p class="empty-state" hidden>No projects in this category.</p></section>
<section class="wrap section more-work" id="archive" aria-labelledby="archive-title"><header class="head"><p class="label" id="archive-title">MORE PROJECTS</p></header><ul class="archive-list">{''.join(archive_row(p) for p in archive)}</ul></section>'''
(ROOT / 'work.html').write_text(page('Work — Matteo Paolini', SITE['work_lead'], work_body, path='work.html'))


# ---------- Project pages ----------
def media_html(m, slug):
    t = m['type']
    if t == 'image':
        return f'''<figure class="{esc(m.get('class', ''))}"><img src="{esc(m['src'])}" width="{int(m['width'])}" height="{int(m['height'])}" loading="lazy" decoding="async" alt="{esc(m['alt'])}"><figcaption>{esc(m.get('caption', ''))}</figcaption></figure>'''
    if t == 'gallery':
        return '<div class="figure-row">' + ''.join(media_html(dict(i, type='image'), slug) for i in m['items']) + '</div>'
    if t == 'youtube':
        return f'''<div class="video-demo"><button type="button" class="video-load" data-video="{esc(m['id'])}" data-title="{esc(m['title'])}"><span class="play-symbol" aria-hidden="true">▶</span><strong>{esc(m['title'])}</strong><span>Loads the YouTube video on request</span></button></div>'''
    if t == 'video':
        return f'''<figure><video class="project-video" controls playsinline preload="none" poster="{esc(m['poster'])}" aria-label="{esc(m['title'])}"><source src="{esc(m['src'])}" type="video/mp4">Your browser does not support video. <a href="{esc(m['src'])}">Open the demo</a>.</video><figcaption>{esc(m['caption'])}</figcaption></figure>'''
    if t == 'map':
        return f'''<figure><div class="map-demo"><button class="map-load" type="button" data-map="{esc(m['src'])}" data-title="{esc(m['title'])}">Explore the route map ↗</button></div><figcaption>{esc(m['caption'])} <a href="{esc(m['src'])}" target="_blank" rel="noopener">Open full screen ↗</a></figcaption></figure>'''
    if t == 'svg':
        return '<figure class="diagram">' + (ROOT / 'projects' / slug / m['src']).read_text() + f'<figcaption>{esc(m.get("caption", ""))}</figcaption></figure>'
    raise ValueError(t)


def section_html(s, i, slug):
    out = f'<section id="{s["id"]}" class="case-section"><p class="section-number">{i:02d}</p><h2>{esc(s["title"])}</h2>'
    for block in s.get('body', []):
        if isinstance(block, str):
            out += '<p>' + esc(block) + '</p>'
        elif 'list' in block:
            out += '<ul class="case-list">' + ''.join('<li>' + esc(x) + '</li>' for x in block['list']) + '</ul>'
        elif 'log' in block:
            out += '<ol class="research-log">' + ''.join(f'<li><time>{esc(d)}</time><p>{esc(x)}</p></li>' for d, x in block['log']) + '</ol>'
        elif 'note' in block:
            out += '<p class="case-note">' + esc(block['note']) + '</p>'
        else:
            out += media_html(block, slug)
    return out + '</section>'


for p in paged:
    pre = '../../'
    metrics = ''.join(f'<div><dt>{esc(l)}</dt><dd>{esc(v)}</dd></div>' for v, l in p.get('metrics', []))
    cover = p.get('hero_media') or p.get('cover')
    cover_html = ''
    if cover:
        src = cover['src'] if cover['src'].startswith('media/') else pre + cover['src']
        cover_html = f'<figure class="case-cover"><img src="{esc(src)}" alt="{esc(cover.get("alt", ""))}" decoding="async"' + (f' style="object-fit:{cover["fit"]}"' if cover.get('fit') else '') + f'>' + (f'<figcaption>{esc(cover["caption"])}</figcaption>' if cover.get('caption') else '') + '</figure>'
    tldr = '<ul class="tldr">' + ''.join('<li>' + esc(x) + '</li>' for x in p.get('tldr', [])) + '</ul>' if p.get('tldr') else ''
    meta = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p['facts'])
    hero_html = f'''<section class="case-hero wrap" id="top"><a class="text-link back" href="{pre}work.html">← All work</a><p class="label">{esc(p['category'])}</p><h1>{esc(p['title'])}</h1><p class="page-lead">{esc(p['summary'])}</p>{f'<dl class="metrics">{metrics}</dl>' if metrics else ''}{cover_html}<div class="case-summary">{tldr}<dl class="case-meta">{meta}</dl></div>{tools(p)}</section>'''
    sections = p['sections']
    links = ''.join(f'<a class="resource" href="{esc(u)}">{esc(n)}<span aria-hidden="true">↗</span></a>' for n, u in p.get('links', []))
    nav_links = ''.join(f'<a href="#{s["id"]}">{esc(s["title"])}</a>' for s in sections) + ('<a href="#resources">Resources</a>' if links else '')
    body = '<div class="case-layout wrap"><aside><nav class="case-nav" aria-label="Case study sections">' + nav_links + '</nav></aside><div class="case-content">'
    body += ''.join(section_html(s, i + 1, p['slug']) for i, s in enumerate(sections))
    if links:
        body += f'<section id="resources" class="case-section"><p class="section-number">{len(sections) + 1:02d}</p><h2>Resources</h2><div class="resources">{links}</div>' + (f'<p class="case-note">{esc(p["links_note"])}</p>' if p.get('links_note') else '') + '</section>'
    body += '</div></div>'
    image = (p.get('cover') or {}).get('src')
    if image and image.endswith('.svg'):
        image = None
    html_out = page(f"{p['title']} — Matteo Paolini", p['summary'], hero_html + body, pre, image, f"projects/{p['slug']}/")
    (ROOT / 'projects' / p['slug'] / 'index.html').write_text(html_out)

# Old URLs of projects that no longer have a page redirect to the archive list.
for p in data:
    if not p.get('page', True):
        target = '../../work.html#archive'
        (ROOT / 'projects' / p['slug'] / 'index.html').write_text(
            f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{BASE_URL}/work.html"><title>{esc(p["title"])} — Matteo Paolini</title></head><body><p><a href="{target}">{esc(p["title"])} is listed under More projects.</a></p></body></html>\n')

print(f'Built home, work and {len(paged)} case studies ({len(featured)} featured, {len(archive)} archive).')
