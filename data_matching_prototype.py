import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load data
data = pd.read_csv('customer_data.csv')

# Define a function to clean and standardize data
def clean_data(row):
    return {
        "name": row['Name'].strip().lower(),
        "email": row['Email'].strip().lower(),
        "address": row['Address'].strip().lower(),
        "phone": row['Phone'].strip()
    }

# Preprocess data
data['Cleaned'] = data.apply(clean_data, axis=1)

# Perform fuzzy matching
def match_records(df, threshold=90):
    matched_pairs = []
    unmatched = []

    for i, row1 in df.iterrows():
        matched = False
        for j, row2 in df.iterrows():
            if i >= j:
                continue

            # Compare key fields with fuzzy matching
            score_name = fuzz.ratio(row1['Cleaned']['name'], row2['Cleaned']['name'])
            score_email = fuzz.ratio(row1['Cleaned']['email'], row2['Cleaned']['email'])
            score_address = fuzz.ratio(row1['Cleaned']['address'], row2['Cleaned']['address'])
            score_phone = fuzz.ratio(row1['Cleaned']['phone'], row2['Cleaned']['phone'])

            avg_score = (score_name + score_email + score_address + score_phone) / 4

            if avg_score > threshold:
                matched_pairs.append((row1['Domain'], row2['Domain'], row1['CustomerID'], row2['CustomerID'], avg_score))
                matched = True

        if not matched:
            unmatched.append(row1)

    return matched_pairs, unmatched

# Perform matching
matched_pairs, unmatched_records = match_records(data)

# Output results
print("Matched Records:")
for match in matched_pairs:
    print(f"Domains: {match[0]} & {match[1]} | IDs: {match[2]} & {match[3]} | Avg. Score: {match[4]:.2f}")

print("\nUnmatched Records:")
for unmatched in unmatched_records:
    print(unmatched)

# Save results to CSV
matched_df = pd.DataFrame(matched_pairs, columns=['Domain1', 'Domain2', 'ID1', 'ID2', 'MatchScore'])
matched_df.to_csv('matched_records.csv', index=False)
