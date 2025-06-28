import streamlit as st

def main():
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your pdf")
    pdf=st.file_uploader("Upload your pdf")


if __name__ =='__main__':
    main()