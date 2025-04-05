import aiml
import csv

# Load CSV files
coding_facts = {}
with open("coding_facts.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        coding_facts[row["question"].lower()] = row["answer"]

general_facts = {}
with open("general_facts.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        general_facts[row["question"].lower()] = row["answer"]

# Initialize AIML kernel
kernel = aiml.Kernel()
kernel.learn("math.aiml")  # 150 math patterns from earlier

# Lookup functions
def get_coding_answer(input_text):
    return coding_facts.get(input_text.lower(), "I don’t know that coding topic yet.")

def get_general_answer(input_text):
    return general_facts.get(input_text.lower(), "I don’t have that general info yet.")

# Chat loop with basic routing
print("Hello! Ask me about math, coding, or general knowledge. Type 'quit' to exit.")
while True:
    user_input = input("> ").lower()
    if user_input == "quit":
        break
    
    # Route based on keywords
    coding_keywords = ["python", "c++", "javascript", "git", "coding", "algorithm", "data structure", "machine learning", "sql", "api"]
    general_keywords = ["what is", "why", "how does", "who", "where", "when", "science", "history", "geography", "capital"]
    
    if any(keyword in user_input for keyword in coding_keywords):
        response = get_coding_answer(user_input)
    elif any(keyword in user_input for keyword in general_keywords):
        response = get_general_answer(user_input)
    else:
        response = kernel.respond(user_input)  # Math patterns
    
    # Fallback
    if not response or response == "":
        response = "I don’t understand that yet. Try asking about math, coding, or general facts!"
    print(response)