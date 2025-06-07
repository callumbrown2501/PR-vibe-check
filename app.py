import streamlit as st
import requests
import openai

# --- 1. UI Setup ---
st.set_page_config(page_title="PR Vibe Check", layout="centered")
st.title("🔍 PR Vibe Check Dashboard")

st.markdown("""
This tool gives you a quick media sentiment readout on a given topic.
It summarises tone, influence, and whether it's cutting through.
""")

topic = st.text_input("Enter a topic, sector, or policy to analyse:", placeholder="e.g. UK rail renationalisation")
country = st.selectbox("Focus region:", ["UK", "US", "EU", "Global"])
submit = st.button("Run Vibe Check")

# --- 2. News API Call ---
def fetch_news(topic, region="UK"):
    api_key = "b43373cb5c9c436e9f5e60f6c2147090"
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": api_key
    }
    try:
        res = requests.get(base_url, params=params)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return articles
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# --- 3. GPT Vibe Analysis ---
def generate_vibe_summary(articles, topic):
    openai.api_key = "sk-fieOblFi1abuO81Gc1NX2yRK3jg0RkJ7OXxzlcuP2biC2HwM0inC1xqrswAysrme086_xcwEuQT3BlbkFJAltLPMuYYPlYqxTz0dLP5O8bIEqn1yLxmuUGdaP46g6_b5zZT0IJAt-q1BRY5m7sUMx6k-UrgA"

    content = "\n\n".join([f"{a['title']} - {a['description']}" for a in articles if a['description']])

    prompt = f"""
    You're a media analyst for a PR agency.
    Given recent articles about "{topic}", summarise the following:

    - Overall sentiment (positive, neutral, negative)
    - Media tone (supportive, critical, divided)
    - Key commentators or outlets
    - Any noticeable patterns or gaps (e.g. silence, low traction)

    Here's the content:
    {content}

    Return a clear bullet-point summary for PR planning.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"GPT error: {e}")
        return ""

# --- 4. Run and Display ---
if submit and topic:
    with st.spinner("Collecting news and analysing vibes..."):
        articles = fetch_news(topic, country)
        if articles:
            st.success(f"Found {len(articles)} articles. Generating vibe check...")
            summary = generate_vibe_summary(articles, topic)
            st.markdown("### 🧠 Media Vibe Summary")
            st.markdown(summary)
        else:
            st.warning("No relevant articles found for this topic.")
