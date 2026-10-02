"""Build the portfolio from projects/<slug>/project.json."""
import json, re, html, hashlib
from pathlib import Path
ROOT = Path(__file__).parent
esc = html.escape
data = sorted((json.loads(p.read_text()) for p in (ROOT/'projects').glob('*/project.json')), key=lambda p: p['order'])
base = (ROOT/'verified-base.html').read_text()
style = re.search(r'<style>(.*?)</style>', base, re.S).group(1)
(ROOT/'styles.css').write_text(style + '\n' + (ROOT/'additions.css').read_text())
css_version = hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:12]
js_version = hashlib.sha256((ROOT/'script.js').read_bytes()).hexdigest()[:12]
head = re.search(r'<head>(.*?)</head>',base,re.S).group(1)
head = re.sub(r'<style>.*?</style>', f'<link rel="stylesheet" href="styles.css?v={css_version}">', head, flags=re.S)
def tags(p):
    return '<ul class="skill-tags" aria-label="Project skills">'+''.join(f'<li>#{esc(t)}</li>' for t in p.get('tags', []))+'</ul>'
def card(p, index):
    return f'''<article class="project-card accent-{p['color']}"><a class="card-link" href="projects/{p['slug']}/index.html"><div class="card-top"><span>{index:02d}</span><span>{esc(p['category'])}</span></div><h2>{esc(p['title'])}</h2><p>{esc(p['summary'])}</p>{tags(p)}<div class="card-meta"><span>{esc(p['context'])}</span><span>{esc(p['year'])}</span></div><span class="read-case">View project <span aria-hidden="true">↗</span></span></a></article>'''
def nav(prefix=''):
    return f'''<a class="skip-link" href="#main-content">Skip to content</a><header class="nav wrap"><a class="brand" href="{prefix}index.html">MATTEO PAOLINI</a><nav aria-label="Main navigation"><a href="{prefix}work.html">Work</a><a href="{prefix}index.html#about">About</a><a class="nav-cta" href="{prefix}index.html#contact">Contact</a></nav></header>'''
