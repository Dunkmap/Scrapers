<!--
{
  "slug": "bilibili-comments-scraper-zh",
  "lang": "zh-CN",
  "title": "2026 B站评论爬虫：Python 无需登录采集评论、弹幕、UP主数据（自动处理 w_rid 签名，一键导出 Excel）",
  "seo_title": "2026 B站评论爬虫：无需登录采集评论、弹幕、UP主数据",
  "description": "2026 最新 B站评论爬虫，自动处理 w_rid 签名和风控，无需登录采集 B站评论、弹幕、UP主 数据，一键导出 Excel / CSV / JSON。开源 Python + 免代码两种用法。",
  "date": "2026-11-09",
  "updated": "2026-11-09",
  "cover": "bilibili-comments-scraper-zh.webp",
  "cover_alt": "B站评论爬虫：评论、弹幕、UP主数据",
  "keywords": "B站爬虫, B站评论爬取, B站弹幕下载, UP主数据采集, w_rid, WBI 签名, 哔哩哔哩爬虫, Python 爬虫",
  "faq": [
    [
      "B站 评论爬虫需要登录或 Cookie 吗？",
      "不需要，只有字幕需要 Cookie。"
    ],
    [
      "w_rid 参数怎么生成？",
      "它来自 B站 的 WBI 签名，本项目已经内置，不用自己算。"
    ],
    [
      "能导出 Excel 吗？",
      "可以。Apify 上点 Export → Excel；本地用 -o xxx.csv。"
    ],
    [
      "能采集 UP主 粉丝数吗？",
      "可以，用 users 模式，每个 UP主 一行。"
    ],
    [
      "合规吗？",
      "只读取公开数据，和 bilibili.com 网页本身调用的接口一致。请遵守 B站 用户协议，控制请求频率，不要传播个人信息。"
    ]
  ]
}
-->
做舆情分析、竞品调研、找 UP主 合作，最常见的需求就是批量拿到 **B站评论、弹幕和 UP主 数据**。但很多人照着网上的旧教程写爬虫，很快就会遇到这些问题：

- 评论接口多了 `w_rid` 和 `wts` 参数，不知道怎么生成；
- 请求返回 `-352`、`-412`，或者返回 `code: 0` 却没有数据（隐性风控）；
- 必须带 Cookie 才能用，账号还容易被限制。

原因是 B站 现在的网页接口使用 **WBI 签名**，并且加了风控和频率限制。2022 年以前的教程大多用的是不带签名的老接口，现在基本已经失效。

本文介绍一个开源项目 **Bilibili Scraper**，已经把这些问题处理好了，两种用法：

1. **免代码**：在 Apify 云端运行，一键导出 Excel / CSV / JSON；
2. **Python**：本地安装，命令行或代码调用。

全程 **不需要登录 B站 账号，也不需要 Cookie**（只有字幕需要）。

- 👉 在线使用（免代码）：https://apify.com/molded_mountainpass/bilibili-scraper
- 👉 只要弹幕：https://apify.com/molded_mountainpass/bilibili-danmaku-scraper
- 👉 开源代码（MIT）：https://github.com/Dunkmap/Bilibili-Scraper

## 一、能采集哪些数据

| 数据 | 内容 |
|---|---|
| **B站评论** | 热门 / 最新排序，含楼中楼回复。每条 23 个字段：用户、点赞、置顶、大会员、认证、UP主点赞、IP 属地、回复数等 |
| **B站弹幕** | 每条弹幕一行，含出现时间（视频第几秒）、颜色、模式、发送时间 |
| **视频数据** | 播放、点赞、投币、收藏、分享、弹幕数、评论数、标签 |
| **UP主 信息** | 昵称、签名、等级、认证、大会员、粉丝数、关注数、视频数、获赞数 |
| **UP主 投稿** | 某个 UP主 的全部投稿，可按发布时间、播放量、收藏排序 |
| **搜索 / 热门** | 关键词搜索（按播放、时间、弹幕等排序）、热门推荐、排行榜前 100 |
| **字幕** | 含 AI 字幕，**需要登录 Cookie** |

