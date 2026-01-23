import streamlit as st
import tempfile
from pathlib import Path
from app.main import process_invoice
from app.services.invoice_llm_service import ask_invoice_question

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Invoice AI Assistant",
    page_icon="📄",
    layout="wide"
)

# ------------------ HEADER ------------------
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: 700;
    color: #2C3E50;
}
.subtitle {
    font-size: 18px;
    color: #7F8C8D;
}
.card {
    background-color: #F8F9FA;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📄 Invoice AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload invoices & ask questions using AI</div>', unsafe_allow_html=True)
st.divider()

# ------------------ FILE UPLOAD SECTION ------------------
st.markdown("### 📤 Upload Files")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        pdf_file = st.file_uploader(
            "Upload Invoice PDF",
            type=["pdf"],
            help="Upload invoice PDF file"
        )

    with col2:
        excel_file = st.file_uploader(
            "Upload Excel File",
            type=["xlsx", "xls"],
            help="Upload invoice reference Excel"
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ PROCESS FILES ------------------
invoice_processed = False

if pdf_file and excel_file:
    if st.button("🚀 Process Invoice", use_container_width=True):
        with st.spinner("Processing invoice using AI..."):
            try:
                # Save PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(pdf_file.read())
                    pdf_path = tmp_pdf.name

                # Save Excel
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
                    tmp_excel.write(excel_file.read())
                    excel_path = tmp_excel.name

                # Call backend
                invoice_data = process_invoice(pdf_path, excel_path)

                st.success("✅ Invoice processed successfully!")
                st.session_state["invoice_data"] = invoice_data
                invoice_processed = True

            except Exception as e:
                st.error(f"❌ Processing failed: {e}")

# ------------------ SHOW EXTRACTED DATA ------------------
if "invoice_data" in st.session_state:
    st.markdown("### 📊 Extracted Invoice Data")
    st.json(st.session_state["invoice_data"], expanded=False)

# ------------------ QUESTION ANSWERING ------------------
st.divider()
st.markdown("### 💬 Ask Questions About the Invoice")

question = st.text_input(
    "Type your question (e.g. What is the payment status?)",
    placeholder="Ask anything about the invoice..."
)

if question and st.button("🧠 Ask AI", use_container_width=True):
    with st.spinner("Thinking..."):
        try:
            answer = ask_invoice_question(question=question)
            st.markdown("### 🤖 AI Answer")
            st.success(answer)

        except Exception as e:
            st.error(f"❌ Failed to answer: {e}")

# ------------------ FOOTER ------------------
st.divider()
st.caption("⚡ Powered by Ollama + RAG | Invoice AI Assistant")
