import streamlit as st
import requests
import os
from datetime import date

# Page settings
st.set_page_config(
    page_title=" AI Study Planner",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Planner")
st.write("🎯 Your Personal AI-Powered Study Assistant")
st.write("Plan Smart • Study Better • Achieve More")
st.caption("Developed by Anwar | Data Science & AI")

st.divider()

# Language option
language = st.radio(
    "🌐 Language",
    ["English", "Roman Urdu", "Urdu"],
    index=1
)

# User inputs
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
    ["Beginner", "Intermediate", "Advanced"]
)

topics = st.text_area(
    "📝 Topics",
    placeholder="Example:\nLinear Regression\nSVM\nDecision Tree\nClustering"
)


# AI function
def generate_ai_plan(
    subject,
    exam_date,
    study_hours,
    difficulty,
    topics,
    language
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "ERROR: OPENROUTER_API_KEY is not set."

    # Language instructions
    if language == "English":

        language_instruction = """
Write the complete study plan in simple English.
"""

    elif language == "Roman Urdu":

        language_instruction = """
Write the complete study plan in simple Roman Urdu.
Do NOT use Urdu/Arabic script.
Use English technical terms when necessary,
but explain them in simple Roman Urdu.
Example:
"Regression ka basic concept samjho aur examples practice karo."
"""

    else:

        language_instruction = """
Write the complete study plan in Urdu language.
Use Urdu script.
Keep technical terms such as Regression, SVM and MCQs
in English where appropriate.
"""


    prompt = f"""
You are an expert AI Study Planner.

Create a personalized day-by-day study plan.

Student Information:

Subject: {subject}
Exam Date: {exam_date}
Daily Study Hours: {study_hours}
Difficulty Level: {difficulty}

Topics:
{topics}

{language_instruction}

Important requirements:

1. Calculate the study plan according to the exam date.
2. Create a day-by-day schedule.
3. Give priority to important/difficult topics.
4. Include study time for each topic.
5. Include practice questions or MCQs.
6. Include revision.
7. Include a final revision before the exam.
8. Give useful exam preparation tips.
9. Make the plan realistic for a student.

For every day include:

Day number
Topic
Study time
What to study
Practice/MCQs
Revision

Make the response clear and easy to understand.
"""


    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
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
            return f"API Error: {response.status_code}\n{response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"


# Generate button
if st.button(
    "🤖 Generate AI Study Plan",
    use_container_width=True
):

    if not subject:

        st.warning("Please enter your subject.")

    elif not topics:

        st.warning("Please enter your topics.")

    else:

        with st.spinner("🤖 AI study plan bana raha hai..."):

            plan = generate_ai_plan(
                subject,
                exam_date,
                study_hours,
                difficulty,
                topics,
                language
            )

        st.divider()

        st.subheader("📅 AI Generated Study Plan")

        st.markdown(plan)