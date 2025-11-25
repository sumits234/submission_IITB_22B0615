import json
import random
from faker import Faker
from num2words import num2words

fake = Faker()

# Entities to generate
LABELS = ["CREDIT_CARD", "PHONE", "EMAIL", "PERSON_NAME", "DATE", "CITY", "LOCATION"]

def add_noise(text):
    # Simulate STT noise
    text = text.replace("@", " at ")
    text = text.replace(".", " dot ")
    text = text.replace("-", " ")
    return text.lower()

def generate_sample(id_num):
    # 1. Select a template and entity
    category = random.choice(LABELS)
    
    if category == "CREDIT_CARD":
        entity_val = fake.credit_card_number()
        # STT often spaces out numbers: 4242 -> four two four two
        spoken_val = " ".join([num2words(int(d)) for d in entity_val if d.isdigit()]) 
        template = [f"my card number is {spoken_val}", f"debit card {spoken_val}"]
        
    elif category == "PHONE":
        entity_val = fake.phone_number()
        spoken_val = " ".join([num2words(int(d)) for d in entity_val if d.isdigit()])
        template = [f"call me at {spoken_val}", f"number is {spoken_val}"]
        
    elif category == "EMAIL":
        entity_val = fake.email()
        spoken_val = add_noise(entity_val)
        template = [f"email is {spoken_val}", f"contact {spoken_val}"]
        
    elif category == "PERSON_NAME":
        entity_val = fake.name()
        spoken_val = entity_val.lower()
        template = [f"my name is {spoken_val}", f"this is {spoken_val} speaking"]
        
    elif category == "DATE":
        entity_val = fake.date()
        spoken_val = entity_val.replace("-", " ")
        template = [f"born on {spoken_val}", f"date is {spoken_val}"]
        
    elif category == "CITY":
        entity_val = fake.city()
        spoken_val = entity_val.lower()
        template = [f"i live in {spoken_val}", f"from {spoken_val}"]
        
    elif category == "LOCATION":
        entity_val = fake.address()
        spoken_val = entity_val.lower().replace("\n", " ")
        template = [f"located at {spoken_val}", f"address is {spoken_val}"]

    text = random.choice(template)
    
    # Very basic substring matching for start/end (Robustness would require better alignment)
    try:
        start_index = text.index(spoken_val)
        end_index = start_index + len(spoken_val)
        
        return {
            "id": f"utt_{id_num:04d}",
            "text": text,
            "entities": [
                {"start": start_index, "end": end_index, "label": category}
            ]
        }
    except:
        return None # Skip if alignment fails

# Generate Data
data_types = [("data/train.jsonl", 800), ("data/dev.jsonl", 150), ("data/test.jsonl", 50)]

for filename, count in data_types:
    print(f"Generating {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        valid_count = 0
        while valid_count < count:
            sample = generate_sample(valid_count)
            if sample:
                json.dump(sample, f)
                f.write("\n")
                valid_count += 1