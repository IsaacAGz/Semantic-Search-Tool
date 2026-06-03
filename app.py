import streamlit as st
import requests

st.set_page_config(
    page_title="AI Semantic Search & Summary",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Semantic Search & Summary Tool")
st.markdown("Provide a document or raw context below, then ask questions about it using a lightweight serverless AI pipeline.")
st.markdown("---")

API_URL = "https://semantic-search-tool.vercel.app/api/ask"

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Step 1: Provide Context Source")

    context_input = st.text_area(
        "Paste your text dataset or article context here:",
        height=350,
        placeholder="Type or paste the reference material the AI should analyze..."
    )

with col2:
    st.subheader("🔍 Step 2: Query the Data")

    question_input = st.text_input(
        "What would you like to know or find?",
        placeholder="e.g., When does a product release?"
    )

    st.markdown("### ⚡ AI Response")

    if st.button("Run AI Analysis", type="primary"):
        if not context_input.strip() or not question_input.strip():
            st.warning("Please fill out both the context and the questions files before running.")
        else:
            
            with st.spinner("Querying serverless pipeline..."):
                try:
                    payload = {
                        "context": context_input,
                        "question": question_input
                    }

                    response = requests.post(API_URL, json=payload, timeout=30)

                    if response.status_code == 200:
                        result = response.json()

                        st.success("Analysis Complete!")
                        st.info(result.get("answer", "No answer found in response."))
                    else:
                        st.error(f"Backend Error (Status {response.status_code}): {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the backend server: {e}")
