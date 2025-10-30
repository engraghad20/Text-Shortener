import tkinter as tk
from tkinter import scrolledtext
import re
from collections import Counter

# دالة التلخيص 
def summarize_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "⚠️ Please enter some text!")
        return

    # تقسيم النص إلى جمل
    sentences = re.split(r'(?<=[.!?]) +', text)
    n_sentences = min(5, len(sentences))  # عدد الجمل في الملخص

    # تكرار الكلمات
    words = re.findall(r'\w+', text.lower())
    freq = Counter(words)

    sentence_scores = {}
    for idx, s in enumerate(sentences):
        score = sum(freq.get(word.lower(),0) for word in re.findall(r'\w+', s))
        # وزن أعلى للجمل في بداية النص
        score += max(0, 5 - idx)
        # وزن للجمل متوسطة الطول
        if 20 <= len(s) <= 200:
            score *= 1.2
        sentence_scores[s] = score

    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n_sentences]
    summary = " ".join(top_sentences)

    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, summary)
    output_text.config(state='normal')  # السماح بالنسخ واللصق

# إعداد نافذة التطبيق
root = tk.Tk()
root.title("Text Shortener")
root.geometry("900x650")
root.resizable(False, False)

# خلفية متدرجة ديناميكية
canvas = tk.Canvas(root, width=900, height=650)
canvas.pack(fill="both", expand=True)
gradient_colors = [(99,20,50), (0,180,255)]  # ألوان متدرجة
def draw_gradient(offset=0):
    canvas.delete("gradient")
    for i in range(650):
        r = int(gradient_colors[0][0] + (gradient_colors[1][0]-gradient_colors[0][0]) * i/650 + offset%50)
        g = int(gradient_colors[0][1] + (gradient_colors[1][1]-gradient_colors[0][1]) * i/650)
        b = int(gradient_colors[0][2] + (gradient_colors[1][2]-gradient_colors[0][2]) * i/650)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 900, i, fill=color, tags="gradient")
    root.after(50, lambda: draw_gradient(offset+1))
draw_gradient()

# إطار داخلي
frame = tk.Frame(canvas, bg="#2c3e50", bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

# عنوان التطبيق
title_label = tk.Label(frame, text="Text Shortener", font=("Helvetica", 28, "bold"),
                       bg="#2c3e50", fg="#ffffff")
title_label.pack(pady=20)

# مربع إدخال النص
input_label = tk.Label(frame, text="Enter your text:", font=("Helvetica", 14, "bold"),
                       bg="#2c3e50", fg="#ffeb3b")
input_label.pack(anchor="w")
input_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=95, height=10,
                                       font=("Helvetica", 12), bg="#3b4a59", fg="#ffffff",
                                       insertbackground='white', bd=0)
input_text.pack(pady=10)
input_text.config(highlightthickness=2, highlightbackground="#ff5722", highlightcolor="#ff5722")

# دعم لصق النصوص (Ctrl+V)
input_text.bind("<Control-v>", lambda e: input_text.event_generate("<<Paste>>"))
input_text.bind("<Control-V>", lambda e: input_text.event_generate("<<Paste>>"))

# تأثير Hover للزر
def on_enter(e):
    summarize_btn['bg'] = '#ff4081'
    summarize_btn['padx'] = 35
    summarize_btn['pady'] = 12
def on_leave(e):
    summarize_btn['bg'] = '#673ab7'
    summarize_btn['padx'] = 30
    summarize_btn['pady'] = 10

# زر التلخيص
summarize_btn = tk.Button(frame, text="Summarize", command=summarize_text,
                          font=("Helvetica", 15, "bold"), bg="#673ab7", fg="white",
                          activebackground="#ff4081", activeforeground="white",
                          bd=5, relief="raised", padx=30, pady=10)
summarize_btn.pack(pady=15)
summarize_btn.bind("<Enter>", on_enter)
summarize_btn.bind("<Leave>", on_leave)

# مربع عرض الملخص
output_label = tk.Label(frame, text="Summarized Text:", font=("Helvetica", 14, "bold"),
                        bg="#2c3e50", fg="#ffeb3b")
output_label.pack(anchor="w")
output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=95, height=10,
                                        font=("Helvetica", 12), bg="#3b4a59", fg="#ffffff",
                                        bd=0)
output_text.pack(pady=10)
output_text.config(state='normal', insertbackground='white', highlightthickness=2,
                   highlightbackground="#ff5722", highlightcolor="#ff5722")

# دعم النسخ واللصق في الملخص
output_text.bind("<Control-c>", lambda e: output_text.event_generate("<<Copy>>"))
output_text.bind("<Control-C>", lambda e: output_text.event_generate("<<Copy>>"))

# تشغيل البرنامج
root.mainloop()
