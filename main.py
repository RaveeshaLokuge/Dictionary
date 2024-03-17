import tkinter as tk
from ttkbootstrap import Style, ttk
import requests
from gtts import gTTS
import pygame
from io import BytesIO


def get_definition(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0]['meanings']
            definitions = []
            for meaning in meanings:
                definitions.append(
                    f"• Meaning: {meaning['partOfSpeech']}\nDefinition: {meaning['definitions'][0]['definition']}\n")
            return '\n'.join(definitions)
    return "No definition found."


def speak_definition(definition_text):
    audio_stream = BytesIO()
    tts = gTTS(text=definition_text, lang='en')
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()


def cancel_speaking():
    pygame.mixer.music.stop()


def search_definition():
    word = entry_word.get()
    definition = get_definition(word)
    if definition == "No definition found.":
        definition = "No definition found for the entered word."
    text_output.configure(state='normal')
    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, definition)
    text_output.configure(state='disabled')
    speak_button.grid(row=1, column=0, pady=5)
    cancel_button.grid_remove()


def speak_meaning():
    definition = text_output.get('1.0', tk.END)
    speak_definition(definition)
    speak_button.grid_remove()
    cancel_button.grid(row=1, column=1, pady=5)


def cancel_speak_meaning():
    cancel_speaking()
    cancel_button.grid_remove()
    speak_button.grid(row=1, column=0, pady=5)


root = tk.Tk()
style = Style(theme="flatly")
root.title("Dictionary App")
root.geometry("1280x720")

# Search frame
frame_search = ttk.Frame(root)
frame_search.pack(padx=20, pady=20)

# Label for the word entry field
label_word = ttk.Label(frame_search, text="Enter a word:",
                       font=('TkDefaultFont', 15, 'bold'))
label_word.grid(row=0, column=0, padx=5, pady=5)

# Entry field for the word
entry_word = ttk.Entry(frame_search, width=20, font='TkDefaultFont 15')
entry_word.grid(row=0, column=1, padx=5, pady=5)

# Search button
button_search = ttk.Button(frame_search, text="Search", command=search_definition)
button_search.grid(row=0, column=2, padx=5, pady=5)

# Output frame
frame_output = ttk.Frame(root)
frame_output.pack(padx=20, pady=10)

# Text output field for displaying the definition
text_output = tk.Text(frame_output, height=10, state='disabled',
                      font=('TkDefaultFont', 15))
text_output.grid(row=0, column=0)

# Button to speak the meaning
speak_button = ttk.Button(frame_output, text="Speak", command=speak_meaning)
speak_button.grid(row=1, column=0, pady=5)
speak_button.grid_remove()  # Initially hidden

# Button to cancel speaking
cancel_button = ttk.Button(frame_output, text="Cancel", command=cancel_speak_meaning)
# Initially hidden
cancel_button.grid(row=1, column=1, pady=5)

root.mainloop()
