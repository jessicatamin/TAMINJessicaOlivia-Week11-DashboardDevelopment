import streamlit as st
import agent

# Requires `DEEPSEEK_API_KEY` in `.env` for DeepSeek API integration.
st.set_page_config(page_title="AI Agent Dashboard", layout="wide")

st.sidebar.header("Configuration")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3)
response_style = st.sidebar.selectbox(
    "Response Style",
    options=["Concise", "Detailed", "Humorous"],
    index=0,
)

if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "agent_response" not in st.session_state:
    st.session_state.agent_response = ""
if "response_ready" not in st.session_state:
    st.session_state.response_ready = False

st.title("AI Agent Dashboard")
st.write("This dashboard provides a starting point for building AI agent workflows.")

input_container = st.container()
output_container = st.container()

with input_container:
    st.subheader("Input")
    user_question = st.text_input("Ask a question", key="user_question")
    action_col_1, action_col_2 = st.columns(2)
    with action_col_1:
        submit = st.button("Submit", use_container_width=True)
    with action_col_2:
        clear = st.button("Clear", use_container_width=True)

if clear:
    st.session_state.user_question = ""
    st.session_state.agent_response = ""
    st.session_state.response_ready = False
    st.rerun()

if submit:
    cleaned_input = user_question.strip()
    if not cleaned_input:
        st.error("Please enter a question before submitting.")
    else:
        try:
            with st.spinner("Processing..."):
                response = agent.process(
                    cleaned_input,
                    temperature=temperature,
                    response_style=response_style,
                )
            st.session_state.agent_response = response
            st.session_state.response_ready = True
            st.success("Response generated successfully.")
        except Exception as exc:
            st.error(f"Failed to process your request: {exc}")

with output_container:
    st.subheader("Agent Response")
    if st.session_state.response_ready:
        st.write(st.session_state.agent_response)
    else:
        st.info("Your agent response will appear here after submission.")
