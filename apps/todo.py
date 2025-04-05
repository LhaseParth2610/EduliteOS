from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
import aiml
import csv

# Load math.aiml
kernel = aiml.Kernel()
kernel.learn("math.aiml")
math_data = []
with open("math.aiml", "r") as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        if "<pattern>" in lines[i]:
            question = lines[i].replace("<pattern>", "").replace("</pattern>", "").strip()
            if i + 1 < len(lines) and "<template>" in lines[i + 1]:
                answer = lines[i + 1].replace("<template>", "").replace("</template>", "").strip()
                math_data.append({"question": question, "answer": answer})
        i += 1

# Load CSV files
coding_df = pd.read_csv("coding_facts.csv")
general_df = pd.read_csv("general_facts.csv")

# Combine all data
data = math_data + coding_df.to_dict("records") + general_df.to_dict("records")
dataset = Dataset.from_list(data)

# Tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForQuestionAnswering.from_pretrained("distilbert-base-uncased")

# Preprocess for Q&A (simplified: answer as label, no context)
def preprocess_function(examples):
    encodings = tokenizer(
        examples["question"],
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors="pt"
    )
    # For simplicity, encode answers as labels (not ideal for production, but lightweight)
    answer_encodings = tokenizer(
        examples["answer"],
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors="pt"
    )
    encodings["labels"] = answer_encodings["input_ids"]
    return encodings

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Training arguments (lightweight settings)
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,              # Few epochs for speed
    per_device_train_batch_size=4,   # Small batch for low RAM
    per_device_eval_batch_size=4,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=200,
    save_total_limit=1,              # Keep only latest checkpoint
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune
trainer.train()

# Save for offline use
model.save_pretrained("fine_tuned_distilbert")
tokenizer.save_pretrained("fine_tuned_distilbert")

# Inference script (offline)
def ask_question(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    start_idx = start_scores.argmax()
    end_idx = end_scores.argmax() + 1
    answer_ids = inputs["input_ids"][0][start_idx:end_idx]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
    return answer if answer else "I don’t know that yet."

# Test
print(ask_question("What is a neural network?"))
print(ask_question("What is the capital of France?"))
print(ask_question("What is a Fibonacci sequence?"))