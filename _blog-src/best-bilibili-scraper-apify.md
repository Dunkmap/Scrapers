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
  "faq": [
    ["What is the best Bilibili scraper on Apify?", "It depends on the job. For comments, danmaku, UP主 profiles and subtitles in one tool, with sentiment and an open-source version you can self-host for free, the Bilibili Scraper by molded_mountainpass covers the most. For the lowest price per danmaku or per comment, a single-purpose scraper can be cheaper."],
    ["What is the cheapest Bilibili danmaku scraper?", "On 9 Nov 2026, the cheapest per-danmaku price on the Apify Store was $0.00002 per danmaku (blueskyscraper/bilibili-danmaku-scraper). Prices change, so check the Store page before a large run."],
    ["What is the cheapest Bilibili comments scraper?", "On 9 Nov 2026, single-purpose comment scrapers started at about $3 per 1,000 comments. Self-hosting the open-source Bilibili Scraper is free."],
    ["Is there a free Bilibili scraper?", "Yes. The Bilibili Scraper is open source (MIT), so you can run it on your own machine for free. On Apify, a free account also includes monthly credit."],
    ["Do Bilibili scrapers need a login?", "Most don't for comments, danmaku, videos and creator profiles. Subtitles usually need a login cookie."]
  ]
}
-->
There are dozens of Bilibili (哔哩哔哩, B站) scrapers on the Apify Store, and their prices differ by **nearly 1,000×** for the same data. I compared 8 of the most-used ones by what they cost and what they return, so you can pick the right one for your job.

**Disclosure:** I built two of them, the [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper) and the [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper). I've tried to be fair: where another scraper is cheaper or more popular, the tables say so.

**How I compared:** prices and descriptions come from each Actor's public Apify Store page on **9 Nov 2026**, on the free plan. Features are what each Actor's own description lists ("–" means not listed, not necessarily missing). Prices change, so check the Store page before a big run.

## Quick answer: which Bilibili scraper should you use?

| If you need… | Best pick | Why |
|---|---|---|
| **Comments + danmaku + UP主 + subtitles in one tool** | [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper) | One Actor for every data type, with reply threads, sentiment and delta mode |
| **To run it free on your own machine** | [Bilibili Scraper](https://github.com/Dunkmap/Bilibili-Scraper) (open source) | MIT-licensed Python library and CLI; none of the others list an open-source version |
| **Danmaku with highlights, filtered by keyword** | [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper) | Merges both danmaku sources, keyword filter before charging, free per-video highlight summaries |
| **The cheapest raw danmaku** | blueskyscraper/bilibili-danmaku-scraper | $0.00002 per danmaku |
| **The cheapest comments only** | socialdatax or hgservices comment scrapers | About $3 per 1,000 comments |
| **The most popular, battle-tested option** | zhorex/bilibili-scraper | 7,600+ users |

## Price comparison: 1,000 comments

| Scraper (Apify) | Price per 1,000 comments | Reply threads |
|---|---|---|
| socialdatax/socialdatax-bilibili-data-api | ~$2.99 | Yes (listed) |
| hgservices/BilBili-Comments-Scraper | ~$3.00 | Yes (listed) |
| lofomachines/bilibili-scraper | ~$4.50 | – |
| **molded_mountainpass/bilibili-scraper** | **$5.00** | **Yes, full nested threads, 23 fields per comment** |
| sian.agency/bilibili-video-scraper | ~$12.00 | – |
| zhorex/bilibili-scraper | ~$20.00 | Yes ("comment threads") |

Our Bilibili Scraper isn't the cheapest for comments alone. What you get for the price: 23 fields per comment (pinned, VIP, verified, liked by uploader, IP location, reply count…), and in a side-by-side test on 26 Oct 2026 its video stats and top 20 comments matched Bilibili exactly.

## Price comparison: 1,000 danmaku (bullet comments)

| Scraper (Apify) | Price per 1,000 danmaku | Notes |
|---|---|---|
| blueskyscraper/bilibili-danmaku-scraper | ~$0.02 | Cheapest per danmaku (may also charge per video) |
| zen-studio/bilibili-danmaku-scraper | ~$0.15 | Plus ~$0.01 per video |
| **molded_mountainpass/bilibili-danmaku-scraper** | **$1.00** | **Keyword filter before charging, free per-video summary rows** |
| **molded_mountainpass/bilibili-scraper** | **$1.00** | Same price inside the all-in-one scraper |
| sian.agency/bilibili-video-scraper | ~$6.00 | |
| xtracto/bilibili-danmaku | ~$19.00 | |

If you only want every raw danmaku as cheaply as possible, a single-purpose danmaku Actor wins on price. Ours is built for **analysis**: the keyword filter runs before charging, so if you only want danmaku that mention a brand you pay only for those, and the free summary row gives each video's busiest moment (`peak_time`) and top phrases without paying for a single danmaku.

## Feature comparison

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

## Why the danmaku source matters

Logged out, Bilibili serves danmaku from **two endpoints**: protobuf segments give a sample over the video's lifetime, and the XML endpoint gives the most recent few thousand. They barely overlap. A scraper that reads only one of them misses many of the danmaku the other one returns. Ours merges both (`danmakuSource: both`). On a 34-minute video that gave 5,416 rows without a login.

New to danmaku? See [What is danmaku?](/blog/what-is-danmaku).

## Why open source matters

Every scraper here runs as a hosted service. Only one of them, as far as their Store pages show, is also open source. The [Bilibili Scraper](https://github.com/Dunkmap/Bilibili-Scraper) is also an MIT-licensed Python library and CLI. You can:

- **run it free** on your own machine or server;
- **read the code** to see exactly how it signs requests (`w_rid` / WBI) and handles risk control;
- **switch to Apify** when you want scheduling, proxies and exports without managing anything.

See [how to scrape Bilibili comments in Python](/blog/scrape-bilibili-comments-python) and [how the Bilibili API works](/blog/bilibili-api).

## The verdict

- **Pick the [Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper)** if you want comments with replies, danmaku, UP主 profiles and subtitles from one tool, with sentiment and delta mode, and the option to self-host for free.
- **Pick the [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper)** if you analyse danmaku: highlights, keyword mentions or reaction over time.
- **Pick a single-purpose scraper** if you need the lowest possible price for one data type and nothing else.
