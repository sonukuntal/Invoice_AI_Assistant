import streamlit as st
from app.services.invoice_llm_service import ask_invoice_question
from app.main import process_invoice

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Invoice AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown(
    "<h2 style='text-align:center;'>🤖 Invoice AI Assistant</h2>",
    unsafe_allow_html=True
)
st.caption("Upload invoices, analyze them, and ask questions in plain English")

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "invoice_loaded" not in st.session_state:
    st.session_state.invoice_loaded = False

# ---------------------------
# Upload Section
# ---------------------------
with st.expander("📤 Upload Invoice Files", expanded=not st.session_state.invoice_loaded):
    pdf_file = st.file_uploader("Invoice PDF", type=["pdf"])
    excel_file = st.file_uploader("Invoice Excel", type=["xlsx", "xls"])

    if st.button("Process Invoice"):
        if not pdf_file or not excel_file:
            st.warning("Please upload both PDF and Excel files")
        else:
            with st.spinner("Processing invoice..."):
                process_invoice(pdf_file, excel_file)
                st.session_state.invoice_loaded = True
                st.success("Invoice processed and stored")

# ---------------------------
# Chat History
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# Chat Input)
# ---------------------------
user_input = st.chat_input("Ask anything about your invoices...")

if user_input:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_invoice_question(user_input)
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )





