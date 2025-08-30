import streamlit as st
import pandas as pd
from preprocessing import preprocess_tickets
from chat_summary import prepare_ticket_narrative, summarize_category


st.title("📊 Ticket Storytelling Summarizer")
st.write("Upload a ticket dataset, clean it, and generate storytelling summaries using LLaMA 3.")

uploaded_file = st.file_uploader("Upload ticket file (.csv or .txt)", type=["csv", "txt"])

if uploaded_file:
    # Load file
    df = pd.read_csv(uploaded_file)
    st.subheader("📂 Raw Data Preview")
    st.dataframe(df.head())

    # Clean + Map
    df_clean = preprocess_tickets(uploaded_file)

    st.subheader("✅ Cleaned & Mapped Data")
    st.dataframe(df_clean.head())

    # Group by Product Category
    grouped = df_clean.groupby("PRODUCT_CATEGORY")

    if st.button("Generate Summaries"):
        summaries = {}
        with st.spinner("Generating summaries with LLaMA 3..."):
            for product, tickets in grouped:
                tickets_text = prepare_ticket_narrative(tickets)
                summary = summarize_category(product, tickets_text)
                summaries[product] = summary

        st.subheader("📖 Storytelling Summaries")
        for product, summary in summaries.items():
            st.markdown(f"### 🏷️ {product}")
            st.write(summary)

        # Option to download
        all_text = ""
        for product, summary in summaries.items():
            all_text += f"===== {product} =====\n{summary}\n\n"

        st.download_button(
            label="📥 Download Summaries (TXT)",
            data=all_text,
            file_name="ticket_storytelling_summaries.txt",
            mime="text/plain"
        )


