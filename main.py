import openai
import streamlit as st

# API KEY
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit Title
st.title("Find Your Data")
st.markdown(
    '''
    **Directions:** Please type below what data you our interested in and our assistant will help you with finding it.
    '''
    )

# Set model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Build chat assistant
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"system", "content":"You are a friendly assistant that is helping users with zero data knowledge. Your role is to help them find at least 3 data sources and explain why they should consider them. Also, the responses may be in a different language, in which you should respond in the same language."}
    ]

# Build prompt with user input
if prompt := st.chat_input("Hi! What are you interested in for finding data sources for?"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        ):
            if response.choices[0].delta.content: full_response += response.choices[0].delta.content
            message_placeholder.markdown(full_response + "(|)")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role":"assistant", "content":full_response})