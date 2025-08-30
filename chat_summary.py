import pandas as pd
from groq import Groq
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


def prepare_ticket_narrative(tickets_df):
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
    # from openai import OpenAI
    # client = OpenAI()

    prompt = f"""
    You are a summarization assistant. Summarize the following ticket records into a storytelling summary
    divided into **five sections**:

    1. Initial Issue:
       - Timeframe
       - Ticket Numbers
       - Narrative

    2. Follow-ups:
       - Timeframe
       - Ticket Numbers
       - Narrative

    3. Developments:
       - Timeframe
       - Ticket Numbers
       - Narrative

    4. Later Incidents:
       - Timeframe
       - Ticket Numbers
       - Narrative

    5. Recent Events:
       - Timeframe
       - Ticket Numbers
       - Narrative

    IMPORTANT: You must strictly follow this structure.

    Here are the ticket details for product category: {product_name}

    {tickets_text}
    """
    client = Groq()  # or read from env
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # or "llama-3-8b-8192" if you want faster
        messages=[{"role": "user", "content": prompt}]
    )


    return response.choices[0].message.content


def main():
    df = pd.read_csv("tickets_cleaned2.csv")
    grouped = df.groupby("PRODUCT_CATEGORY")
    # grouped_df = df.groupby('PRODUCT_CATEGORY').sum() # Apply an aggregation
    # grouped_df.to_csv("groups_Category.csv", index=False)
    # # Summarize the tickets
    # #summarize_tickets(grouped_df)
    summaries = {}

    for product, tickets in grouped:
        tickets_text = prepare_ticket_narrative(tickets)
        summary = summarize_category(product, tickets_text)
        summaries[product] = summary

    # Save all summaries into a file
    with open("ticket_storytelling_summaries.txt", "w", encoding="utf-8") as f:
        for product, summary in summaries.items():
            f.write(f"===== {product} =====\n{summary}\n\n")








if __name__ == "__main__":
    main()