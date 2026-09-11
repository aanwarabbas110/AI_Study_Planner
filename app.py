import streamlit as st
import requests
import os
from datetime import date


# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)


# ==============================
# HEADER
# ==============================

st.title("📚 AI Study Planner")

st.subheader("🤖 Your Personal AI-Powered Study Assistant")

st.write(
    "Create personalized, day-by-day study plans "
    "based on your subjects, exam date, study time, "
    "difficulty level, and topics."
)

st.caption("✨ Developed by Shahzeb | Data Science & AI")


# ==============================
# LANGUAGE
# ==============================

language = st.radio(
    "🌐 Language",
    ["English", "Roman Urdu", "Urdu"],
    index=1
)


# ==============================
# USER INPUT
# ==============================

subject = st.text_input(
    "📖 Subject",
    placeholder="e.g. Artificial Intelligence"
)

exam_date = st.date_input(
    "📅 Exam Date",
    min_value=date.today()
)

study_hours = st.number_input(
    "⏰ Daily Study Hours",
    min_value=1,
    max_value=12,
    value=2
)

difficulty = st.selectbox(
    "📊 Difficulty Level",
    ["Easy", "Medium", "Hard"]
)

topics = st.text_area(
    "📝 Topics / Syllabus",
    placeholder="e.g. AI Agents, Search Algorithms, Machine Learning, Neural Networks"
)


# ==============================
# API KEY FUNCTION
# ==============================

def get_api_key():

    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]

        if api_key:
            return api_key.strip()

    except Exception as e:
        st.error(f"Secrets Error: {e}")

    # Local computer fallback
    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key:
        return api_key.strip()

    return None


# ==============================
# AI STUDY PLAN FUNCTION
# ==============================

def generate_study_plan(
    subject,
    exam_date,
    study_hours,
    difficulty,
    topics,
    language
):

    api_key = get_api_key()

    if not api_key:
        return "❌ API Key nahi mili. Streamlit Cloud → Settings → Secrets mein OPENROUTER_API_KEY add karein."

    today = date.today()

    remaining_days = (exam_date - today).days

    if remaining_days < 1:
        return "❌ Exam date valid nahi hai."

    prompt = f"""
You are an expert AI study planner.

Create a personalized day-by-day study plan.

Student Information:

Subject: {subject}

Exam Date: {exam_date}

Today: {today}

Remaining Days: {remaining_days}

Daily Study Hours: {study_hours}

Difficulty Level: {difficulty}

Topics:
{topics}

Language: {language}

IMPORTANT REQUIREMENTS:

1. Create exactly {remaining_days} days of study planning.
2. Do not create extra days.
3. Divide the topics intelligently across the available days.
4. Mention the day number clearly.
5. Mention what the student should study each day.
6. Include the recommended study time.
7. Include revision.
8. Include practice questions or MCQs.
9. Include important exam tips.
10. Keep the plan realistic for {study_hours} hours per day.
11. Give a final revision strategy before the exam.
12. Write the complete response in {language}.

Make the plan clear and easy for a university student to follow.
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aistudyplanner.streamlit.app",
        "X-Title": "AI Study Planner"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:

            return (
                f"❌ OpenRouter API Error\n\n"
                f"Status Code: {response.status_code}\n\n"
                f"Details: {response.text}"
            )

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:

        return "❌ Request timeout. Please try again."

    except requests.exceptions.RequestException as e:

        return f"❌ Connection Error: {e}"

    except Exception as e:

        return f"❌ Unexpected Error: {e}"


# ==============================
# GENERATE BUTTON
# ==============================

if st.button("🚀 Generate AI Study Plan"):

    if not subject:

        st.warning("⚠️ Please enter your subject.")

    elif not topics:

        st.warning("⚠️ Please enter your topics / syllabus.")

    else:

        with st.spinner("🤖 AI is creating your study plan..."):

            plan = generate_study_plan(
                subject,
                exam_date,
                study_hours,
                difficulty,
                topics,
                language
            )

        st.markdown("---")

        st.header("📅 AI Generated Study Plan")

        st.markdown(plan)


# ==============================
# FOOTER
# ==============================

st.markdown("---")

st.caption(
    "📚 AI Study Planner | Powered by OpenRouter | "
    "Data Science & AI Project"
)