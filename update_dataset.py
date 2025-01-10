import os

def update_dataset(faq_file, dataset_file):
    try:
        if not os.path.exists(faq_file):
            print(f"{faq_file} does not exist.")
            return False

        with open(faq_file, "r") as file:
            lines = file.readlines()

        if not lines:
            print("No new FAQs to process.")
            return False

        
        processed_faqs = []
        for line in lines:
            try:
                question, answer = line.strip().split("-", 1)
                question = question.strip()
                answer = answer.strip()

                
                if "account" in question.lower():
                    faq_class = "accounts"
                elif "card" in question.lower():
                    faq_class = "cards"
                else:
                    faq_class = "general"  # Default class

                processed_faqs.append(f"{question},{answer},{faq_class}\n")
            except ValueError:
                print(f"Skipping invalid FAQ format: {line.strip()}")

        
        with open(dataset_file, "a") as dataset:
            dataset.writelines(processed_faqs)

       
        with open(faq_file, "w") as file:
            file.write("")

        print("FAQs successfully added to the dataset.")
        return True
    except Exception as e:
        print(f"Error in update_dataset: {e}")
        return False

