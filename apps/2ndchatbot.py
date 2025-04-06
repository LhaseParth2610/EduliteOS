import customtkinter as ctk
import faiss
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# === Load ===
index = faiss.read_index("model_data/chatbot_index.faiss")
with open("model_data/questions.pkl", "rb") as f:
    questions = pickle.load(f)
with open("model_data/answers.pkl", "rb") as f:
    answers = pickle.load(f)
with open("model_data/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# === Ask ===
def get_answer(query):
    query_vec = vectorizer.transform([query]).toarray().astype('float32')
    _, I = index.search(query_vec, 1)
    return answers[I[0][0]]

# === GUI Setup ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("🎓 EduLite Kids Chatbot 🤖")
app.geometry("800x650")
app.resizable(False, False)

frame = ctk.CTkFrame(app, corner_radius=20, fg_color="#FFF9EC")
frame.pack(padx=20, pady=20, fill="both", expand=True)

title_label = ctk.CTkLabel(
    frame, text="🌟 EduLite AI Chatbot for Kids 🌈",
    font=("Comic Sans MS", 26, "bold"), text_color="#FF5733"
)
title_label.pack(pady=(10, 5))

chatbox = ctk.CTkTextbox(
    frame, wrap="word", height=420, font=("Comic Sans MS", 14),
    fg_color="#FFF", text_color="#333"
)
chatbox.pack(padx=15, pady=(5, 10), fill="both", expand=True)
chatbox.insert("end", "👋 Hi there! I'm your friendly study buddy!\nAsk me anything about Science, GK, Grammar & more!\n\n")
chatbox.configure(state="disabled")

input_frame = ctk.CTkFrame(frame, fg_color="transparent")
input_frame.pack(fill="x", padx=15, pady=(0, 10))

user_input = ctk.CTkEntry(input_frame, placeholder_text="Type your question...", font=("Comic Sans MS", 14), height=40)
user_input.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

def on_ask():
    query = user_input.get().strip()
    if query == "":
        return
    user_input.delete(0, "end")

    chatbox.configure(state="normal")
    chatbox.insert("end", f"\n🧒 You: {query}\n", "user")
    answer = get_answer(query)
    chatbox.insert("end", f"🤖 Bot: {answer}\n", "bot")
    chatbox.configure(state="disabled")
    chatbox.see("end")

button_frame = ctk.CTkFrame(frame, fg_color="transparent")
button_frame.pack(pady=(0, 10), fill="x", padx=15)

ask_button = ctk.CTkButton(button_frame, text="🚀 Ask", command=on_ask)
ask_button.pack(side="left", padx=(0, 10), pady=10)

exit_button = ctk.CTkButton(button_frame, text="❌ Exit", fg_color="#FF4C4C", hover_color="#CC0000", command=app.quit)
exit_button.pack(side="right", pady=10)

chatbox.tag_config("user", foreground="#007FFF")
chatbox.tag_config("bot", foreground="#008000")

app.mainloop()
