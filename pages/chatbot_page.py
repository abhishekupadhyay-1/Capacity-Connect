"""
pages/chatbot_page.py — Dataset-aware chatbot UI for Capacity Connect.
Clean, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.chatbot import process_query, EXAMPLE_QUESTIONS
from modules.ui_theme import render_html_table


def _init():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "bot",
            "type": "text",
            "content": (
                "**Capacity Connect Assistant** is ready.\n\n"
                "You can query workforce metrics, individual employee records, performance scores, "
                "or department rankings using natural language. Select an example query or enter your question below."
            ),
            "ts": datetime.now().strftime("%H:%M"),
        })
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None


def _bubble(msg: dict):
    ts = msg.get("ts", "")
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-user">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <span style="font-weight:600; color:var(--text-main); font-size:0.84rem;">You</span>
            <span style="font-size:0.72rem; color:var(--text-muted);">{ts}</span>
          </div>
          <div style="color:var(--text-main); font-size:0.88rem; line-height:1.5;">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        content = msg.get("content", "")
        ctype   = msg.get("type", "text")
        st.markdown(f"""
        <div class="chat-bot">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-weight:600; color:var(--text-main); font-size:0.84rem;">Assistant</span>
            <span style="font-size:0.72rem; color:var(--text-muted);">{ts}</span>
          </div>
          <div style="color:var(--text-main); font-size:0.88rem; line-height:1.5;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        if ctype == "table" and "data" in msg:
            df = msg["data"]
            if isinstance(df, pd.DataFrame) and not df.empty:
                render_html_table(df)
        elif ctype == "list" and "items" in msg:
            for item in msg["items"]:
                st.markdown(f"- {item}")


def show_chatbot():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("chatbot_page")

    _init()

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Data Assistant</div>
      <div class="page-header-sub">Dataset query interface connected in real-time to active employee and appraisal records</div>
    </div>
    """, unsafe_allow_html=True)

    chat_col, side_col = st.columns([3, 1])

    # ── Sidebar Panel ─────────────────────────────────────────────────────────
    with side_col:
        msg_count = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        st.markdown(f"""
        <div class="kpi-card" style="text-align:center; padding:12px; margin-bottom:12px;">
          <div class="kpi-value" style="font-size:1.5rem;">{msg_count}</div>
          <div class="kpi-label">Queries Processed</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Sample Queries")
        st.caption("Click any item to execute query:")

        for q in EXAMPLE_QUESTIONS:
            short = q if len(q) <= 44 else q[:41] + "..."
            if st.button(short, key=f"eq_{q}", use_container_width=True):
                st.session_state.pending_query = q

        st.markdown("<hr/>", unsafe_allow_html=True)
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.chat_history = [{
                "role": "bot", "type": "text",
                "content": "Conversation history reset. Enter a query below.",
                "ts": datetime.now().strftime("%H:%M"),
            }]
            st.session_state.pending_query = None
            st.rerun()

        st.markdown("""
        <div style="font-size:0.75rem; color:var(--text-muted); margin-top:12px; line-height:1.5;">
          <strong>Architecture</strong><br/>
          Natural language regex intent matching with Pandas vector queries. Zero external API dependencies.
        </div>
        """, unsafe_allow_html=True)

    # ── Chat Area ─────────────────────────────────────────────────────────────
    with chat_col:
        for msg in st.session_state.chat_history:
            _bubble(msg)

        st.markdown('<div id="chat-bottom"></div>', unsafe_allow_html=True)
        st.components.v1.html("""
        <script>
          const el = window.parent.document.getElementById('chat-bottom');
          if (el) el.scrollIntoView({behavior:'smooth'});
        </script>
        """, height=0)

        st.markdown("")

        with st.form("chat_form", clear_on_submit=True):
            cols = st.columns([6, 1])
            with cols[0]:
                user_input = st.text_input(
                    "Message",
                    placeholder="Enter query (e.g. 'Show employees in IT department' or 'Who has the highest score?')...",
                    label_visibility="collapsed",
                )
            with cols[1]:
                send = st.form_submit_button("Send", use_container_width=True)

        query = None
        if send and user_input.strip():
            query = user_input.strip()
        elif st.session_state.pending_query:
            query = st.session_state.pending_query
            st.session_state.pending_query = None

        if query:
            now = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({
                "role": "user", "type": "text",
                "content": query, "ts": now,
            })
            with st.spinner("Processing query..."):
                resp = process_query(query)
            st.session_state.chat_history.append({
                "role": "bot", "ts": now, **resp,
            })
            st.rerun()


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_chatbot()