## 二、免代码用法（Apify 云端，一键导出 Excel）

1. 打开 **[Bilibili Scraper](https://apify.com/molded_mountainpass/bilibili-scraper)**，点击 **Try for free**（免费账号每月有赠送额度）；
2. 选择 **What to scrape**：`videos`（视频）、`comments`（评论）、`danmaku`（弹幕）、`subtitles`（字幕）、`users`（UP主）；
3. 填入视频链接、UP主 空间链接（`space.bilibili.com/...`）、搜索链接，或者直接输入关键词，如 `原神`；
4. 点击 **Start**，完成后 **Export** 导出 Excel / CSV / JSON，也可以直接同步到 Google Sheets。

示例：采集关键词「原神」搜索结果前 20 个视频的评论（含楼中楼回复）：

```json
{
  "mode": "comments",
  "searchQueries": ["原神"],
  "maxVideosPerSource": 20,
  "maxCommentsPerVideo": 200,
  "includeReplies": true
}
```

### 采集 UP主 信息

把 `mode` 设为 `users`，填入 UP主 UID（`space.bilibili.com/` 后面的数字）：

```json
{
  "mode": "users",
  "userIds": ["2", "546195"]
}
```

输出字段：`name`（昵称）、`sign`（签名）、`level`（等级）、`verified`（认证）、`vip`、`followers`（粉丝数）、`following`（关注数）、`videos`（视频数）、`likes`（获赞数）、`url`。想要 UP主 的投稿列表，用 `mode: "videos"` 加同样的 `userIds` 即可。

**价格**：按结果计费，无月费。评论 / 视频 / UP主 每条 $0.005，弹幕每条 $0.001，1000 条评论约 $5。

## 三、Python 用法

```bash
git clone https://github.com/Dunkmap/Bilibili-Scraper
cd Bilibili-Scraper
pip install -e .
```

命令行：

```bash
bili comments BV1xx411c7mD --replies -o comments.csv     # 评论 + 楼中楼
bili danmaku BV1xx411c7mD -o danmaku.csv                 # 弹幕
bili user 2                                              # UP主 信息
bili uploads 2 --order click --limit 100 -o uploads.csv  # UP主 投稿
bili search "原神" --order click --limit 200 -o search.csv
```

代码调用：

```python
import asyncio
from bilibili_scraper import Scraper

async def main():
    async with Scraper(rate=4) as s:
        video = await s.video("BV1xx411c7mD")
        async for c in s.comments(video["bvid"], limit=500, replies=True):
            print(c["uname"], c["content"])

        up = await s.user(video["owner_mid"])
        print(up["name"], up["followers"])

        async for v in s.user_videos(video["owner_mid"], order="click", limit=20):
            print(v["title"], v["views"])

asyncio.run(main())
```

## 四、它是怎么解决 w_rid 签名和风控的

- **WBI 签名**：自动获取 `img_key` / `sub_key`，生成 `w_rid` 和 `wts`；密钥会缓存，签名被拒（`-352`）时自动刷新；
- **隐性风控识别**：B站 有时返回 `code: 0` 但只有 `v_voucher` 没有数据，脚本会识别并重试，而不是当成空页面；
- **设备 Cookie**：自动生成 `buvid`，不需要登录账号；
- **限速与重试**：请求加随机间隔，遇到 `-412` 自动退避重试；云端版本被拦截时会逐级切换代理。

## 五、其他功能

- **情感分析**：用你自己的 Groq API Key（有免费额度），把每条评论 / 弹幕标注为正面、中性、负面；
- **增量模式**：定时任务只返回上次之后的新数据，适合长期舆情监控；
- **弹幕专用版**：只需要弹幕的话，可以用 [Bilibili Danmaku Scraper](https://apify.com/molded_mountainpass/bilibili-danmaku-scraper)，支持关键词过滤和免费的弹幕密度 / 高能时刻分析。
