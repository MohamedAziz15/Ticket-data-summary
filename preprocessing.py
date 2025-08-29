import pandas as pd

def preprocess_tickets(file_path: str = "Ticket_Data.txt"):
    """
    Preprocess the ticket data by filtering specific service categories
    and mapping them to product categories.
    """
    # Step 1: Read the text file (comma-separated like your sample)
    df = pd.read_csv("Ticket_Data.txt")

    # Step 2: Define allowed categories
    allowed_categories = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']

    # Step 3: Filter data
    filtered_df = df[df['SERVICE_CATEGORY'].isin(allowed_categories)]

    # Step 4: Create category → product mapping
    category_product_map = {
        'KAI': 'Broadband',
        'NET': 'Broadband',
        'KAV': 'Voice',
        'KAD': 'TV',
        'GIGA': 'GIGA',
        'VOD': 'VOD'
    }

    # Step 5: Add new column with mapped product
    filtered_df['PRODUCT_CATEGORY'] = filtered_df['SERVICE_CATEGORY'].map(category_product_map)

    # Step 6: Save cleaned and mapped data
    filtered_df.to_csv("tickets_cleaned2.csv", index=False)
    filtered_df.to_excel("tickets_cleaned.xlsx", index=False)

    print("✅ Tickets cleaned and mapped successfully!")

    return filtered_df



