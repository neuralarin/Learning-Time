import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

# Load environment variables
load_dotenv()

# LLM
model = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert information extraction assistant.

Your task is to carefully read the given paragraph and extract all important and useful information.

Rules:
- Extract ONLY information explicitly mentioned.
- Never hallucinate or guess.
- If information is unavailable, write "Not Mentioned."
- Keep the response concise and well organized.
- End with a 2-4 sentence summary.

Extract:

• Title / Name
• Category
• Genre
• Type
• Language
• Country of Origin
• Release Date / Year
• Based On
• Franchise / Series
• Production Company
• Distributor
• Director(s)
• Writer(s)
• Producer(s)
• Cast
• Main Characters
• Organizations Mentioned
• Locations Mentioned
• Timeline / Setting
• Related Universe / Series
• Sequel / Prequel Information
• Major Plot
• Important Events
• Themes
• Keywords
• Important Facts
• Summary

Format the response using headings and bullet points.
"""
        ),
        (
            "human",
            """
Extract useful information from the following paragraph.

Paragraph:
{paragraph}
"""
        )
    ]
)

# Create chain
chain = prompt | model

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Information Extractor", page_icon="📄")

st.title("🎬 Movie Information Extractor")

paragraph = st.text_area(
    "Enter your paragraph:",
    height=250,
    placeholder="Paste your paragraph here..."
)

if st.button("Extract Information"):
    if paragraph.strip():
        with st.spinner("Extracting information..."):
            response = chain.invoke({"paragraph": paragraph})

        st.markdown("## Extracted Information")
        st.write(response.content)
    else:
        st.warning("Please enter a paragraph.")