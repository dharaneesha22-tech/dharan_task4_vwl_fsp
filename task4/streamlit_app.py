import streamlit as st
import sqlite3
import requests

st.set_page_config(
    page_title="QuoteVerse",
    page_icon="💬",
    layout="centered"
)

st.title("💬 QuoteVerse")
st.write("Random Quotes, History and Favorites")


# -----------------------------
# Database
# -----------------------------
def get_connection():
    return sqlite3.connect("quotes.db")


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_database()


# -----------------------------
# Get Random Quote
# -----------------------------
def get_random_quote():

    try:
        response = requests.get(
            "https://api.quotable.io/random",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()

            quote = data.get(
                "content",
                "Success is built one day at a time."
            )

            author = data.get(
                "author",
                "QuoteVerse"
            )

        else:
            quote = "Success is built one day at a time."
            author = "QuoteVerse"

    except Exception:
        quote = "Success is built one day at a time."
        author = "QuoteVerse"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO history (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return quote, author


# -----------------------------
# Save Favorite
# -----------------------------
def save_favorite(quote, author):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO favorites (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Get History
# -----------------------------
def get_history():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT quote, author
        FROM history
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# -----------------------------
# Get Favorites
# -----------------------------
def get_favorites():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT quote, author
        FROM favorites
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# -----------------------------
# Random Quote
# -----------------------------
if st.button("🎲 Get Random Quote"):

    quote, author = get_random_quote()

    st.session_state["quote"] = quote
    st.session_state["author"] = author


# -----------------------------
# Display Quote
# -----------------------------
if "quote" in st.session_state:

    st.subheader("✨ Quote")

    st.info(
        f'"{st.session_state["quote"]}"'
    )

    st.write(
        f'— {st.session_state["author"]}'
    )

    if st.button("❤️ Add to Favorites"):

        save_favorite(
            st.session_state["quote"],
            st.session_state["author"]
        )

        st.success("Quote added to favorites!")


st.divider()


# -----------------------------
# History
# -----------------------------
st.subheader("📜 Quote History")

history = get_history()

if history:

    for quote, author in history:
        st.write(f'💬 "{quote}"')
        st.caption(f"— {author}")

else:
    st.write("No quote history available.")


st.divider()


# -----------------------------
# Favorites
# -----------------------------
st.subheader("❤️ Favorites")

favorites = get_favorites()

if favorites:

    for quote, author in favorites:
        st.write(f'❤️ "{quote}"')
        st.caption(f"— {author}")

else:
    st.write("No favorite quotes yet.")