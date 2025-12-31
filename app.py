import os

import openai
import streamlit as st
from streamlit_chat import message


APP_TITLE = "Amara"
PAGE_TITLE = "Care Assist"

MODEL_ID = "ft:gpt-3.5-turbo-0125:personal::8xxvubdv"
SYSTEM_PROMPT = "You are a helpful assistant."

# Simple demo user context rules (consider moving to a config file)
DIABETES_USERS = ["Steve", "Harvey"]
HEART_USERS = ["Tom", "Robert"]


st.set_page_config(page_title=PAGE_TITLE)
st.markdown(
    """
    <style>
    [data-testid="baseButton-secondaryFormSubmit"] {
        background: #757474 !important;
    }
    [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    </style>
    <br>
    <h1 style='text-align: center;'>Amara</h1>
    """,
    unsafe_allow_html=True,
)


# Avoid hard-coding secrets. Set OPENAI_API_KEY in your environment or Streamlit secrets.
openai.api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
openai.api_key = openai.api_key or os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.warning(
        "Missing OpenAI API key. Set OPENAI_API_KEY in environment variables or Streamlit secrets.",
        icon="⚠️",
    )

def _init_session_state() -> None:
    """Initialize Streamlit session keys used by the chat UI."""

    st.session_state.setdefault("generated", [])
    st.session_state.setdefault("past", [])
    st.session_state.setdefault("messages", [{"role": "system", "content": SYSTEM_PROMPT}])
    st.session_state.setdefault("model_name", [])
    st.session_state.setdefault("cost", [])
    st.session_state.setdefault("total_tokens", [])
    st.session_state.setdefault("total_cost", 0.0)


_init_session_state()

model_name = MODEL_ID
model = MODEL_ID


def generate_response(prompt: str):
    """Send a user prompt to the chat model and return the response + usage."""

    st.session_state["messages"].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(model=model, messages=st.session_state["messages"])
    response = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


def enrich_user_input(user_input: str) -> str:
    """Append lightweight user context (demo rules) and response length guidance."""

    enriched = user_input
    for usr in DIABETES_USERS:
        if usr.lower() in enriched.lower():
            enriched += " has diabetes"
    for usr in HEART_USERS:
        if usr.lower() in enriched.lower():
            enriched += " has heart condition."
    enriched += " Limit response to 300 characters"
    return enriched


response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
    if submit_button and user_input:
        actual_input = enrich_user_input(user_input)
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(actual_input)
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)
        st.session_state["model_name"].append(model_name)
        st.session_state["total_tokens"].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "gpt-3.5-turbo":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state["cost"].append(cost)
        st.session_state["total_cost"] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]};")
            # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
