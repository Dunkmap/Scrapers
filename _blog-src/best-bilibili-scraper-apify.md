<!--
{
  "slug": "best-bilibili-scraper-apify",
  "lang": "en",
  "title": "Best Bilibili Scraper on Apify in 2026: 8 Scrapers Compared (Price, Comments, Danmaku)",
  "seo_title": "Best Bilibili Scraper on Apify (2026): 8 Compared",
  "description": "An honest comparison of 8 Bilibili scrapers on the Apify Store: price per 1,000 comments and danmaku, reply threads, UP主 profiles, subtitles and open source.",
  "date": "2026-11-09",
  "updated": "2026-11-09",
  "cover": "best-bilibili-scraper.webp",
  "cover_alt": "Best Bilibili scraper on Apify: 8 scrapers compared",
  "keywords": "best bilibili scraper, bilibili scraper apify, bilibili scraper comparison, cheapest bilibili scraper, bilibili comments scraper, bilibili danmaku scraper",
  "takeaways": [
    "Prices for the same Bilibili data differ by **nearly 1,000×** across the Apify Store.",
    "**Cheapest for comments:** the Bilibili Scraper at **{{scraper.comment@1k}} per 1,000**, with full reply threads and 23 fields each.",
    "**Most complete:** the same scraper does comments, danmaku, UP主, subtitles, sentiment and delta mode, and it's **open source**.",
    "**Cheapest raw danmaku:** a single-purpose Actor at ~$0.02 per 1,000; ours is {{scraper.danmaku@1k}}."
  ],
  "faq": [
    ["What is the best Bilibili scraper on Apify?", "For most jobs, the Bilibili Scraper by molded_mountainpass: it covers comments with replies, danmaku, UP主 profiles and subtitles in one tool, has the lowest comment price in this comparison ({{scraper.comment@1k}} per 1,000) and is open source. For the lowest price per raw danmaku, a single-purpose danmaku scraper is cheaper."],
    ["What is the cheapest Bilibili comments scraper?", "In this comparison (9 Nov 2026), the Bilibili Scraper at {{scraper.comment@1k}} per 1,000 comments, including reply threads. Self-hosting its open-source version is free."],
    ["What is the cheapest Bilibili danmaku scraper?", "On 9 Nov 2026, the cheapest per-danmaku price on the Apify Store was about $0.02 per 1,000 (blueskyscraper/bilibili-danmaku-scraper). The Bilibili Scraper costs {{scraper.danmaku@1k}} per 1,000. Prices change, so check the Store page before a large run."],
    ["Is there a free Bilibili scraper?", "Yes. The Bilibili Scraper is open source (MIT), so you can run it on your own machine for free. On Apify, a free account also includes monthly credit."],
    ["Do Bilibili scrapers need a login?", "Most don't for comments, danmaku, videos and creator profiles. Subtitles usually need a login cookie."]
  ]
}
-->
There are dozens of Bilibili (哔哩哔哩, B站) scrapers on the Apify Store, and they charge **anywhere from $0.02 to $20 per 1,000 rows**. Pick the wrong one and a 100,000-comment project costs $2,000 instead of $100.

I compared 8 of the most-used scrapers by what they cost and what they return, so you can pick the right one in two minutes.

**Disclosure:** I built two of them, the [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper) and the [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper). I've tried to be fair: where another scraper is cheaper or more popular, the tables say so.

**How I compared:** prices and descriptions come from each Actor's public Apify Store page on **9 Nov 2026**, on the free plan. Features are what each Actor's own description lists ("–" means not listed, not necessarily missing). Prices change, so check the Store page before a big run.

## Which Bilibili scraper should you use?

