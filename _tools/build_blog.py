"""Build /blog/ pages from _blog-src/*.md.

Each source starts with an HTML comment holding JSON front matter (slug, lang, title,
seo_title, description, date, updated, cover, cover_alt, keywords, takeaways, faq), then
Markdown. Writes blog/<slug>.html, blog/index.html and refreshes the blog entries in
sitemap.xml.

In the Markdown (and front matter text):
  {{scraper.comment}}      price per event, e.g. "$0.001"
  {{scraper.comment@1k}}   price per 1,000 events, e.g. "$1"
  [[card:scraper]]         on its own line: an Actor card with logo, price and button
Prices come live from the Apify Store, so posts follow price changes on the next build;
_blog-src/prices.json caches the last fetch for offline builds.

    pip install markdown
    python3 _tools/build_blog.py
"""
import html
import json
import math
import re
import urllib.request
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_blog-src"
OUT = ROOT / "blog"
SITE = "https://scrapers.practicemysql.com"
REFERRAL = "fpr=2untzw"  # Apify referral ID, added to every link to our own Actors

ACTORS = {
    "scraper": {"id": "molded_mountainpass~bilibili-scraper", "name": "Bilibili Scraper",
                "url": "https://apify.com/molded_mountainpass/bilibili-scraper", "logo": "/images/bilibili-scraper.webp"},
    "danmaku": {"id": "molded_mountainpass~bilibili-danmaku-scraper", "name": "Bilibili Danmaku Scraper",
                "url": "https://apify.com/molded_mountainpass/bilibili-danmaku-scraper", "logo": "/images/bilibili-danmaku-scraper.webp"},
}
SCRAPER = ACTORS["scraper"]["url"]
DANMAKU = ACTORS["danmaku"]["url"]

HEAD_TAGS = """  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-P4NHL4WT');</script>
  <!-- End Google Tag Manager -->
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MH5BEL56V4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-MH5BEL56V4');
  </script>"""

FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css?v=20261112">
  <script src="/script.js"></script>"""

BODY_TOP = """  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P4NHL4WT"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
  <nav>
    <div class="wrap">
      <a class="brand" href="/"><i>DR</i><span>Divya Raj · Scrapers</span></a>
      <ul>
        <li><a href="/#scrapers">Scrapers</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/#about">About</a></li>
      </ul>
    </div>
  </nav>"""

FOOTER = """  <footer>
    <div class="wrap">
      <p>All scrapers read public data only. Bilibili is a trademark of its owner; these tools are independent and not affiliated with Bilibili.</p>
      <p>Apify links on this site are referral links: if you sign up and later choose a paid Apify plan, I may earn a reward, at no extra cost to you.</p>
      <p>© Divya Raj · <a href="/">scrapers.practicemysql.com</a> · <a href="mailto:divyaraj@practicemysql.com">divyaraj@practicemysql.com</a></p>
    </div>
  </footer>"""

# Highlights the TOC entry of the section being read; collapses the TOC on small screens.
TOC_JS = """  <script>
  (function () {
    var toc = document.querySelector('.post-toc details');
    if (toc && window.matchMedia('(max-width: 960px)').matches) toc.removeAttribute('open');
    var links = document.querySelectorAll('.post-toc a[href^="#"]');
    if (!('IntersectionObserver' in window) || !links.length) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove('active'); });
        var a = map[e.target.id];
        if (a) a.classList.add('active');
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  })();
  </script>"""

AUTHOR = {"@type": "Person", "name": "Divya Raj", "url": SITE + "/"}

LABELS = {
    "en": {"home": "Home", "blog": "Blog", "updated": "Updated", "faq": "FAQ", "faq_h": "Frequently asked questions",
           "try": "Try the Bilibili Scraper", "danmaku": "Danmaku-only scraper", "more": "More Bilibili guides",
           "toc": "On this page", "takeaways": "Key takeaways", "read": "min read", "try_free": "Try it free",
           "cta": "<strong>Want the data without writing code?</strong> The Bilibili Scraper exports comments, danmaku, videos and UP主 profiles to Excel, CSV or JSON. Pay per result, no login.",
           "cards": {
               "scraper": ("Comments with replies, danmaku, videos, UP主 profiles and subtitles in one tool. No login.",
                           "Comments {scraper.comment@1k} / 1,000 · Danmaku {scraper.danmaku@1k} / 1,000 · Open source"),
               "danmaku": ("Bullet comments with timestamps, a keyword filter and free per-video highlight summaries.",
                           "Danmaku {danmaku.danmaku@1k} / 1,000 · Summary rows free"),
           }},
    "zh-CN": {"home": "首页", "blog": "博客", "updated": "更新于", "faq": "常见问题", "faq_h": "常见问题",
              "try": "免费试用 Bilibili Scraper", "danmaku": "弹幕专用版", "more": "更多 B站 数据教程",
              "toc": "本文目录", "takeaways": "要点速览", "read": "分钟阅读", "try_free": "免费试用",
              "cta": "<strong>不想写代码？</strong> Bilibili Scraper 可一键导出 B站评论、弹幕、视频和 UP主 数据到 Excel / CSV / JSON，按结果计费，无需登录。",
              "cards": {
                  "scraper": ("评论（含楼中楼）、弹幕、视频、UP主、字幕，一个工具全搞定，无需登录。",
                              "评论 {scraper.comment@1k} / 千条 · 弹幕 {scraper.danmaku@1k} / 千条 · 开源"),
                  "danmaku": ("带时间轴的弹幕，支持关键词过滤和免费的高能时刻统计。",
                              "弹幕 {danmaku.danmaku@1k} / 千条 · 统计行免费"),
              }},
}


def fetch_prices():
    """Current per-event USD prices of both Actors, from the public Apify Store."""
    cache = SRC / "prices.json"
    prices = {}
    try:
        for key, a in ACTORS.items():
            q = a["name"].lower().replace(" ", "%20")
            items = json.load(urllib.request.urlopen(f"https://api.apify.com/v2/store?limit=50&search={q}", timeout=20))["data"]["items"]
            item = next(x for x in items if f"{x['username']}~{x['name']}" == a["id"])
            events = (item.get("currentPricingInfo") or {}).get("pricingPerEvent", {}).get("actorChargeEvents", {})
            prices[key] = {k: v["eventPriceUsd"] for k, v in events.items() if v.get("eventPriceUsd") is not None}
        cache.write_text(json.dumps(prices, indent=2) + "\n", encoding="utf-8")
    except Exception as e:  # offline or the Store changed shape: use the last good fetch
        print(f"price fetch failed ({e}); using {cache.name}")
        prices = json.loads(cache.read_text(encoding="utf-8"))
    return prices


def money(x):
    if x >= 1:
        return f"${x:,.2f}".replace(".00", "")
    return "$" + f"{x:.6f}".rstrip("0").rstrip(".")


def fill_prices(text, prices):
    def sub(m):
        actor, event, per1k = m.group(1), m.group(2), m.group(3)
        price = prices[actor][event]
        return money(price * 1000) if per1k else money(price)
    return re.sub(r"\{\{?(scraper|danmaku)\.([a-z-]+)(@1k)?\}?\}", sub, text)


def load(path, prices):
    text = fill_prices(path.read_text(encoding="utf-8"), prices)
    m = re.match(r"<!--\s*(\{.*?\})\s*-->\s*", text, re.S)
    meta = json.loads(m.group(1))
    meta["body_md"] = text[m.end():]
    return meta


def esc(s):
    return html.escape(s, quote=True)


def actor_card(key, lang, prices):
    a = ACTORS[key]
    lab = LABELS[lang]
    tagline, price = lab["cards"][key]
    return (f'<div class="actor-card">'
            f'<img src="{a["logo"]}" alt="{esc(a["name"])} logo" width="64" height="64" loading="lazy">'
            f'<div class="actor-info"><strong>{esc(a["name"])}</strong><span>{esc(tagline)}</span>'
            f'<span class="actor-price">{esc(fill_prices(price, prices))}</span></div>'
            f'<a class="btn" href="{a["url"]}" rel="noopener">{lab["try_free"]} →</a></div>')


def reading_minutes(md_text, lang):
    plain = re.sub(r"```.*?```", "", md_text, flags=re.S)
    if lang.startswith("zh"):
        return max(1, math.ceil(len(re.findall(r"[一-鿿]", plain)) / 400 + len(plain.split()) / 600))
    return max(1, math.ceil(len(plain.split()) / 220))


def render_post(p, posts, prices):
    lab = LABELS[p["lang"]]
    url = f"{SITE}/blog/{p['slug']}"
    img = f"{SITE}/images/blog/{p['cover']}"
    md_src = re.sub(r"^\[\[card:(scraper|danmaku)\]\]$", lambda m: actor_card(m.group(1), p["lang"], prices),
                    p["body_md"], flags=re.M)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    body = md.convert(md_src)
    body = re.sub(r'<a href="(https?://[^"]+)"(?! rel)', r'<a href="\1" rel="noopener"', body)
    toc_items = "\n".join(f'              <li><a href="#{t["id"]}">{esc(html.unescape(t["name"]))}</a></li>'
                          for t in md.toc_tokens if t["level"] == 2)
    if p.get("faq"):
        toc_items += f'\n              <li><a href="#faq">{lab["faq_h"]}</a></li>'
    takeaways = ""
    if p.get("takeaways"):
        lis = "".join(f"<li>{markdown.markdown(t)[3:-4]}</li>" for t in p["takeaways"])
        takeaways = f'<div class="takeaways"><p class="takeaways-h">⚡ {lab["takeaways"]}</p><ul>{lis}</ul></div>'
    minutes = reading_minutes(p["body_md"], p["lang"])
    graph = [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "image": img,
         "datePublished": p["date"], "dateModified": p["updated"], "inLanguage": p["lang"], "author": AUTHOR,
         "publisher": AUTHOR, "mainEntityOfPage": url, "keywords": p["keywords"], "timeRequired": f"PT{minutes}M",
         "about": [{"@type": "SoftwareApplication", "name": a["name"], "url": a["url"], "image": SITE + a["logo"],
                    "applicationCategory": "BusinessApplication", "operatingSystem": "Web"} for a in ACTORS.values()]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": lab["home"], "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": lab["blog"], "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["seo_title"], "item": url}]},
    ]
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    faq_html = "\n".join(
        f'          <details class="reveal"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p.get("faq", []))
    related = "\n".join(
        f'          <li><a href="/blog/{o["slug"]}">{esc(o["title"])}</a></li>' for o in posts if o["slug"] != p["slug"])
    s = ACTORS["scraper"]
    return f"""<!doctype html>
