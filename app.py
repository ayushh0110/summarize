import streamlit as st
from summarizer import summarize_basic, summarize_advanced, MODELS
from pypdf import PdfReader

st.title("🧠 Smart Summarizer — Basic & Advanced Modes")

option = st.radio("Input type:", ["Text Input", "Upload PDF"])
model_choice = st.selectbox("Model:", list(MODELS.keys()))
model_name = MODELS[model_choice]

text=""

if option=="Text Input":
    text = st.text_area("Enter text:", height=200)
else:
    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        reader = PdfReader(file)
        for page in reader.pages:
            t = page.extract_text()
            if t: text += t+" "

max_len = st.slider("Max Length", 50,600,200)
min_len = st.slider("Min Length", 10,300,80)

col1, col2 = st.columns(2)

# 🟡 Normal Summarize
if col1.button("Summarize"):
    if len(text)<50:
        st.warning("Please add more text.")
    else:
        p = st.progress(0); status = st.empty()
        def upd(x): p.progress(x); status.write(f"Progress {x}%")
        with st.spinner("Summarizing…"):
            summary = summarize_basic(text, model_name, max_len, min_len, 300, upd)
        st.subheader("📄 Summary"); st.write(summary)

# 🔴 Extra Compress Summarize
if col2.button("Extra Summarize (More Compact)"):
    if len(text)<50:
        st.warning("Please add more text.")
    else:
        p = st.progress(0); status = st.empty()
        def upd(x): p.progress(x); status.write(f"Progress {x}%")
        with st.spinner("Compressing…"):
            summary = summarize_advanced(text, model_name, max_len, min_len, 300, upd)
        st.subheader("🔻 Extra Compressed Summary"); st.write(summary)
