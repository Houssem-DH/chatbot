import csv
from transformers import pipeline


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


faq_file = "faqs.txt"  
dataset_file = "dataset.csv"  


categories = ["accounts", "security", "cards", "loans", "investments", "general"]


def process_faq_data():
    try:
        
        with open(faq_file, "r") as file:
            lines = file.readlines()
        
        valid_faqs = []
        
        
        for line in lines:
            line = line.strip()
            
            
            if not line:
                continue
            
            
            if line.count(",") < 2:
                print(f"Skipping invalid FAQ format: {line}")
                continue
            
            
            parts = line.split(",", 2)  
            if len(parts) != 3:
                print(f"Skipping invalid FAQ format: {line}")
                continue
            
            question, answer, category = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            
            try:
                result = classifier(question, categories)
                classified_category = result['labels'][0]  
                
                
                with open(dataset_file, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([question, answer, classified_category])
                    print(f"FAQ processed and added to {dataset_file}.")
            except Exception as e:
                print(f"Error classifying FAQ: {e}")
                continue

    except Exception as e:
        print(f"Error reading FAQ file: {e}")


process_faq_data()
