# A chatbot using self-hosted LLAMA-2 or other LLM

# import openai
import streamlit as st
import json
import requests
from streamlit_chat import message

# Set up Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "primer" not in st.session_state:
    st.session_state["primer"] = "You are a friendly and helpful assistant."
if "context_length" not in st.session_state:
    st.session_state["context_length"] = 10


def main():
    st.sidebar.header("Settings")

    with st.sidebar:
        # Allow the user to set their prompt
        st.session_state.primer = st.text_area(
            "Primer Message",
            "You are a friendly and helpful assistant.",
        )
        st.session_state.context_length = st.slider(
            "Context Message Length", min_value=10, max_value=1000, value=300, step=10
        )

        # Allow Users to reset the memory
        if st.button("New Chat"):
            st.session_state.messages = []
            st.info("Chat Memory Cleared. New chat session is initiated.")

    # A place to draw the chat history
    history = st.container()

    # Change this url if changed
    url = 'https://e94b-34-29-123-139.ngrok.io/chatbot'


    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            # Create an on the fly message stack
            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages[-st.session_state.context_length :]
            )

            # Call the OpenAI API
            # r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

            r = {
            'llm' : "llama-7b-chat",
            'temperature' : 0.3,
            'top_k' : 3,
            'prompt' : input,
            "usage" : {"total_tokens": 300}
            # "content" : input
            }

        
            r = json.dumps(r)

            r = requests.post(url, data=r)
            r = r.json()
            print("response_data: ", r)


            st.session_state.messages.append(
                 {"role": "assistant", "content": r["content"]}
            )


    # display message history
    with history:
        messages = st.session_state.get('messages', {"content": ""})
        for i, msg in enumerate(messages[:]):
            print("i, msg: ", i, msg)
            if i % 2 != 0:
                with st.chat_message("user"):
                    st.markdown(f'{msg["content"]}')
                # message(msg["content"], is_user=True, key=str(i) + '_user')
            else:
                with st.chat_message("assistant"):
                    st.markdown(f'{msg["content"]}')
                # message(msg["content"], is_user=False, key=str(i) + '_ai')

# use streamlit_chat to set avatar styles:
# supported styles: https://www.dicebear.com/styles

# Move this line outside of any function
st.title("Chatbot based on self-hosted LLM")

# Call the main function
if __name__ == "__main__":
    main()