<html lang="{p['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{HEAD_TAGS}
  <title>{esc(p['seo_title'])}</title>
  <meta name="description" content="{esc(p['description'])}">
  <meta name="keywords" content="{esc(p['keywords'])}">
  <meta name="author" content="Divya Raj">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="article">
  <meta property="og:title" content="{esc(p['title'])}">
  <meta property="og:description" content="{esc(p['description'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img}">
  <meta property="article:published_time" content="{p['date']}">
  <meta property="article:modified_time" content="{p['updated']}">
  <meta name="twitter:card" content="summary_large_image">

  <script type="application/ld+json">
{ld}
  </script>

{FONTS}
</head>
<body>
{BODY_TOP}

  <header class="hero post-hero" id="top">
    <div class="wrap">
      <p class="crumbs"><a href="/">{lab['home']}</a> › <a href="/blog/">{lab['blog']}</a></p>
      <div class="post-logos"><img src="{s['logo']}" alt="" width="40" height="40"><img src="{ACTORS['danmaku']['logo']}" alt="" width="40" height="40"><span>Bilibili · 哔哩哔哩 · B站</span></div>
      <h1>{esc(p['title'])}</h1>
      <p class="post-meta">Divya Raj · {lab['updated']} <time datetime="{p['updated']}">{p['updated']}</time> · {minutes} {lab['read']}</p>
      <div class="cta">
        <a class="btn big" href="{SCRAPER}">{lab['try']}</a>
        <a class="btn ghost" href="{DANMAKU}">{lab['danmaku']}</a>
      </div>
    </div>
  </header>
  <main>
    <section>
      <div class="wrap post-layout">
        <article class="post">
          <img class="post-cover" src="/images/blog/{p['cover']}" alt="{esc(p['cover_alt'])}" width="1000" height="420">
          {takeaways}
{body}
        </article>
        <aside class="post-toc">
          <details open>
            <summary>{lab['toc']}</summary>
            <ol>
{toc_items}
            </ol>
          </details>
          <a class="toc-card" href="{s['url']}" rel="noopener">
            <img src="{s['logo']}" alt="{esc(s['name'])} logo" width="48" height="48" loading="lazy">
            <span><strong>{esc(s['name'])}</strong>{esc(fill_prices(lab['cards']['scraper'][1], prices))}</span>
          </a>
        </aside>
      </div>
    </section>
    <section id="faq">
      <div class="wrap">
        <p class="kicker">{lab['faq']}</p>
        <h2>{lab['faq_h']}</h2>
        <div class="faq">
{faq_html}
        </div>
        <div class="note reveal">{lab['cta']}</div>
        <div class="cta center reveal">
          <a class="btn big" href="{SCRAPER}">{lab['try']}</a>
        </div>
      </div>
    </section>
    <section>
      <div class="wrap">
        <p class="kicker">{lab['more']}</p>
        <ul class="post-list">
{related}
        </ul>
      </div>
    </section>
  </main>
{FOOTER}
{TOC_JS}
</body>
</html>
"""


def render_index(posts, prices):
    url = SITE + "/blog/"
    items = "\n".join(f"""          <article class="card reveal">
            <a href="/blog/{p['slug']}"><img class="post-thumb" src="/images/blog/{p['cover']}" alt="{esc(p['cover_alt'])}" width="1000" height="420" loading="lazy"></a>
            <h3><a class="title-link" href="/blog/{p['slug']}">{esc(p['title'])}</a></h3>
            <p class="what">{esc(p['description'])}</p>
          </article>""" for p in posts)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Blog", "name": "Bilibili Data Guides",
                     "url": url, "author": AUTHOR,
                     "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}",
                                   "datePublished": p["date"], "inLanguage": p["lang"]} for p in posts]},
                    ensure_ascii=False, indent=2)
    cards = actor_card("scraper", "en", prices) + "\n" + actor_card("danmaku", "en", prices)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{HEAD_TAGS}
  <title>Bilibili Scraping Guides: Comments, Danmaku, UP主 &amp; API | Blog</title>
  <meta name="description" content="Guides to scraping Bilibili (哔哩哔哩, B站): comments with replies, danmaku bullet comments, UP主 creator data and the Bilibili API, with Python and no-code tools.">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Bilibili Scraping Guides">
  <meta property="og:description" content="Scrape Bilibili comments, danmaku and UP主 data without a login.">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/blog/{posts[0]['cover']}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{ld}
  </script>
{FONTS}
</head>
<body>
{BODY_TOP}

  <header class="hero post-hero" id="top">
    <div class="wrap">
      <p class="crumbs"><a href="/">Home</a> › Blog</p>
      <h1>Bilibili scraping guides</h1>
      <p>How to get Bilibili (哔哩哔哩, B站) comments, danmaku bullet comments, UP主 creator data and video stats, with Python or no code, and without a login.</p>
      <div class="index-cards">
{cards}
      </div>
    </div>
  </header>
  <main>
    <section>
      <div class="wrap">
        <div class="grid">
{items}
        </div>
      </div>
    </section>
  </main>
{FOOTER}
</body>
</html>
"""


