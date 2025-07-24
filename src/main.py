import streamlit as st
from pdf_ingestion import *
from ollama import chat
from answer import *
import pandas as pd
import altair as alt
import re
import json

st.title("Dashboard LLM")

uploaded_file=st.file_uploader("Drop your CSV",type="csv")
if uploaded_file:

    st.success(f"✅ CSV processed and embedded successfully! You can now ask questions about the document.")

    df=pd.read_csv(uploaded_file)
    df.to_csv("data.csv", index=False)
    st.dataframe(df.head())
    preview=df.head(5).to_markdown(index=False)
    vectorstore = create_vectorstore("data.csv")


# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        if 'vectorstore' in locals() and vectorstore is not None:
            with st.spinner("Retrieving relevant information..."):
                context= retrieve(prompt, vectorstore)

            with st.spinner("Generating answer..."):
                        answer = generate_answer(prompt, context, preview)
                        st.write(answer)  # Debugging: Show the raw answer

                        # Extract JSON from the answer
                        json_match = re.search(r"```json\s*(\{.*?\})\s*```", answer, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1)
                            vega_spec = json.loads(json_str)

                            # Render the chart using the DataFrame directly
                            if "mark" in vega_spec or "encoding" in vega_spec:
                                st.vega_lite_chart(
                                    df,  # Use your DataFrame directly
                                   {
                                "mark": vega_spec["mark"],
                                "encoding": vega_spec["encoding"],
                                "title": vega_spec.get("title", "Generated Chart"),
                            },
                                    use_container_width=True,
                                )
                            else:
                                st.write("No chart data available.")
                        else:
                            st.write("No chart data available.")


        #st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

