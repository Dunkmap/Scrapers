<!--
{
  "slug": "scrape-bilibili-comments-python",
  "lang": "en",
  "title": "How to Scrape Bilibili Comments, Danmaku and UP主 Data in Python (2026, No Login)",
  "seo_title": "Scrape Bilibili Comments, Danmaku & UP主 Data in Python (2026)",
  "description": "Download Bilibili comments with replies, danmaku bullet comments, video stats and UP主 creator profiles to Excel, CSV or JSON without a login. Python or no code.",
  "date": "2026-11-09",
  "updated": "2026-11-09",
  "cover": "bilibili-comments-scraper.webp",
  "cover_alt": "Scrape Bilibili comments, danmaku and UP主 data in Python",
  "keywords": "bilibili comments, scrape bilibili comments, bilibili scraper, bilibili danmaku, bilibili api python, UP主, export bilibili comments to excel",
  "faq": [
    ["Is there an official Bilibili API?", "No public one for comments or danmaku. This scraper uses the same web endpoints bilibili.com uses and handles their WBI signing for you."],
    ["Can I read Bilibili comments without an account?", "Yes. Comments, danmaku, videos, search, creators and trending all work logged out. Only subtitles need a login cookie."],
    ["How do I generate the w_rid parameter?", "You don't have to. The scraper signs every request itself with Bilibili's WBI keys."],
    ["Can I export Bilibili comments to Excel?", "Yes. On Apify, click Export and choose Excel. Locally, use -o comments.csv and open the file in Excel."],
    ["Is scraping Bilibili legal?", "It reads public data the same way the bilibili.com website does. Follow Bilibili's terms of service, keep the request rate reasonable and don't republish personal data."]
  ]
}
-->
Bilibili (哔哩哔哩, B站) is China's biggest video platform for anime, gaming, tech and lifestyle. Its comment sections and **danmaku** (弹幕, the bullet comments that fly across the video) are a goldmine for market research, sentiment analysis and influencer discovery.

The problem: Bilibili has **no official public API** for this data. Its web endpoints now need a **`w_rid` / `wts` signature (WBI signing)**, they throw silent risk-control errors (`-352`, `-412`) and they rate-limit you. Most tutorials from before 2023 use old unsigned endpoints and simply don't work anymore.

This guide shows two ways to get the data **without a Bilibili account**:

1. **No code:** a ready-made Bilibili scraper on Apify, with a 1-click export to Excel.
2. **Python:** the same open-source library, run locally.

## What you can scrape

| Data | What you get |
|---|---|
| **Comments** | Hot or newest first, with full nested reply threads. 23 fields per comment: user, likes, pinned, VIP, verified, "liked by uploader", IP location, reply count… |
| **Danmaku (bullet comments)** | Every bullet comment as its own row, with its playback time, colour, mode and send time |
| **Videos** | Views, likes, coins, favourites, shares, danmaku and reply counts, tags |
| **UP主 (creators)** | Name, bio, level, verified title, VIP, followers, following, video count, total likes |
| **Creator uploads** | Every video a creator uploaded, sorted by date, views or favourites |
| **Search & trending** | Keyword search (sort by views, date, danmaku…), the popular feed and the top-100 ranking |
| **Subtitles / transcripts** | Including AI captions. This is the one thing that needs a login cookie |

## Option 1: No code (Apify)

1. Open the **[Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper)** and click **Try for free**. A free Apify account includes monthly credit.
2. Pick **What to scrape**: `videos`, `comments`, `danmaku`, `subtitles` or `users`.
3. Give it a source: paste video links, `space.bilibili.com/...` creator links or search links, or just type keywords such as `原神`.
4. Click **Start**, then **Export** to Excel, CSV or JSON (or send it straight to Google Sheets).

Example: the comments, with replies, on the top 20 search results for a keyword:

```json
{
  "mode": "comments",
  "searchQueries": ["原神"],
  "maxVideosPerSource": 20,
  "maxCommentsPerVideo": 200,
  "includeReplies": true
}
```

### Scraping UP主 (creator) profiles

Set `mode` to `users` and pass creator IDs (the number in `space.bilibili.com/<UID>`):

```json
{
  "mode": "users",
  "userIds": ["2", "546195"]
}
```

Each row has `name`, `sign` (bio), `level`, `verified`, `vip`, `followers`, `following`, `videos`, `likes` and the profile `url`. To get a creator's videos instead, use `mode: "videos"` with the same `userIds`.

**Pricing:** pay per result, no subscription. $0.005 per comment, video or creator profile and $0.001 per danmaku, so 1,000 comments cost about $5.

## Option 2: Python

The scraper is open source (MIT):

```bash
git clone https://github.com/Dunkmap/Bilibili-Scraper
cd Bilibili-Scraper
pip install -e .
```

From the command line:

```bash
bili comments BV1xx411c7mD --replies -o comments.csv
bili danmaku BV1xx411c7mD -o danmaku.csv
bili user 2                                   # UP主 profile
bili uploads 2 --order click --limit 100 -o uploads.csv
bili search "原神" --order click --limit 200 -o search.csv
```

Or as a library:

```python
import asyncio
from bilibili_scraper import Scraper

async def main():
    async with Scraper(rate=4) as s:
        video = await s.video("BV1xx411c7mD")
        async for c in s.comments(video["bvid"], limit=500, replies=True):
            print(c["uname"], c["content"])

        creator = await s.user(video["owner_mid"])
        print(creator["name"], creator["followers"])

        async for v in s.user_videos(video["owner_mid"], order="click", limit=20):
            print(v["title"], v["views"])

asyncio.run(main())
```

## How it handles w_rid signing and risk control

- **WBI signing:** fetches `img_key` / `sub_key`, generates `w_rid` and `wts`, caches the keys and refreshes them when Bilibili rejects a signature (`-352`).
- **Silent risk control:** Bilibili sometimes answers `code: 0` with only a `v_voucher` and no data. The scraper detects this and retries instead of treating it as an empty page.
- **Device cookies:** generates a `buvid` itself, so no account is needed.
- **Rate limits:** jittered delays and backoff retries on `-412`. The cloud version also switches to a proxy when it gets blocked.

## Extras

- **Sentiment analysis:** label every comment and danmaku positive, neutral or negative, using your own free Groq API key.
- **Delta mode:** scheduled runs return only items that are new since the last run, which is handy for brand monitoring.
- **Danmaku-only version:** if you only need bullet comments, the [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper) adds a keyword filter and a free per-video highlight timeline.
