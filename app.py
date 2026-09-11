import streamlit as st
import requests
import os
from datetime import date


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)


# ==========================================
# HEADER
# ==========================================

st.title("📚 AI Study Planner")

st.subheader("🤖 Your Personal AI-Powered Study Assistant")

st.write(
    "Create a personalized day-by-day study plan "
    "based on your subject, exam date, study time, "
    "difficulty level and topics."
)

st.caption("✨ Developed by Shahzeb | Data Science & AI")

st.divider()


# ==========================================
# LANGUAGE
# ==========================================

language = st.radio(
    "🌐 Language",
    ["English", "Roman Urdu", "Urdu"],
    index=1
)


# ==========================================
# USER INPUTS
# ==========================================

subject = st.text_input(
    "📖 Subject",
    placeholder="Example: Machine Learning"
)


exam_date = st.date_input(
    "📅 Exam Date",
    min_value=date.today()
)


study_hours = st.number_input(
    "⏰ Daily Study Hours",
    min_value=1,
    max_value=12,
    value=3
)


difficulty = st.selectbox(
    "🎯 Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


topics = st.text_area(
    "📝 Topics",
    placeholder=(
        "Example:\n"
        "Linear Regression\n"
        "SVM\n"
        "Decision Tree\n"
        "Random Forest\n"
        "K-Means"
    )
)


# ==========================================
# CALCULATE DAYS
# ==========================================

today = date.today()

remaining_days = (exam_date - today).days


if remaining_days > 0:

    st.info(
        f"📅 {remaining_days} days remaining until your exam."
    )

elif remaining_days == 0:

    st.warning(
        "⚠️ Your exam is today!"
    )


# ==========================================
# GET API KEY
# ==========================================

def get_api_key():

    # First try Streamlit Secrets
    try:

        api_key = st.secrets["OPENROUTER_API_KEY"]

        if api_key:
            return api_key

    except Exception:
        pass


    # If running locally, try environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key:
        return api_key


    return None


# ==========================================
# GENERATE AI PLAN
# ==========================================

def generate_ai_plan():

    api_key = get_api_key()


    if not api_key:

        return (
            "❌ API Key nahi mili.\n\n"
            "Streamlit Cloud mein Settings → Secrets mein "
            "OPENROUTER_API_KEY add karein."
        )


    # ======================================
    # LANGUAGE INSTRUCTIONS
    # ======================================

    if language == "English":

        language_instruction = """
Write the complete study plan in simple English.
"""


    elif language == "Roman Urdu":

        language_instruction = """
Write the complete study plan in simple Roman Urdu.

IMPORTANT:
- Urdu/Arabic script bilkul use na karein.
- Roman Urdu use karein.
- English technical terms ko English mein rehne dein.
- Difficult technical terms ko simple Roman Urdu mein explain karein.

Example:
"Regression ka basic concept samjho aur examples practice karo."
"""


    else:

        language_instruction = """
Write the complete study plan in Urdu script.

Use English technical terms such as:
Regression, SVM, Decision Tree, MCQs
where appropriate.
"""


    # ======================================
    # TOPIC INFORMATION
    # ======================================

    if remaining_days > 0:

        days_instruction = f"""
The student has exactly {remaining_days} days
remaining before the exam.

Create a study plan covering these {remaining_days} days.

Do not create more days than the remaining days.
"""


    else:

        days_instruction = """
The exam date has arrived.
Create an emergency revision plan for today.
"""


    # ======================================
    # AI PROMPT
    # ======================================

    prompt = f"""
You are an expert AI Study Planner.

Create a personalized and realistic study plan.

STUDENT INFORMATION:

Subject:
{subject}

Exam Date:
{exam_date}

Days Remaining:
{remaining_days}

Daily Study Hours:
{study_hours}

Difficulty Level:
{difficulty}

Topics:
{topics}


{days_instruction}


{language_instruction}


For EVERY DAY include:

1. Day number
2. Topic
3. Study time
4. What to study
5. Practice questions or MCQs
6. Revision


IMPORTANT:

- Give more time to difficult topics.
- Give priority to important topics.
- Include revision.
- Include MCQ practice.
- Include a final revision before the exam.
- Make the plan realistic.
- Do not overload the student.
- Give useful exam preparation tips at the end.


FORMAT:

📅 Day 1
📚 Topic:
⏰ Study Time:
📖 What to Study:
📝 Practice/MCQs:
🔄 Revision:


Continue this format for every study day.

At the end provide:

🎯 Important Topics
🔄 Final Revision Strategy
💡 Exam Preparation Tips
"""


    # ======================================
    # OPENROUTER API
    # ======================================

    url = "https://openrouter.ai/api/v1/chat/completions"


    headers = {

        "Authorization": f"Bearer {api_key}",

        "Content-Type": "application/json",

        "HTTP-Referer": "https://streamlit.io",

        "X-Title": "AI Study Planner"

    }


    data = {

        "model": "openrouter/free",

        "messages": [

            {
                "role": "user",
                "content": prompt
            }

        ],

        "temperature": 0.7

    }


    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=90
        )


        # ==================================
        # API ERROR
        # ==================================

        if response.status_code != 200:

            return (
                f"❌ API Error: {response.status_code}\n\n"
                f"{response.text}"
            )


        result = response.json()


        # ==================================
        # AI RESPONSE
        # ==================================

        if "choices" not in result:

            return (
                "❌ AI ne koi valid response nahi diya."
            )


        return result["choices"][0]["message"]["content"]


    except requests.exceptions.Timeout:

        return (
            "⏱️ AI response mein zyada time lag raha hai. "
            "Dobara try karein."
        )


    except Exception as e:

        return f"❌ Error: {str(e)}"


# ==========================================
# GENERATE BUTTON
# ==========================================

if st.button(
    "🤖 Generate AI Study Plan",
    use_container_width=True
):

    if not subject:

        st.warning(
            "⚠️ Please enter your subject."
        )


    elif not topics:

        st.warning(
            "⚠️ Please enter your topics."
        )


    elif remaining_days < 0:

        st.error(
            "❌ Exam date past mein hai. "
            "Please select a future exam date."
        )


    else:

        with st.spinner(
            "🤖 AI aapka personalized study plan bana raha hai..."
        ):

            plan = generate_ai_plan()


        st.divider()

        st.subheader(
            "📅 AI Generated Study Plan"
        )

        st.markdown(plan)