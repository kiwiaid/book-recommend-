import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# -----------------------------
# Backend imports (UNCHANGED)
# -----------------------------
from src.data_processing import load_and_clean_data
from src.feature_processing import create_tfidf
from src.recommender import build_similarity, recommend_books
from src.gener_recommender import calculate_genre_popularity, recommend_by_genre

# -----------------------------
# Load model ONCE
# -----------------------------
DATA_PATH = "data/contentBased.csv"

df = load_and_clean_data(DATA_PATH)
tfidf_matrix = create_tfidf(df)
cosine_sim = build_similarity(tfidf_matrix)
genre_popularity = calculate_genre_popularity(df)

# -----------------------------
# Main App Window
# -----------------------------
root = tk.Tk()
root.title("📚 Book Recommendation System")
root.geometry("900x600")
root.configure(bg="#eef2f7")

# -----------------------------
# Colors
# -----------------------------
BG = "#eef2f7"
CARD = "#ffffff"
PRIMARY = "#4f46e5"
HOVER = "#4338ca"
TEXT = "#111827"
MUTED = "#6b7280"

# -----------------------------
# Styling
# -----------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel",
                background=BG,
                foreground=TEXT,
                font=("Segoe UI", 11))

style.configure("Header.TLabel",
                font=("Segoe UI", 22, "bold"),
                foreground=TEXT,
                background=BG)

style.configure("Card.TFrame",
                background=CARD)

style.configure("Accent.TButton",
                font=("Segoe UI", 11, "bold"),
                padding=12,
                background=PRIMARY,
                foreground="white",
                borderwidth=0)

style.map("Accent.TButton",
          background=[("active", HOVER)])

# -----------------------------
# Header
# -----------------------------
header = ttk.Frame(root)
header.pack(fill="x", pady=20)

title = ttk.Label(header,
                  text="📚 Book Recommendation System",
                  style="Header.TLabel")
title.pack()

subtitle = ttk.Label(header,
                     text="Smart content & genre based book discovery",
                     foreground=MUTED)
subtitle.pack()

# -----------------------------
# Main Content
# -----------------------------
content = ttk.Frame(root)
content.pack(expand=True, fill="both", padx=30, pady=10)

# -----------------------------
# Input Card
# -----------------------------
input_card = ttk.Frame(content, style="Card.TFrame")
input_card.pack(fill="x", pady=10)
input_card.configure(padding=20)

ttk.Label(input_card, text="Enter a book you like").pack(anchor="w")

book_entry = ttk.Entry(input_card, font=("Segoe UI", 12))
book_entry.pack(fill="x", pady=8)

# -----------------------------
# Recommendation Type
# -----------------------------
rec_var = tk.StringVar(value="content")

radio_frame = ttk.Frame(input_card)
radio_frame.pack(pady=5)

ttk.Radiobutton(radio_frame,
                text="Content-Based",
                variable=rec_var,
                value="content").pack(side="left", padx=15)

ttk.Radiobutton(radio_frame,
                text="Genre-Based",
                variable=rec_var,
                value="genre").pack(side="left", padx=15)

# -----------------------------
# Status Label
# -----------------------------
status_label = ttk.Label(
    input_card,
    text="✨ Ready to recommend your next favorite book",
    font=("Segoe UI", 9),
    foreground=MUTED
)
status_label.pack(pady=5)

# -----------------------------
# Recommendation Function
# -----------------------------
def get_recommendations():
    book = book_entry.get().strip()

    if not book:
        messagebox.showwarning("Input Error", "Please enter a book name")
        return

    status_label.config(text="🔎 Searching recommendations...")
    root.update_idletasks()

    output.delete("1.0", tk.END)

    if rec_var.get() == "content":
        results = recommend_books(book, df, cosine_sim)
        title = f"📖 Content-based recommendations for '{book}'\n\n"
    else:
        results = recommend_by_genre(book, df)
        title = f"🎭 Genre-based recommendations for '{book}'\n\n"

    if isinstance(results, str):
        output.insert(tk.END, results)
        status_label.config(text="❌ Book not found")
        return

    output.insert(tk.END, title)

    for r in results:
        output.insert(
            tk.END,
            f"📘 {r['Book']}\n"
            f"👤 {r['Author']}\n"
            f"⭐ Rating: {r['Avg_Rating']}\n"
            f"💡 {r['Reason']}\n\n"
        )

    status_label.config(text="✅ Recommendations ready")

# -----------------------------
# Interactive Button
# -----------------------------
def on_enter(e):
    recommend_btn.configure(cursor="hand2")

def on_leave(e):
    recommend_btn.configure(cursor="")

recommend_btn = ttk.Button(
    input_card,
    text="🔍 Get Recommendations",
    style="Accent.TButton",
    command=get_recommendations
)
recommend_btn.pack(pady=12)

recommend_btn.bind("<Enter>", on_enter)
recommend_btn.bind("<Leave>", on_leave)

# -----------------------------
# Results Card
# -----------------------------
results_card = ttk.Frame(content, style="Card.TFrame")
results_card.pack(expand=True, fill="both", pady=15)
results_card.configure(padding=15)

output = ScrolledText(results_card,
                      font=("Segoe UI", 10),
                      wrap=tk.WORD,
                      height=15,
                      relief="flat")
output.pack(expand=True, fill="both")

# -----------------------------
# Footer
# -----------------------------
footer = ttk.Label(
    root,
    text="Recommede Me • Machine Learning Project",
    font=("Segoe UI", 9),
    foreground=MUTED,
    background=BG
)
footer.pack(pady=8)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()
