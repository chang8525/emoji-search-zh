# -*- coding: utf-8 -*-
"""
Traditional Chinese Emoji Search Engine — Streamlit UI

Run:  streamlit run app.py
"""

import streamlit as st
from search import load_dataset, search

st.set_page_config(page_title="繁中 Emoji 搜尋引擎", page_icon="🔎", layout="centered")

st.title("🔎 繁體中文 Emoji 搜尋引擎")
st.caption("輸入中文詞彙、情緒或語氣，找到最適合的表情符號")

dataset = load_dataset()

query = st.text_input(
    "想表達什麼？",
    placeholder="例如：開心、生氣、笑死、無奈、生日快樂...",
)

with st.sidebar:
    st.header("關於這個工具")
    st.write(
        "這是一個以**語氣與情境**為核心的繁中 emoji 搜尋引擎，"
        "而不只是照字面比對 emoji 官方名稱。"
    )
    st.write(f"目前資料庫收錄 **{len(dataset)}** 個表情符號。")
    st.write("---")
    st.write("💡 試試看語氣詞，例如「無語」「笑死」「拜託」「好熱」")

if query:
    results = search(query, dataset, top_n=15)
    if not results:
        st.warning("找不到符合的 emoji，換個詞試試看？")
    else:
        st.write(f"找到 **{len(results)}** 個結果：")
        cols = st.columns(5)
        for i, r in enumerate(results):
            with cols[i % 5]:
                st.markdown(
                    f"<div style='text-align:center; font-size:48px'>{r['emoji']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align:center; font-size:12px; color:gray'>"
                    f"{r['matched_keyword']}</div>",
                    unsafe_allow_html=True,
                )
else:
    st.info("在上面輸入一個詞開始搜尋 👆")
    st.write("**分類瀏覽：**")
    categories = sorted({e["category"] for e in dataset})
    tabs = st.tabs(categories)
    for tab, cat in zip(tabs, categories):
        with tab:
            entries = [e for e in dataset if e["category"] == cat]
            cols = st.columns(6)
            for i, e in enumerate(entries):
                with cols[i % 6]:
                    st.markdown(
                        f"<div style='text-align:center; font-size:32px'>{e['emoji']}</div>",
                        unsafe_allow_html=True,
                    )
