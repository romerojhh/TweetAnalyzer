import streamlit as st
import tweet_analyzer as ta

def main():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.image("logo.png", use_column_width=True)
    html_content = """
<div style="text-align: center; padding: 10px;">
    <p>Our platform will fetch their latest tweets and provide insightful analysis, helping you understand trends, sentiments, and public discourse. Simply enter the username and get ready to unravel the wealth of information embedded within the Twittersphere!</p>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
    id1 = st.text_input("Enter Twitter ID:", "")
    st.session_state['twitter_id1'] = id1

    st.markdown(
        """
        <style>
        .sidebar .css-1ywd4w6 {text-align: center;}
        </style>
        """, unsafe_allow_html=True)
    _, col2, _ = st.columns([5, 3, 5])
    with col2:
        if st.button("Start Chatting!"):
            st.switch_page("pages/1_chat.py")

    chain = ta.setup_backend()
    st.session_state['chain'] = chain

if __name__ == "__main__":
    main()
