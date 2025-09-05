import pandas as pd
import re

class MedicineBot:
    def __init__(self, csv_path='data/home_remedies.csv'):
        self.df = pd.read_csv(csv_path)
    
    def find_remedy(self, symptom_input):
        try:
            symptom_input = symptom_input.lower()
            
            # Simple exact matching
            for index, row in self.df.iterrows():
                symptoms = row['symptoms'].lower()
                
                # Check if any word matches
                input_words = symptom_input.split()
                symptom_words = symptoms.split()
                
                for word in input_words:
                    if word in symptom_words:
                        return {
                            'disease': row['disease'],
                            'remedy': row['remedy'],
                            'ingredients': row['ingredients'],
                            'confidence': 0.9
                        }
            
            return self.get_fallback_response()
            
        except Exception as e:
            print(f"Error: {e}")
            return self.get_fallback_response()
    
    def get_fallback_response(self):
        return {
            'disease': 'Unknown',
            'remedy': 'Please consult a doctor for proper diagnosis.',
            'ingredients': 'Professional medical advice recommended',
            'confidence': 0.0
        }
    