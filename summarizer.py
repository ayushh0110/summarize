from transformers import pipeline
import re
from functools import lru_cache

MODELS = {
    "BART (facebook/bart-large-cnn)": "facebook/bart-large-cnn",
    "T5 Large (t5-large)": "t5-large",
    "Pegasus (google/pegasus-xsum)": "google/pegasus-xsum",
}

@lru_cache(maxsize=3)
def load_model(name):
    print(f"Loading model → {name}")
    return pipeline("summarization", model=name, framework="pt")

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def summarize_once(text, model_name, max_length, min_length):
    model = load_model(model_name)
    text = clean_text(text)[:2000]
    summary = model(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]

def chunk_text(text, size=300):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

# Normal Summarization (NO final compression)
def summarize_basic(text, model_name, max_length, min_length, chunk_size=300, progress=None):
    text = clean_text(text)
    chunks = list(chunk_text(text, chunk_size))

    if len(chunks) == 1:
        if progress: progress(100)
        return summarize_once(text, model_name, max_length, min_length)

    summaries=[]
    for i,chunk in enumerate(chunks):
        summaries.append(summarize_once(chunk, model_name, max_length, min_length))
        if progress: progress(int(((i+1)/len(chunks))*100))

    return "\n\n".join(summaries)   # <-- no merge summarization

# Extra Summarization (Hierarchical)
def summarize_advanced(text, model_name, max_length, min_length, chunk_size=300, progress=None):
    basic = summarize_basic(text, model_name, max_length, min_length, chunk_size, progress)
    return summarize_once(basic, model_name, max_length//2, min_length//2)   # more compression
