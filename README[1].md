# 繁體中文 Emoji 搜尋引擎 (Traditional Chinese Emoji Search Engine)

Search emoji by meaning, tone, or emotion in Traditional Chinese — not just
literal keyword names. Built to showcase how a linguistics background can
shape a genuinely useful search experience: querying "無語" (speechless/done
with this) correctly surfaces 🙄😑💀 even though none of those have "無語" as
their "official" name anywhere.

## Why this is different from existing emoji pickers

Most emoji search (including the built-in OS ones) matches literal English
names ("face with rolling eyes"). This project is built around **how people
actually use emoji in Traditional Chinese** — tone, sarcasm, internet slang
(e.g. 💀 = "笑死" / dying laughing, not literally "skull") — which is exactly
the kind of nuance a linguist notices and a keyword-matcher misses.

## Setup

```
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## How it works

- **`data/emoji_zh.json`** — a hand-curated dataset of ~150 commonly used
  emoji, each tagged with Traditional Chinese keywords covering literal
  meaning AND real conversational usage (slang, tone, sarcasm).
- **`search.py`** — the scoring/ranking logic. Uses `jieba` (Chinese word
  segmentation) when available for smarter partial matches, with a
  character-bigram fallback so it still works without it. No API calls,
  no external dependencies beyond the two in `requirements.txt`.
- **`app.py`** — the Streamlit UI: a search box plus a "browse by category"
  view when there's no query yet.

## Try these queries

| Query | What it should surface |
|---|---|
| 開心 | 😀 😊 💃 |
| 笑死 | 💀 ☠️ |
| 無奈 | 🙃 😓 |
| 拜託 | 🥺 🙏 |
| 好熱 | 🥵 |
| 生日快樂 | 🎂 🎉 🎈 |

## Known limitations / next steps

- The dataset is hand-curated (~150 emoji), not the full Unicode set (~3,700+
  emoji exist). This was a deliberate scope choice to keep quality high for
  a portfolio piece — expanding coverage is the natural next step.
- Matching is keyword/token-overlap based, not true semantic search. A
  natural upgrade: embed each keyword set with a multilingual sentence
  embedding model and do vector similarity search, so queries that share no
  words with any keyword (but mean something similar) still match.
- Could add: usage examples per emoji, platform-rendering differences (Apple
  vs. Android), or letting users submit/upvote keyword suggestions to grow
  the dataset over time.

## Tech notes for reviewers

This project deliberately avoids requiring any paid API or rate-limited
service — it runs fully offline once installed, which makes it easy for
anyone to clone and try immediately.
