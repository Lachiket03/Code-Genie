
import streamlit as st
import google.generativeai as genai
import os
import dotenv

# Load Gemini API key
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="CodeGenie 👩‍💻", layout="wide")
st.title("🧞‍♂️ CodeGenie – Learn to Code, the Easy Way")

# Sidebar
st.sidebar.header("🧠 What do you want to learn?")
learning_goal = st.sidebar.selectbox("Choose a topic or action", [
    "Explain a coding concept",
    "Help me debug my code",
    "Translate code to another language",
    "Explain what my code does",
    "Give me a practice problem",
    "Ask anything about programming"
])

beginner_mode = st.sidebar.checkbox("🍼 Beginner Mode (simplify explanations)", value=True)

# Build prompt for Gemini
def build_prompt(task, user_input):
    base = "You are CodeGenie, a friendly AI coding mentor."
    if beginner_mode:
        base += " Explain everything simply, assuming the user is new to programming."

    if task == "Explain a coding concept":
        return f"{base}\n\nExplain this concept clearly: {user_input}"

    elif task == "Help me debug my code":
        return f"{base}\n\nA user is having trouble with this code. Identify what's wrong, explain it, and suggest a fix:\n```{user_input}```"

    elif task == "Translate code to another language":
        lang = st.sidebar.selectbox("Translate to", ["Python", "JavaScript", "C++", "Java"])
        return f"{base}\n\nTranslate this code to {lang}:\n```{user_input}```"

    elif task == "Explain what my code does":
        return f"{base}\n\nExplain what this code does line-by-line:\n```{user_input}```"

    elif task == "Give me a practice problem":
        return f"{base}\n\nGive the user a beginner-level coding challenge in {user_input}. Include a description, hint, and solution."

    elif task == "Ask anything about programming":
        return f"{base}\n\n{user_input}"

# Section: Prompt-based help
st.subheader("📥 Enter your request or code below")
user_input = st.text_area("Paste code, type a concept, or ask a question:")

if st.button("✨ Get Help from CodeGenie") and user_input.strip():
    with st.spinner("Summoning the Genie... 🧞‍♂️"):
        prompt = build_prompt(learning_goal, user_input)
        try:
            response = model.generate_content(prompt)
            answer = response.candidates[0].content.parts[0].text
            st.subheader("🧞‍♂️ CodeGenie Says:")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Section: Chat-based Q&A
st.divider()
st.subheader("💬 Ask CodeGenie Anything")
chat_input = st.chat_input("Ask me something about programming...")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if chat_input:
    if len(st.session_state.chat_history) == 0:
        chat_input = "You are CodeGenie, a friendly AI that helps beginners learn to code. " + chat_input

    st.session_state.chat_history.append({"role": "user", "parts": chat_input})

    try:
        chat_response = model.generate_content(st.session_state.chat_history)
        chat_reply = chat_response.candidates[0].content.parts[0].text
        st.session_state.chat_history.append({"role": "model", "parts": chat_reply})
    except Exception as e:
        chat_reply = f"Error: {str(e)}"
        st.session_state.chat_history.append({"role": "model", "parts": chat_reply})

# Show chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["parts"])
    else:
        st.chat_message("assistant").markdown(msg["parts"])
