
import streamlit as st
from utils import load_css
from agent import run_agent

def main():
    st.set_page_config(page_title="YouTube Transcript Summarizer", page_icon="📝", layout="wide")
    st.title("YouTube Transcript Summarizer")

    css = load_css("style.css")
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    st.subheader("Enter a YouTube URL or a search query")

    query = st.text_input("", "")

    if st.button("Summarize"):
        if query:
            with st.spinner("Summarizing..."):
                summary, reasoning = run_agent(query)
                st.subheader("Summary")
                st.text_area("", summary, height=200)

                with st.expander("Show Reasoning"):
                    st.write(reasoning)

                st.subheader("Rate the summary")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Good"):
                        st.markdown('<div class="feedback success"><span>👍</span> Thanks for your feedback!</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("👎 Bad"):
                        st.markdown('<div class="feedback error"><span>👎</span> Thanks for your feedback! We will improve.</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a YouTube URL or a search query.")

if __name__ == "__main__":
    main()
