import streamlit as st
from fuzzywuzzy import fuzz

# App title and intro
st.set_page_config(page_title="AI Doc Assistant", page_icon="💊")
st.title("💊 AI Doc Assistant")
st.markdown("""
Welcome to **AI Doc Assistant** — your simple chatbot for multivitamin advice.

Ask anything related to general wellness or energy-boosting multivitamins.
""")

# Q&A with italic formatting on the second answer
qa_pairs = [
    {
        "question": "Hi, I am looking for a multivitamin supplement.",
        "answer": "Hello. Looking into a multivitamin is a smart move. Let’s make sure you get the one that meets your needs.",
        "markdown": False
    },
    {
        "question": "I just want something to support my general health and maybe boost my energy.",
        "answer": "Understood.*You should take NutriPlus Daily Multi. It's the right choice for your health and energy support.*",
        "markdown": True
    }
]

# Fuzzy match function
def get_response(user_input, threshold=80):
    for qa in qa_pairs:
        score = fuzz.token_sort_ratio(user_input.lower(), qa["question"].lower())
        if score >= threshold:
            return qa["answer"], qa.get("markdown", False)
    return "Sorry, I can only help with general multivitamin questions right now.", False

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("markdown", False):
            st.markdown(msg["content"])
        else:
            st.write(msg["content"])

# Input
user_input = st.chat_input("Ask something about multivitamins...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response, is_markdown = get_response(user_input)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "markdown": is_markdown
    })

    # Show AI response
    with st.chat_message("assistant"):
        if is_markdown:
            st.markdown(response)
        else:
            st.write(response)
