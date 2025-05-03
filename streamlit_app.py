import streamlit as st
import google.generativeai as genai
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

api_key = os.getenv("OPENAI_KEY")

if not api_key:
    st.error("❌ API key not found.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to fetch/generate a response
def get_response(messages):
    try:
        response = model.generate_content(messages)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Maintain conversation history
def fetch_conversation_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "user",
                "parts": "System prompt: You are Tarot Tina - the world's best psychic and tarot reader. You teach about spirituality, astrology, and tarot. Be helpful, mysterious, and kind. Use emojis and images when you can."
            }
        ]
    return st.session_state["messages"]

# UI
st.title("🔮 Tarot Tina - Your Tarot Reader and Psychic Mentor")

user_input = st.chat_input("You:")

if user_input:
    messages = fetch_conversation_history()
    messages.append({"role": "user", "parts": user_input})

    response = get_response(messages)

    if isinstance(response, str):  # If an error string
        st.error(response)
    else:
        reply = response.candidates[0].content.parts[0].text
        messages.append({"role": "model", "parts": reply})

    for message in messages:
        if message["role"] == "model":
            st.write(f"🧙‍♀️ Tarot Tina: {message['parts']}")
        elif message["role"] == "user" and "System prompt" not in message["parts"]:
            st.write(f"🧍 You: {message['parts']}")