def update_sitemap(posts):
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\s*<url><loc>[^<]*/blog/[^<]*</loc>.*?</url>", "", text)
    entries = [f"  <url><loc>{SITE}/blog/</loc><lastmod>{max(p['updated'] for p in posts)}</lastmod></url>"]
    entries += [f"  <url><loc>{SITE}/blog/{p['slug']}</loc><lastmod>{p['updated']}</lastmod></url>" for p in posts]
    text = text.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
    path.write_text(text, encoding="utf-8")


def add_referral(page):
    """Add the Apify referral ID to every link to our own Actors (hrefs only, not JSON-LD)."""
    def sub(m):
        url = m.group(1)
        if REFERRAL in url:
            return m.group(0)
        base, _, frag = url.partition("#")
        base += ("&" if "?" in base else "?") + REFERRAL
        return f'href="{base}#{frag}"' if frag else f'href="{base}"'
    return re.sub(r'href="(https://apify\.com/molded_mountainpass[^"]*)"', sub, page)


def main():
    prices = fetch_prices()
    posts = sorted((load(p, prices) for p in SRC.glob("*.md")), key=lambda p: (p["date"], p["lang"] != "en", p["slug"]))
    OUT.mkdir(exist_ok=True)
    for p in posts:
        (OUT / f"{p['slug']}.html").write_text(add_referral(render_post(p, posts, prices)), encoding="utf-8")
    (OUT / "index.html").write_text(add_referral(render_index(posts, prices)), encoding="utf-8")
    update_sitemap(posts)
    print(f"built {len(posts)} posts with prices {prices}")


if __name__ == "__main__":
    main()
