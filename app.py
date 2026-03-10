import streamlit as st
import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="Market Mind AI", page_icon="📈", layout="wide")

# Sidebar - Configuration
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
model = st.sidebar.selectbox("Choose Model:", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])

# Initialize Groq Client
if api_key:
    client = Groq(api_key=api_key)
else:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")
    st.stop()

def get_market_intelligence(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a senior market analyst and marketing strategist."},
                {"role": "user", "content": prompt},
            ],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Main UI
st.title("🧠 Market Mind: AI Sales & Marketing Intelligence")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Market Analysis", "✍️ Sales Copy Gen", "💡 Strategy Chat"])

with tab1:
    st.header("Global Market Intelligence")
    industry = st.text_input("Industry (e.g., Renewable Energy, SaaS, Fintech):")
    region = st.text_input("Target Region (e.g., SE Asia, North America):")
    
    if st.button("Generate Market Report"):
        with st.spinner("Analyzing market trends..."):
            prompt = f"Provide a detailed market intelligence report for the {industry} industry in {region}. Include top 3 trends, competitive landscape, and potential risks for 2026."
            report = get_market_intelligence(prompt)
            st.markdown(report)

with tab2:
    st.header("AI Sales Copywriter")
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name:")
        target_audience = st.text_input("Target Audience:")
    with col2:
        tone = st.selectbox("Tone:", ["Professional", "Witty", "Aggressive", "Empathetic"])
        platform = st.selectbox("Platform:", ["Email", "LinkedIn Post", "Ad Copy"])

    if st.button("Generate Copy"):
        with st.spinner("Writing copy..."):
            prompt = f"Write a high-converting {platform} for {product_name} targeting {target_audience}. The tone should be {tone}. Focus on benefits and a clear Call to Action."
            copy = get_market_intelligence(prompt)
            st.code(copy, language="markdown")

with tab3:
    st.header("Consultant Chat")
    st.info("Ask specific questions about your marketing strategy or sales hurdles.")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I increase my conversion rate?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = get_market_intelligence(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})