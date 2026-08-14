#!/usr/bin/env python3
from pathlib import Path
import shutil

path = Path("index.html")
if not path.exists():
    raise SystemExit("ERROR: run from the 333.github.io repository root.")

text = path.read_text(encoding="utf-8")
if "Open FleaPit Media Gate" in text:
    print("ALREADY PATCHED: index.html")
    raise SystemExit(0)

backup = Path("index.html.pre-fleapit-network")
if not backup.exists():
    shutil.copy2(path, backup)

replacements = [
    (
        "333 Network — a local-first gateway connecting HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, and Bunya through one clear member journey.",
        "333 Network — a local-first gateway connecting HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, FleaPit, SIte, and Bunya through one clear member journey.",
    ),
    (
        "One Local Identity · Six Connected Application Spaces",
        "One Local Identity · Seven Connected Application Spaces",
    ),
    (
        "HOLLO · KANSEE · E=VEN MAIL · BAZAAR · SITE · BUNYA",
        "HOLLO · KANSEE · E=VEN MAIL · BAZAAR · FLEAPIT · SITE · BUNYA",
    ),
    (
        "Join the network, meet privately, apply for an address, participate creatively, build a site, or organize the infrastructure beneath it.",
        "Join the network, meet privately, apply for an address, participate creatively, discover media, build a site, or organize the infrastructure beneath it.",
    ),
    (
        '<div class="platform-stat"><strong>06</strong><span>Verified Applications</span></div>',
        '<div class="platform-stat"><strong>07</strong><span>Verified Applications</span></div>',
    ),
    (
        "This gateway reads only descriptive local records created by the six applications on this device.",
        "This gateway reads only descriptive local records created by the seven applications on this device.",
    ),
    (
        '<h2 id="applicationsTitle">Six roles. One organized network.</h2>',
        '<h2 id="applicationsTitle">Seven roles. One organized network.</h2>',
    ),
    (
        "All six launch paths were matched to existing files in the repository’s singular <code>app/</code> directory.",
        "All seven launch paths were matched to existing files in the repository’s singular <code>app/</code> directory.",
    ),
    (
        "HOLLO · KANSEE · E=Ven Mail · Bazaar Art Live · SIte · Bunya. A local-first network gateway within Verve N Veda.",
        "HOLLO · KANSEE · E=Ven Mail · Bazaar Art Live · FleaPit · SIte · Bunya. A local-first network gateway within Verve N Veda.",
    ),
]
for old, new in replacements:
    if old in text:
        text = text.replace(old, new, 1)

bazaar_choice = '''          <a class="choice-card" style="--accent:var(--rose)" href="./app/Bazaar_Art_Live_index.html">
            <span class="choice-icon" aria-hidden="true">✦</span><h3>Enter the Community</h3><p>Explore creative posts, groups, events, reels, and artistic participation.</p><span>Open Bazaar Art Live →</span>
          </a>'''
fleapit_choice = '''          <a class="choice-card" style="--accent:var(--gold)" href="./app/FleaPit™_media_gate_Index.html">
            <span class="choice-icon" aria-hidden="true">▶</span><h3>Explore Movies & Media</h3><p>Enter FleaPit for public-domain films, documentaries, learning media, family video, archives, and your saved library.</p><span>Open FleaPit Media Gate →</span>
          </a>'''
if bazaar_choice not in text:
    raise SystemExit("ERROR: Bazaar choice-card anchor not found; no change made.")
text = text.replace(bazaar_choice, bazaar_choice + "\n" + fleapit_choice, 1)

creation_anchor = '        <section class="category-shelf" style="--accent:var(--green)" aria-labelledby="creationTitle">'
media_section = '''        <section class="category-shelf" style="--accent:var(--gold)" aria-labelledby="mediaTitle">
          <div class="category-head"><div><h3 id="mediaTitle">Media</h3><p>Discover free-access and public-domain media while keeping a personal watch library under member control.</p></div><span class="category-count">1 application</span></div>
          <div class="app-grid single">
            <article class="app-card" style="--accent:var(--gold)" data-app data-search="fleapit movies media films documentaries family video archive lectures library favorites queue watch">
              <span class="app-icon" aria-hidden="true">▶</span><span class="app-tag">Media</span><h3>FleaPit™</h3><span class="app-sub">Media Gate & Protected Library</span><p>A local-first movie and media aggregator for public-domain films, official free sources, documentaries, learning media, family video, archives, and saved links.</p>
              <ul class="feature-list"><li>Media Gate leads into the full FleaPit Hub</li><li>Favorites, watch queue, notes, family controls, and recovery state</li><li>OHMIC-backed member library when the sovereign backend is available</li></ul>
              <div class="app-actions"><a href="./app/FleaPit™_media_gate_Index.html">Open FleaPit Media Gate</a></div>
            </article>
          </div>
        </section>

'''
if creation_anchor not in text:
    raise SystemExit("ERROR: Creation section anchor not found; no change made.")
text = text.replace(creation_anchor, media_section + creation_anchor, 1)

if 'fleapit:"fleapit_protected_state_v3"' not in text:
    text = text.replace(
        '        bazaar:"bazaar_live_frontend_v1",',
        '        bazaar:"bazaar_live_frontend_v1",\n        fleapit:"fleapit_protected_state_v3",',
        1,
    )
if 'fleapit:"./app/FleaPit™_media_gate_Index.html"' not in text:
    text = text.replace(
        '        bazaar:"./app/Bazaar_Art_Live_index.html",',
        '        bazaar:"./app/Bazaar_Art_Live_index.html",\n        fleapit:"./app/FleaPit™_media_gate_Index.html",',
        1,
    )

text = text.replace(
    '          bazaar:safeJson(STORAGE.bazaar),site:safeJson(STORAGE.site),bunya:safeJson(STORAGE.bunya)',
    '          bazaar:safeJson(STORAGE.bazaar),fleapit:safeJson(STORAGE.fleapit),site:safeJson(STORAGE.site),bunya:safeJson(STORAGE.bunya)',
    1,
)

bazaar_status = '          {id:"bazaar",name:"Bazaar Art Live",accent:"var(--rose)",href:LINKS.bazaar,detected:Boolean(data.bazaar),ready:Boolean(data.bazaar?.currentUserId),meta:data.bazaar?`${Array.isArray(data.bazaar.posts)?data.bazaar.posts.length:0} local posts detected`:"No local creative workspace detected"},'
fleapit_status = '          {id:"fleapit",name:"FleaPit",accent:"var(--gold)",href:LINKS.fleapit,detected:Boolean(data.fleapit),ready:Boolean(data.fleapit),meta:data.fleapit?`${Array.isArray(data.fleapit.media)?data.fleapit.media.length:0} saved media items detected`:"No local fallback library record detected"},'
if bazaar_status in text and fleapit_status not in text:
    text = text.replace(bazaar_status, bazaar_status + "\n" + fleapit_status, 1)

text = text.replace(
    "Bazaar profiles and feeds, SIte projects, and the Bunya registry operate locally in this browser.",
    "Bazaar profiles and feeds, FleaPit libraries, SIte projects, and the Bunya registry operate locally in this browser.",
    1,
)

path.write_text(text, encoding="utf-8")
print("PATCHED: index.html")
print("BACKUP: index.html.pre-fleapit-network")
