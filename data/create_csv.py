import pandas as pd
import os

# Data
data = {
    'disease': [
        'headache', 'common cold', 'fever', 'cough', 
        'sore throat', 'indigestion', 'stress', 'insomnia'
    ],
    'symptoms': [
        'throbbing pain sensitivity to light',
        'runny nose sneezing congestion',
        'high temperature body aches', 
        'dry cough wet cough chest congestion',
        'pain when swallowing scratchy throat',
        'bloating stomach pain gas',
        'anxiety tension irritability',
        'difficulty sleeping waking up frequently'
    ],
    'remedy': [
        'Apply peppermint oil to temples or drink peppermint tea',
        'Drink ginger tea with honey and lemon',
        'Stay hydrated and take basil tea with honey',
        'Drink turmeric milk or honey with warm water', 
        'Gargle with salt water 3 times daily',
        'Drink peppermint tea or fennel water after meals',
        'Practice deep breathing and drink chamomile tea',
        'Drink warm milk with turmeric before bedtime'
    ],
    'ingredients': [
        'peppermint oil peppermint leaves',
        'ginger honey lemon water',
        'basil leaves water honey', 
        'turmeric milk honey',
        'salt warm water',
        'peppermint leaves fennel seeds water',
        'chamomile tea water',
        'milk turmeric honey'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Save to CSV
df.to_csv('data/home_remedies.csv', index=False)
print("✅ CSV file created successfully at: data/home_remedies.csv")

# Show file info
file_path = 'data/home_remedies.csv'
file_size = os.path.getsize(file_path)
print(f"📁 File size: {file_size} bytes")

# Show first few rows
print("\n📋 Sample data:")
print(df.head(3))