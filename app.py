
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

# Sidebar options
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

# Dynamic input areas
st.subheader("📥 Enter your request or code below")

language = ""
topic = ""
user_input = ""

if learning_goal == "Explain a coding concept":
    user_input = st.text_input("🧠 Concept you want explained:")

elif learning_goal == "Help me debug my code":
    user_input = st.text_area("🐞 Paste your buggy code here:")

elif learning_goal == "Translate code to another language":
    user_input = st.text_area("🔁 Paste your code to translate:")
    language = st.selectbox("🌐 Translate to language:", ["Python", "JavaScript", "C++", "Java"])

elif learning_goal == "Explain what my code does":
    user_input = st.text_area("🔍 Paste your code for explanation:")

elif learning_goal == "Give me a practice problem":
    language = st.selectbox("🌐 Programming language:", ["Python", "JavaScript", "C++", "Java"])
    topic = st.text_input("📚 Topic or concept (e.g., loops, arrays):")

elif learning_goal == "Ask anything about programming":
    user_input = st.text_input("💬 What's your question?")

# Build prompt
def build_prompt():
    base = "You are CodeGenie, a friendly AI coding mentor."
    if beginner_mode:
        base += " Explain everything simply, assuming the user is new to programming."

    if learning_goal == "Explain a coding concept":
        return f"{base}\n\nExplain this concept clearly: {user_input}"

    elif learning_goal == "Help me debug my code":
        return f"{base}\n\nA user is having trouble with this code. Identify what's wrong, explain it, and suggest a fix:\n```{user_input}```"

    elif learning_goal == "Translate code to another language":
        return f"{base}\n\nTranslate this code to {language}:\n```{user_input}```"

    elif learning_goal == "Explain what my code does":
        return f"{base}\n\nExplain what this code does line-by-line:\n```{user_input}```"

    elif learning_goal == "Give me a practice problem":
        return f"{base}\n\nGive the user a beginner-level coding challenge in {language} about {topic}. Include a description, hint, and solution."

    elif learning_goal == "Ask anything about programming":
        return f"{base}\n\n{user_input}"

# Handle prompt-based request
if st.button("✨ Get Help from CodeGenie"):
    if any([user_input, topic]):  # check if inputs exist
        with st.spinner("Summoning the Genie... 🧞‍♂️"):
            try:
                prompt = build_prompt()
                response = model.generate_content(prompt)
                answer = response.candidates[0].content.parts[0].text
                st.subheader("🧞‍♂️ CodeGenie Says:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please fill out the input fields first.")

# 🔄 Chat Mode (Optional)
st.divider()
st.subheader("💬 Ask CodeGenie Anything")

chat_input = st.chat_input("Ask me something about programming...")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if chat_input:
    # First-time context
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

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["parts"])
    else:
        st.chat_message("assistant").markdown(msg["parts"])