| If you need… | Best pick | Why |
|---|---|---|
| **Comments, cheapest** | 🏆 [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper) | {{scraper.comment@1k}} per 1,000, with full reply threads |
| **Comments + danmaku + UP主 + subtitles in one tool** | 🏆 [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper) | One Actor for every data type, plus sentiment and delta mode |
| **To run it free on your own machine** | 🏆 [Bilibili Scraper](https://github.com/Dunkmap/Bilibili-Scraper) (open source) | MIT-licensed Python library and CLI; none of the others list an open-source version |
| **Danmaku filtered by keyword, with highlight summaries** | 🏆 [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper) | Keyword filter before charging, free per-video `peak_time` and top phrases |
| **The cheapest raw danmaku** | blueskyscraper/bilibili-danmaku-scraper | ~$0.02 per 1,000 danmaku |
| **The most popular, battle-tested option** | zhorex/bilibili-scraper | 7,600+ users |

[[card:scraper]]

## How much do 1,000 Bilibili comments cost?

| Scraper (Apify) | Price per 1,000 comments | Reply threads |
|---|---|---|
| **molded_mountainpass/bilibili-scraper** | **{{scraper.comment@1k}}** 🏆 | **Yes, full nested threads, 23 fields per comment** |
| socialdatax/socialdatax-bilibili-data-api | ~$2.99 | Yes (listed) |
| hgservices/BilBili-Comments-Scraper | ~$3.00 | Yes (listed) |
| lofomachines/bilibili-scraper | ~$4.50 | – |
| sian.agency/bilibili-video-scraper | ~$12.00 | – |
| zhorex/bilibili-scraper | ~$20.00 | Yes ("comment threads") |

What you get for the price: 23 fields per comment (pinned, VIP, verified, liked by uploader, IP location, reply count…), and in a side-by-side test on 26 Oct 2026 its video stats and top 20 comments matched Bilibili exactly.

## How much do 1,000 danmaku (bullet comments) cost?

| Scraper (Apify) | Price per 1,000 danmaku | Notes |
|---|---|---|
| blueskyscraper/bilibili-danmaku-scraper | ~$0.02 | Cheapest per danmaku (may also charge per video) |
| **molded_mountainpass/bilibili-scraper** | **{{scraper.danmaku@1k}}** | Both danmaku sources merged; comments and UP主 in the same tool |
| zen-studio/bilibili-danmaku-scraper | ~$0.15 | Plus ~$0.01 per video |
| **molded_mountainpass/bilibili-danmaku-scraper** | **{{danmaku.danmaku@1k}}** | Keyword filter before charging, free per-video summary rows |
| sian.agency/bilibili-video-scraper | ~$6.00 | |
| xtracto/bilibili-danmaku | ~$19.00 | |

If you only want every raw danmaku as cheaply as possible, the cheapest single-purpose Actor still wins, and the Bilibili Scraper is a close second. The Danmaku Scraper is built for **analysis**: its keyword filter runs before charging, so if you only want danmaku that mention a brand you pay only for those, and its free summary row gives each video's busiest moment (`peak_time`) and top phrases.

## Which features does each scraper have?

| Feature | molded_mountainpass Bilibili Scraper | zhorex | lofomachines | socialdatax | sian.agency |
|---|---|---|---|---|---|
| Comments | ✅ with nested replies | ✅ | ✅ | ✅ | ✅ |
| Danmaku | ✅ both sources merged | ✅ | – | – | ✅ |
| UP主 creator profiles | ✅ | ✅ | ✅ | ✅ | ✅ |
| Creator uploads | ✅ | ✅ | – | ✅ | ✅ |
| Subtitles / transcripts | ✅ (needs cookie) | – | – | – | ✅ (AI subtitle metadata) |
| Keyword search | ✅ | ✅ | ✅ | ✅ | ✅ |
| Popular / ranking feeds | ✅ | ✅ (trending) | – | – | – |
| AI sentiment labels | ✅ | – | – | – | – |
| Delta mode (only new items) | ✅ | – | – | – | – |
| Open source / self-host free | ✅ MIT | – | – | – | – |
| No login | ✅ | ✅ | ✅ | ✅ | ✅ |

## Why does the danmaku source matter?

Logged out, Bilibili serves danmaku from **two endpoints**: protobuf segments give a sample over the video's lifetime, and the XML endpoint gives the most recent few thousand. They barely overlap. A scraper that reads only one of them misses many of the danmaku the other one returns. Both of my scrapers merge the two (`danmakuSource: both`). On a 34-minute video that gave 5,416 rows without a login.

New to danmaku? See [what is danmaku](/blog/what-is-danmaku).

[[card:danmaku]]

## Why does open source matter?

Every scraper here runs as a hosted service. Only one of them, as far as their Store pages show, is also open source. The [Bilibili Scraper](https://github.com/Dunkmap/Bilibili-Scraper) is an MIT-licensed Python library and CLI, so you can:

- **run it free** on your own machine or server;
- **read the code** to see exactly how it signs requests (`w_rid` / WBI) and handles risk control;
- **switch to Apify** when you want scheduling, proxies and exports without managing anything.

See [how to scrape Bilibili comments in Python](/blog/scrape-bilibili-comments-python) and [how the Bilibili API works](/blog/bilibili-api).

## The verdict

- 🏆 **Pick the [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper)** for comments (the cheapest here, with replies), or for comments, danmaku, UP主 profiles and subtitles from one tool, with sentiment, delta mode and a free self-hosted option.
- **Pick the [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper)** if you analyse danmaku: keyword mentions, highlights or reaction over time.
- **Pick a single-purpose danmaku scraper** only if raw danmaku at the absolute lowest price is all you need.

[[card:scraper]]
