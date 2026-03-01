import json
import os
import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Mood Books",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #0e0c0a;
}

.block-container {
    padding-top: 60px !important;
    max-width: 700px !important;
}

body, p, div, span, label {
    color: #e8e0d0 !important;
    font-family: 'DM Mono', monospace !important;
}

.eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c4a05a !important;
    text-align: center;
    margin-bottom: 12px;
}

.main-heading {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 400;
    line-height: 1.1;
    color: #f0e8d8 !important;
    text-align: center;
    margin-bottom: 10px;
}

.main-heading em {
    font-style: italic;
    color: #c4a05a !important;
}

.subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #5a5040 !important;
    text-align: center;
    margin-bottom: 48px;
}

.word-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #5a5040 !important;
    margin-bottom: 4px;
}

.stTextInput > div > div > input {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 1px solid #3a3020 !important;
    border-radius: 0 !important;
    color: #f0e8d8 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important;
    font-style: italic !important;
    padding: 8px 0 !important;
    box-shadow: none !important;
}

.stTextInput > div > div > input:focus {
    border-bottom: 1px solid #c4a05a !important;
    box-shadow: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: #3a3020 !important;
    font-style: italic !important;
}

.stTextInput > label {
    display: none !important;
}

.stButton > button {
    background-color: #c4a05a !important;
    color: #0e0c0a !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 16px !important;
    margin-top: 20px !important;
}

.stButton > button:hover {
    background-color: #d4b06a !important;
    color: #0e0c0a !important;
}

hr {
    border-color: #2a2418 !important;
    margin: 32px 0 !important;
}

.results-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #5a5040 !important;
    text-align: center;
    margin-bottom: 28px;
}

.book-card {
    background-color: #16140f;
    border: 1px solid #2a2418;
    padding: 24px;
    margin-bottom: 24px;
}

.book-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0e8d8 !important;
    line-height: 1.3;
    margin-bottom: 4px;
}

.book-author {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c4a05a !important;
    margin-bottom: 14px;
}

.book-summary {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    line-height: 1.7;
    color: #8a8070 !important;
    margin-bottom: 16px;
}

.mood-divider {
    border-top: 1px solid #2a2418;
    padding-top: 14px;
    margin-top: 4px;
}

.mood-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c4a05a !important;
    margin-bottom: 6px;
}

.mood-text {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    line-height: 1.6;
    color: #6a6050 !important;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)


def get_book_recommendations(words: list) -> list:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    quoted = '", "'.join(words)
    prompt = f"""The user described their current vibe/mood/preferences with these words: "{quoted}".

These words could mean mood, genre, feeling, aesthetic, or themes — interpret them creatively.

Recommend exactly 5 books that perfectly match this combination.

Return ONLY a valid JSON array (no markdown, no explanation). Each object:
{{
  "title": "exact book title",
  "author": "Author Full Name",
  "year": 1984,
  "summary": "2-3 sentence description of the book",
  "mood_match": "1-2 sentences: why this book fits the given words specifically",
  "rating": "Approximate rating out of 5 based on critical reception e.g. 4.2"
}}"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1200,
        system="You are a world-class literary curator with encyclopedic knowledge of fiction and non-fiction.",
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<div class='eyebrow'>Literary Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='main-heading'>What are you <em>feeling</em>?</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>3 words → 5 perfect books</div>", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='word-label'>Word 1</div>", unsafe_allow_html=True)
    word1 = st.text_input("w1", placeholder="melancholy", key="w1")
with col2:
    st.markdown("<div class='word-label'>Word 2</div>", unsafe_allow_html=True)
    word2 = st.text_input("w2", placeholder="adventure", key="w2")
with col3:
    st.markdown("<div class='word-label'>Word 3</div>", unsafe_allow_html=True)
    word3 = st.text_input("w3", placeholder="surreal", key="w3")

words = [w.strip() for w in [word1, word2, word3] if w.strip()]

# ── Button & Results ──────────────────────────────────────────────────────────
if st.button("Find My Books →"):
    if not words:
        st.warning("Please enter at least one word.")
    else:
        with st.spinner("Consulting the library..."):
            try:
                books = get_book_recommendations(words)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='results-label'>Recommendations for &ldquo;{' · '.join(words)}&rdquo;</div>",
                    unsafe_allow_html=True
                )

                for book in books:
                    st.markdown(f"""
                        <div class='book-card'>
                            <div class='book-title'>{book['title']}</div>
                            <div class='book-author'>by {book['author']} &nbsp;·&nbsp; ⭐ {book.get('rating', 'N/A')} &nbsp;·&nbsp; {book.get('year', '')}</div>
                            <div class='book-summary'>{book['summary']}</div>
                            <div class='mood-divider'>
                                <div class='mood-label'>Why it fits</div>
                                <div class='mood-text'>{book['mood_match']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")


#Use this code in Terminal to run the app: cd ~/dev/py && streamlit run mood_books_app.py and control + c to stop