footer = '''<footer id="contact" class="wrap"><p class="label">CONTACT</p><div class="email-container"><a class="email" href="mailto:paolini134@gmail.com">Let’s talk<span>↗</span></a><button class="copy" id="copy-email" type="button">Copy email</button><div class="toast" id="toast" role="status" aria-live="polite"></div></div><div class="footer-bottom"><span>© 2026 Matteo Paolini</span><div class="social"><a href="https://github.com/matpaol">GitHub</a><a href="https://www.linkedin.com/in/matpaolini/">LinkedIn</a></div><a href="#top">Back to top ↑</a></div></footer>'''
script = f'<script src="script.js?v={js_version}" defer></script>'
profiles = '''<nav class="profile-links" aria-label="Professional profiles"><a href="https://github.com/matpaol">GitHub <span aria-hidden="true">↗</span></a><a href="https://www.linkedin.com/in/matpaolini/">LinkedIn <span aria-hidden="true">↗</span></a></nav>'''
footer = footer.replace('<div class="footer-bottom">', '<p class="contact-address"><a href="mailto:paolini134@gmail.com">paolini134@gmail.com</a></p>'+profiles+'<div class="footer-bottom">')
footer = re.sub(r'<div class="social">.*?</div>', '', footer)
home = re.sub(r'<head>.*?</head>', '<head>'+head+'</head>', base, flags=re.S)
home = re.sub(r'<header class="nav wrap">.*?</header>', nav(), home, flags=re.S)
home = home.replace('<main>', '<main id="main-content">')
home = home.replace('Building intelligent physical systems.', 'Robotics. Simulation. Mechanical design.')
home = home.replace('Robotics, simulation and intelligent manufacturing.', "Mechatronics engineering student · Research intern at the Royal Military Academy.")
home = home.replace('<a class="secondary" href="assets/Matteo-Paolini-CV.pdf" download>Download CV ↓</a>', '<button class="secondary cv-button" type="button" data-cv>Download CV ↓</button>')
home = home.replace('<span class="nerd" role="img" aria-label="nerd face">🤓</span>', '<button class="nerd" type="button" id="nerd-trigger" aria-label="Discover nerd mode" aria-haspopup="dialog" aria-controls="nerd-dialog">🤓</button>')
home = home.replace('</div></div><div class="bottom', '</div>'+profiles+'</div><div class="bottom', 1)
work = '<section id="work" class="wrap section"><header class="head"><p class="label">SELECTED WORK</p><a class="text-link" href="work.html">All work ↗</a></header><div class="project-grid">'+''.join(card(p,i+1) for i,p in enumerate(data) if p['featured'])+'</div></section>'
home = re.sub(r'<section id="work".*?</section>',work,home,flags=re.S)
home = home.replace('SELECTED WORK', 'HIGHLIGHTS')
home = re.sub(r'<div class="marquee-container">.*?</div></div>', '''<div class="about-grid"><p>I'm studying Mechanical Engineering with a specialization in Mechatronics at UNIVPM, with coursework at ULB and VUB in Brussels. My work connects robot motion planning, soft actuators, mechanical design and data analysis.</p><p>I'm currently doing a research internship at the Royal Military Academy within DREAM. I like projects where a model becomes something you can test, question and improve.</p></div><div class="expertise"><span>Robotics</span><span>Simulation</span><span>Mechanical design</span><span>Data &amp; AI</span></div>''',home,flags=re.S)
home = re.sub(r'<footer.*?</footer>',footer,home,flags=re.S)
home = home.replace('<div class="expertise"><span>Robotics</span><span>Simulation</span><span>Mechanical design</span><span>Data &amp; AI</span></div>', '<div class="expertise" aria-label="Skills"><span>#robotics</span><span>#3dprint</span><span>#nx</span><span>#fem</span><span>#python</span><span>#simulation</span><span>#cad</span></div>')
home = re.sub(r'<script>.*?</script>',script,home,flags=re.S)
dialog = '''<dialog id="cv-dialog"><button class="dialog-close" type="button" data-close aria-label="Close">×</button><p class="label">CURRICULUM VITAE</p><h2>An updated CV is on its way.</h2><p>For my current experience and availability, get in touch.</p><a class="button" href="mailto:paolini134@gmail.com">Request my CV</a></dialog>'''
nerd_dialog = '''<dialog id="nerd-dialog" class="nerd-dialog" aria-labelledby="nerd-title"><button class="dialog-close" type="button" data-close aria-label="Close nerd mode">×</button><div class="nerd-orbit" aria-hidden="true"><span>🤓</span><i></i><i></i><i></i><i></i></div><p class="label">YOU FOUND THE EASTER EGG</p><h2 id="nerd-title">Nerd mode unlocked.</h2><p>Cool ideas don’t build themselves.</p><p class="nerd-log">Curiosity: 100%<br>Prototypes: always in progress<br>Unexpected bugs: part of the process</p><button class="button" type="button" data-close>Back to tinkering ↗</button></dialog>'''
home=home.replace('</body>',dialog+nerd_dialog+'</body>')
(ROOT/'index.html').write_text(home.rstrip()+'\n')
archive = '''<section class="archive-intro wrap" id="top"><p class="label">PROJECT ARCHIVE</p><h1>Things I've worked on.</h1><p class="page-lead">Robotics, engineering design and data analysis. Academic projects, team work and research in progress.</p><div class="filters" role="group" aria-label="Filter projects"><button type="button" aria-pressed="true" data-filter="All">All</button>'''+''.join(f'<button type="button" aria-pressed="false" data-filter="{esc(c)}">{esc(c)}</button>' for c in dict.fromkeys(p['category'] for p in data))+'''</div><p class="filter-status" role="status" aria-live="polite"></p></section><section class="wrap archive-grid" aria-label="Projects"><div class="project-grid">'''+''.join(card(p,i+1).replace('<article ', f'<article data-category="{esc(p["category"])}" ') for i,p in enumerate(data))+'''</div><p class="empty-state" hidden>No projects in this category.</p></section>'''
(ROOT/'work.html').write_text('<!doctype html><html lang="en"><head>'+head.replace('Matteo Paolini — Portfolio','Work — Matteo Paolini')+'</head><body>'+nav()+'<main id="main-content">'+archive+'</main>'+footer+script+'</body></html>')
labels=[('overview','Overview'),('constraints','Requirements & constraints'),('contribution','My contribution'),('approach','Approach & decisions'),('results','Results & validation'),('limits','Limitations & next steps')]
(ROOT/'projects').mkdir(exist_ok=True)
for p in data:
    overview = f'''<section class="case-hero wrap" id="top"><a class="text-link back" href="../../work.html">← All work</a><p class="label">{esc(p['category'])}</p><h1>{esc(p['title'])}</h1><p class="page-lead">{esc(p['summary'])}</p><dl class="case-meta"><div><dt>Context</dt><dd>{esc(p['context'])}</dd></div><div><dt>Period</dt><dd>{esc(p['year'])}</dd></div><div><dt>Status</dt><dd>{esc(p['status'])}</dd></div><div><dt>Team</dt><dd>{esc(p['team'])}</dd></div></dl></section>'''
    links=''.join(f'<a class="resource" href="{esc(r[1])}">{esc(r[0])}<span aria-hidden="true">↗</span></a>' for r in p['links'])
    overview = overview.replace('<dl class="case-meta">', tags(p)+'<dl class="case-meta">')
    contents = '<div class="case-layout wrap"><aside><nav class="case-nav" aria-label="Case study sections">'+''.join(f'<a href="#{k}">{v}</a>' for k,v in labels)+'<a href="#resources">Resources</a></nav></aside><div class="case-content">'
    for k,v in labels:
        contents+=f'<section id="{k}" class="case-section"><p class="section-number">{labels.index((k,v))+1:02d}</p><h2>{v}</h2>'+''.join('<p>'+esc(t)+'</p>' for t in p[k])
        for media in p.get('media', []):
            if media.get('section', 'overview') != k:
                continue
            if media['type'] == 'youtube':
                contents+=f'''<div class="video-demo"><button type="button" class="video-load" data-video="{esc(media['id'])}"><span class="play-symbol" aria-hidden="true">▶</span><strong>{esc(media['title'])}</strong><span>Loads the YouTube demo on request</span></button></div>'''
            elif media['type'] == 'image':
                contents+=f'''<figure><img src="{esc(media['src'])}" width="{int(media['width'])}" height="{int(media['height'])}" loading="lazy" alt="{esc(media['alt'])}"><figcaption>{esc(media.get('caption', ''))}</figcaption></figure>'''
        contents+='</section>'
    contents+='<section id="resources" class="case-section"><p class="section-number">07</p><h2>Resources</h2><div class="resources">'+links+'</div>'+( '<p class="resource-note">Further project material will be added to this case study.</p>' if not links else '')+'</section></div></div>'
    ph=head.replace('href="styles.css','href="../../styles.css').replace('Matteo Paolini — Portfolio',esc(p['title'])+' — Matteo Paolini')
    page='<!doctype html><html lang="en"><head>'+ph+'</head><body>'+nav('../../')+'<main id="main-content">'+overview+contents+'</main>'+footer+script.replace('src="script.js','src="../../script.js')+'</body></html>'
    (ROOT/'projects'/p['slug']/'index.html').write_text(page)
print(f'Built home, archive and {len(data)} standardized project pages.')
