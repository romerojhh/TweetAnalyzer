import streamlit as st
import time

def get_response_from_prompt(prompt):
    # Add backend here
    pass

def response_generator(prompt):
    response = get_response_from_prompt(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.1)

def main():
    if 'twitter_id1' not in st.session_state or 'twitter_id2' not in st.session_state:
        st.switch_page("app.py")
    st.set_page_config(initial_sidebar_state="collapsed")

    _, col1 = st.columns([10, 2.5])
    with col1:
        if st.button("→ Home🏠", use_container_width=True):
            st.switch_page("app.py")

    st.title("Chat with TweetAnalyzer..")
    st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me Anything!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

