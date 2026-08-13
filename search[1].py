# -*- coding: utf-8 -*-
"""
Traditional Chinese Emoji Search Engine — core search logic
--------------------------------------------------------------
Loads the hand-curated zh-Hant emoji keyword dataset and scores emoji
against a free-text Traditional Chinese query.

Scoring strategy (works without needing a full Chinese word segmenter,
though it uses jieba when available for better partial-word matching):

  1. Exact keyword match            -> highest score
  2. Query is substring of a keyword, or keyword is substring of query
                                     -> high score
  3. jieba-tokenized query/keyword overlap
                                     -> medium score
  4. Character-level overlap (for short queries / single characters)
                                     -> low score, tie-breaker

Results are ranked by total score, descending.
"""

import json
import os
from collections import defaultdict

try:
    import jieba
    _HAS_JIEBA = True
except ImportError:
    _HAS_JIEBA = False

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "emoji_zh.json")


def load_dataset(path: str = DATA_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _tokenize(text: str) -> set[str]:
    """Tokenize Traditional Chinese text into a set of tokens for overlap scoring."""
    if _HAS_JIEBA:
        return {t for t in jieba.cut(text) if t.strip()}
    # Fallback: character bigrams, which approximates word-level matching
    # reasonably well for short Chinese search queries without a segmenter.
    text = text.strip()
    if len(text) <= 1:
        return {text} if text else set()
    return {text[i:i + 2] for i in range(len(text) - 1)}


def score_entry(query: str, keywords: list[str]) -> float:
    query = query.strip()
    if not query:
        return 0.0

    best = 0.0
    query_tokens = _tokenize(query)

    for kw in keywords:
        if query == kw:
            return 100.0  # exact match short-circuits, can't do better
        if query in kw or kw in query:
            best = max(best, 60.0)
            continue

        kw_tokens = _tokenize(kw)
        overlap = query_tokens & kw_tokens
        if overlap:
            # score proportional to how much of the shorter token set matched
            ratio = len(overlap) / max(1, min(len(query_tokens), len(kw_tokens)))
            best = max(best, 20.0 + 20.0 * ratio)

    return best


def search(query: str, dataset: list[dict] | None = None, top_n: int = 12) -> list[dict]:
    """Search the emoji dataset for a Traditional Chinese query string.

    Returns a list of dicts: {emoji, category, keywords, matched_keyword, score}
    sorted by score descending. Entries with score 0 are excluded.
    """
    if dataset is None:
        dataset = load_dataset()

    results = []
    for entry in dataset:
        s = score_entry(query, entry["keywords"])
        if s > 0:
            # find the single best-matching keyword to show the user why it matched
            matched_kw = max(
                entry["keywords"],
                key=lambda kw: score_entry(query, [kw]),
            )
            results.append(
                {
                    "emoji": entry["emoji"],
                    "category": entry["category"],
                    "keywords": entry["keywords"],
                    "matched_keyword": matched_kw,
                    "score": s,
                }
            )

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_n]


if __name__ == "__main__":
    # Quick manual test from the command line:
    #   python search.py 開心
    import sys

    q = " ".join(sys.argv[1:]) or "開心"
    ds = load_dataset()
    print(f"Query: {q!r}  (jieba available: {_HAS_JIEBA})\n")
    for r in search(q, ds):
        print(f"  {r['emoji']}  score={r['score']:.0f}  matched='{r['matched_keyword']}'  all={r['keywords']}")
