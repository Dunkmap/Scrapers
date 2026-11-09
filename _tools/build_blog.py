"""Build /blog/ pages from _blog-src/*.md.

Each source starts with an HTML comment holding JSON front matter (slug, lang, title,
seo_title, description, date, updated, cover, cover_alt, keywords, faq), then Markdown.
Writes blog/<slug>.html, blog/index.html and refreshes the blog entries in sitemap.xml.

    pip install markdown
    python3 _tools/build_blog.py
"""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_blog-src"
OUT = ROOT / "blog"
SITE = "https://scrapers.practicemysql.com"
SCRAPER = "https://apify.com/molded_mountainpass/bilibili-scraper"
DANMAKU = "https://apify.com/molded_mountainpass/bilibili-danmaku-scraper"

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
  <link rel="stylesheet" href="/style.css">
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
      <p>© Divya Raj · <a href="/">scrapers.practicemysql.com</a> · <a href="mailto:divyarajvt752@gmail.com">divyarajvt752@gmail.com</a></p>
    </div>
  </footer>"""

AUTHOR = {"@type": "Person", "name": "Divya Raj", "url": SITE + "/"}

LABELS = {
    "en": {"home": "Home", "blog": "Blog", "updated": "Updated", "faq": "FAQ", "faq_h": "Frequently asked questions",
           "try": "Try the Bilibili Scraper", "danmaku": "Danmaku-only scraper", "more": "More Bilibili guides",
           "cta": "<strong>Want the data without writing code?</strong> The Bilibili Scraper exports comments, danmaku, videos and UP主 profiles to Excel, CSV or JSON. Pay per result, no login."},
    "zh-CN": {"home": "首页", "blog": "博客", "updated": "更新于", "faq": "常见问题", "faq_h": "常见问题",
              "try": "免费试用 Bilibili Scraper", "danmaku": "弹幕专用版", "more": "更多 B站 数据教程",
              "cta": "<strong>不想写代码？</strong> Bilibili Scraper 可一键导出 B站评论、弹幕、视频和 UP主 数据到 Excel / CSV / JSON，按结果计费，无需登录。"},
}


def load(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"<!--\s*(\{.*?\})\s*-->\s*", text, re.S)
    meta = json.loads(m.group(1))
    meta["body_md"] = text[m.end():]
    return meta


def esc(s):
    return html.escape(s, quote=True)


def render_post(p, posts):
    lab = LABELS[p["lang"]]
    url = f"{SITE}/blog/{p['slug']}"
    img = f"{SITE}/images/blog/{p['cover']}"
    body = markdown.markdown(p["body_md"], extensions=["tables", "fenced_code", "toc"])
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', body)
    graph = [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "image": img,
         "datePublished": p["date"], "dateModified": p["updated"], "inLanguage": p["lang"], "author": AUTHOR,
         "publisher": AUTHOR, "mainEntityOfPage": url, "keywords": p["keywords"],
         "about": [{"@type": "SoftwareApplication", "name": "Bilibili Scraper", "url": SCRAPER,
                    "applicationCategory": "BusinessApplication", "operatingSystem": "Web"}]},
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
      <h1>{esc(p['title'])}</h1>
      <p class="post-meta">Divya Raj · {lab['updated']} <time datetime="{p['updated']}">{p['updated']}</time></p>
      <div class="cta">
        <a class="btn big" href="{SCRAPER}">{lab['try']}</a>
        <a class="btn ghost" href="{DANMAKU}">{lab['danmaku']}</a>
      </div>
    </div>
  </header>
  <main>
    <section>
      <div class="wrap">
        <article class="post">
          <img class="post-cover" src="/images/blog/{p['cover']}" alt="{esc(p['cover_alt'])}" width="1000" height="420">
{body}
        </article>
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
</body>
</html>
"""


def render_index(posts):
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


def main():
    posts = sorted((load(p) for p in SRC.glob("*.md")), key=lambda p: (p["date"], p["lang"] != "en", p["slug"]))
    OUT.mkdir(exist_ok=True)
    for p in posts:
        (OUT / f"{p['slug']}.html").write_text(render_post(p, posts), encoding="utf-8")
    (OUT / "index.html").write_text(render_index(posts), encoding="utf-8")
    update_sitemap(posts)
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
