import streamlit as st
from app.services.rag.rag_pipeline import ask_question
from app.main import process_invoice
import tempfile

# -------------------------------------------------
# Page config (ChatGPT feel)
# -------------------------------------------------
st.set_page_config(
    page_title="Invoice AI Assistant",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Invoice AI Assistant")
st.caption("Ask questions about your invoices")

# -------------------------------------------------
# Session state initialization
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# -------------------------------------------------
# Upload section (only once)
# -------------------------------------------------
with st.sidebar:
    st.header("📂 Upload Files")

    pdf_file = st.file_uploader("Upload Invoice PDF", type=["pdf"])
    excel_file = st.file_uploader("Upload Invoice Excel", type=["xlsx"])

    if st.button("Process Documents"):
        if not pdf_file or not excel_file:
            st.warning("Please upload both PDF and Excel")
        else:
            with st.spinner("Processing invoices..."):
                # Save PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(pdf_file.read())
                    pdf_path = tmp_pdf.name

                # Save Excel
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
                    tmp_excel.write(excel_file.read())
                    excel_path = tmp_excel.name

                process_invoice(pdf_path, excel_path)

                st.session_state.data_loaded = True
                st.success("Invoices indexed successfully!")

# -------------------------------------------------
# Chat history display
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# Chat input
# -------------------------------------------------
if st.session_state.data_loaded:
    user_input = st.chat_input("Ask a question about your invoices...")
else:
    user_input = None
    st.info("👈 Upload PDF & Excel to start chatting")

# -------------------------------------------------
# Handle user message
# -------------------------------------------------
if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_question(user_input)
            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })