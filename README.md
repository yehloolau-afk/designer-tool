# designer-tool

Two single-file tools for designers. No backend, no framework, no build step.

---

## 🗞️ AI News Station

**Live →** [yehloolau-afk.github.io/designer-tool/ai-station.html](https://yehloolau-afk.github.io/designer-tool/ai-station.html)

A 7-channel AI news aggregator built for design teams. Pulls from 20+ Chinese and English sources, auto-translates, and updates hourly via GitHub Actions.

**Channels:** 精选 · 全部 · 官方动态 · 产品发布 · 设计 · 视频 · 日报

**Sources include:** 量子位 · 爱范儿 · 极客公园 · 少数派 · The Verge · TechCrunch · OpenAI · Anthropic · and more.

Built for my team at DiDi. Now open to everyone.

---

## 🎨 Wanhuatong · 万花筒

**Live →** [yehloolau-afk.github.io/designer-tool](https://yehloolau-afk.github.io/designer-tool/)

A text-to-video automation pipeline for Chinese elementary school language lessons.

**Workflow:** Lesson text → storyboard → AI image generation → AI video generation → download assets

**Powered by:** Volcengine Seedream (image) · Volcengine Seedance (video) · Claude (storyboard parsing)

Bring your own API key. Everything runs in the browser.

---

## How it's built

- Single HTML files — one file per tool, open and use
- No server, no database, no login
- GitHub Actions generates static data files hourly (for AI 资讯站)
- Deployed on GitHub Pages + Netlify

`Claude Code` · `Vanilla HTML / CSS / JS` · `GitHub Actions`
