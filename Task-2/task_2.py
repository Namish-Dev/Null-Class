# -*- coding: utf-8 -*-
"""Task-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mXBqMH2OB_08JeyibcclP7maRvIP3WaC
"""

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import datetime
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import time

#  Load Pretrained Model
try:
    model = load_model('bidirectional_translation_model.h5')
except Exception as e:
    print("Model load failed:", e)
    model = None

#  Time Constraint Check
def is_translation_time():
    now = datetime.datetime.now().time()
    start = datetime.time(21, 30)
    end = datetime.time(22, 0)
    return start <= now <= end

#  Preprocess and Postprocess
def preprocess_text(text):
    return text.lower()

def pad(seq, max_len):
    return pad_sequences(seq, maxlen=max_len, padding='post')

def logits_to_text(logits, tokenizer):
    index_to_word = {v: k for k, v in tokenizer.word_index.items()}
    output = ""
    for index in np.argmax(logits, axis=1):
        if index == 0:
            continue
        word = index_to_word.get(index, '')
        if word == 'end_':
            break
        output += word + " "
    return output.strip()

# Voice Recognition
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

#Translation
def translate():
    if not is_translation_time():
        output_label.config(text=" Taking rest, see you tomorrow!")
        return

    input_text = get_voice_input()
    if not input_text:
        output_label.config(text=" Could not understand, please repeat.")
        return

    try:
        cleaned = preprocess_text(input_text)
        seq = english_tokenizer.texts_to_sequences([cleaned])
        padded = pad(seq, max_hindi_sequence_length)
        preds = model.predict(padded)[0]
        translated = logits_to_text(preds, hindi_tokenizer)
        output_label.config(text=f"EN: {input_text}\nHI: {translated}")
    except Exception as e:
        output_label.config(text=f" Error: {e}")

# GUI
root = tk.Tk()
root.title("English to Hindi Voice Translator")
root.geometry("500x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text=" Click Below to Speak", font=("Helvetica", 14)).pack(pady=10)
tk.Button(root, text=" Translate", command=translate, font=("Helvetica", 12)).pack(pady=10)
output_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=480, justify="left")
output_label.pack(pady=20)

root.mainloop()