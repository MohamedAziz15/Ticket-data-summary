# Ticket-data-summary
## 📚 Documentation for Ticket Storytelling Summarizer

---

### 1. Implementation Steps

#### **A. Data Preprocessing**
- **File Loading:** The app expects a ticket dataset in CSV or TXT format. When uploaded, it is read using `pandas.read_csv`.
- **Filtering:** Only tickets with specific `SERVICE_CATEGORY` values (`HDW`, `NET`, `KAI`, `KAV`, `GIGA`, `VOD`, `KAD`) are retained.
- **Cleaning:** The filtered data is saved as both CSV and Excel for further use.

#### **B. Category Mapping**
- **Mapping Logic:** Each allowed `SERVICE_CATEGORY` is mapped to a broader `PRODUCT_CATEGORY` (e.g., `KAI` and `NET` → `Broadband`).
- **Column Addition:** A new column `PRODUCT_CATEGORY` is added to the cleaned DataFrame.

#### **C. Summary Generation**
- **Grouping:** Tickets are grouped by `PRODUCT_CATEGORY`.
- **Narrative Preparation:** For each group, a narrative is constructed listing ticket details.
- **LLM Summarization:** The narrative is sent to the LLaMA 3 model via Groq API, which returns a structured, five-section summary.
- **Display & Download:** Summaries are shown in the app and can be downloaded as a TXT file.

---

### 2. Code Documentation

#### **preprocessing.py**
```python
import pandas as pd

def preprocess_tickets(file_path: str = "Ticket_Data.txt"):
    """
    Preprocess the ticket data by filtering specific service categories
    and mapping them to product categories.

    Steps:
    1. Load ticket data from a CSV/TXT file.
    2. Filter tickets to only include allowed service categories.
    3. Map service categories to product categories.
    4. Save cleaned data to CSV and Excel.
    5. Return the cleaned DataFrame.
    """
    df = pd.read_csv("Ticket_Data.txt")  # Load raw data

    allowed_categories = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
    filtered_df = df[df['SERVICE_CATEGORY'].isin(allowed_categories)]  # Filter

    category_product_map = {
        'KAI': 'Broadband',
        'NET': 'Broadband',
        'KAV': 'Voice',
        'KAD': 'TV',
        'GIGA': 'GIGA',
        'VOD': 'VOD'
    }
    filtered_df['PRODUCT_CATEGORY'] = filtered_df['SERVICE_CATEGORY'].map(category_product_map)  # Map

    filtered_df.to_csv("tickets_cleaned2.csv", index=False)  # Save CSV
    filtered_df.to_excel("tickets_cleaned.xlsx", index=False)  # Save Excel

    print("✅ Tickets cleaned and mapped successfully!")
    return filtered_df
```

#### **chat_summary.py**
```python
import pandas as pd
from groq import Groq
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

def prepare_ticket_narrative(tickets_df):
    """
    Convert a DataFrame of tickets into a narrative string for LLM input.
    Each ticket includes number, date, service, and issue.
    """
    records = []
    for _, row in tickets_df.iterrows():
        record = f"""
        Ticket: {row['ORDER_NUMBER']}
        Date: {row['ACCEPTANCE_TIME']}
        Service: {row['SERVICE_CATEGORY']}
        Issue: {row['ORDER_DESCRIPTION_1']} - {row['ORDER_DESCRIPTION_2']}
        """
        records.append(record)
    return "\n".join(records)

def summarize_category(product_name, tickets_text):
    """
    Use Groq's LLaMA 3 model to summarize tickets for a product category.
    The summary is structured into five sections.
    """
    prompt = f"""
    You are a summarization assistant. Summarize the following ticket records into a storytelling summary
    divided into **five sections**:
    1. Initial Issue
    2. Follow-ups
    3. Developments
    4. Later Incidents
    5. Recent Events
    IMPORTANT: You must strictly follow this structure.
    Here are the ticket details for product category: {product_name}
    {tickets_text}
    """
    client = Groq()
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

#### **app.py**
```python
import streamlit as st
import pandas as pd
from preprocessing import preprocess_tickets
from chat_summary import prepare_ticket_narrative, summarize_category

st.title("📊 Ticket Storytelling Summarizer")
st.write("Upload a ticket dataset, clean it, and generate storytelling summaries using LLaMA 3.")

uploaded_file = st.file_uploader("Upload ticket file (.csv or .txt)", type=["csv", "txt"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📂 Raw Data Preview")
    st.dataframe(df.head())

    df_clean = preprocess_tickets(uploaded_file)
    st.subheader("✅ Cleaned & Mapped Data")
    st.dataframe(df_clean.head())

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

        all_text = ""
        for product, summary in summaries.items():
            all_text += f"===== {product} =====\n{summary}\n\n"

        st.download_button(
            label="📥 Download Summaries (TXT)",
            data=all_text,
            file_name="ticket_storytelling_summaries.txt",
            mime="text/plain"
        )
```

---

### 3. User Guide

---


1. **Set Up the Environment:**
   - Open a terminal in the project directory.
   - Clone repo
   - Create uv :
        ```bash 
        uv init .
        ```
   - Create a virtual environment:
     ```bash
     uv add ruff
     ```
   - Activate the virtual environment:
     ```bash
     .\venv\Scripts\activate
     ```
   - Install the required dependencies:
     ```bash
     uv pip install -r requirements.txt
     ```

2. **Create the `.env` File:**
   - Ensure the `.env` file exists in the src directory with the following content:
     ```properties
     GROQ_API_KEY=
     ```

3. **Launch the App:**
   - Run the following command to start the Streamlit app:
     ```bash
     streamlit run app.py
     ```

4. **Upload Ticket Data:**
   - Click "Upload ticket file (.csv or .txt)" and select your ticket dataset.

5. **Preview Raw Data:**
   - The app displays the first few rows of your uploaded data.

6. **Clean & Map Data:**
   - The app automatically filters and maps categories, showing the cleaned data.

7. **Generate Summaries:**
   - Click "Generate Summaries" to start the LLaMA 3 summarization.
   - Wait for the summaries to be generated and displayed.

8. **Download Summaries:**
   - Click "Download Summaries (TXT)" to save all summaries as a text file.

#### **Requirements**
- Python 3.8+
- Required packages: `streamlit`, `pandas`, `groq`, `langchain_groq`, `python-dotenv`
- A valid Groq API key in `.env` file.

---
