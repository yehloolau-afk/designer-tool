"""
每日 AI 精选 RSS 生成脚本
数据源：AI HOT API + 主流 AI 媒体 RSS
输出：feed.xml（托管于 GitHub Pages）
"""

import requests
import feedparser
import json
import os
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from xml.sax.saxutils import escape

SITE_URL = "https://yehloolau-afk.github.io/designer-tool/ai-station.html"
FEED_URL = "https://yehloolau-afk.github.io/designer-tool/feed.xml"
MAX_ITEMS = 20
TIMEOUT = 10

RSS_SOURCES = [
    ("OpenAI Blog",      "https://openai.com/blog/rss.xml"),
    ("Anthropic Blog",   "https://www.anthropic.com/rss.xml"),
    ("Google AI Blog",   "https://blog.research.google/feeds/posts/default?alt=rss"),
    ("The Verge AI",     "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"),
    ("MIT Tech Review",  "https://www.technologyreview.com/feed/"),
    ("量子位",            "https://www.qbitai.com/feed"),
    ("机器之心",          "https://www.jiqizhixin.com/rss"),
]


def fetch_aihot():
    """从 AI HOT API 拉取精选内容"""
    items = []
    try:
        r = requests.get(
            "https://aihot.virxact.com/api/public",
            params={"page": 1, "pageSize": 30},
            timeout=TIMEOUT
        )
        data = r.json()
        entries = data.get("data", data) if isinstance(data, dict) else data
        if isinstance(entries, list):
            for e in entries[:15]:
                title = e.get("title") or e.get("name", "")
                link  = e.get("url") or e.get("link", "")
                desc  = e.get("description") or e.get("summary", "")
                pub   = e.get("publishedAt") or e.get("created_at", "")
                if title and link:
                    items.append({
                        "title": title,
                        "link": link,
                        "description": desc,
                        "pubDate": parse_date(pub),
                        "source": "AI HOT 精选"
                    })
    except Exception as ex:
        print(f"AI HOT API error: {ex}")
    return items


def fetch_rss(name, url):
    """拉取单个 RSS 源"""
    items = []
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "Mozilla/5.0"})
        for e in feed.entries[:5]:
            title = e.get("title", "")
            link  = e.get("link", "")
            desc  = e.get("summary", "")[:300]
            pub   = e.get("published", e.get("updated", ""))
            if title and link:
                items.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "pubDate": parse_date(pub),
                    "source": name
                })
    except Exception as ex:
        print(f"RSS error [{name}]: {ex}")
    return items


def parse_date(raw):
    """将各种日期格式统一为 RFC 822"""
    if not raw:
        return format_datetime(datetime.now(timezone.utc))
    try:
        from dateutil import parser as dp
        dt = dp.parse(str(raw))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return format_datetime(dt)
    except Exception:
        return format_datetime(datetime.now(timezone.utc))


def dedupe(items):
    """按链接去重"""
    seen = set()
    out = []
    for item in items:
        key = item["link"]
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def build_rss(items):
    now_str = format_datetime(datetime.now(timezone.utc))
    rows = []
    for item in items:
        rows.append(f"""    <item>
      <title>{escape(item['title'])}</title>
      <link>{escape(item['link'])}</link>
      <description>{escape(item['description'])}</description>
      <pubDate>{item['pubDate']}</pubDate>
      <guid isPermaLink="true">{escape(item['link'])}</guid>
      <source url="{escape(item['link'])}">{escape(item['source'])}</source>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>飞翔的AI资讯站 · 每日精选</title>
    <link>{SITE_URL}</link>
    <description>每日精选 AI 行业最值得关注的动态——模型更新、产品发布、设计趋势</description>
    <language>zh-CN</language>
    <lastBuildDate>{now_str}</lastBuildDate>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
{chr(10).join(rows)}
  </channel>
</rss>"""


def main():
    print("开始拉取数据源...")
    all_items = []

    # AI HOT 精选优先
    aihot = fetch_aihot()
    print(f"AI HOT: {len(aihot)} 条")
    all_items.extend(aihot)

    # RSS 源
    for name, url in RSS_SOURCES:
        items = fetch_rss(name, url)
        print(f"{name}: {len(items)} 条")
        all_items.extend(items)

    # 去重 + 截取
    all_items = dedupe(all_items)[:MAX_ITEMS]
    print(f"最终入选: {len(all_items)} 条")

    xml = build_rss(all_items)

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "feed.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"feed.xml 已写入: {out_path}")


if __name__ == "__main__":
    main()
