import tkinter as tk
from tkinter import messagebox, ttk
from gtts import gTTS
from playsound import playsound
import random
import os
from PIL import Image, ImageTk, ImageSequence
import pygame  # background music

PASTEL_BG = "#F8F1FF"
PASTEL_ACCENT = "#B8E1DD"
PASTEL_BTN = "#C4D7E0"
PASTEL_TEXT = "#5A5A5A"

class DyslexiaApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Learning App for Dyslexic Kids")
        master.geometry("600x500")
        master.resizable(False, False)

        # Init pygame mixer
        pygame.mixer.init()
        self.music_path = #"add path"
        self.play_background_music()

        # Animated background
        self.bg_path = #"add path"
        self.bg_label = tk.Label(master)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.animate_background()

        # Foreground frame
        self.ui_frame = tk.Frame(master, bg=PASTEL_BG)
        self.ui_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Assets
        self.listen_path = #"add path"
        self.submit_path = #"add path"
        self.star_path = #"add path"
        self.icon_path = #"add path"
        self.correct_mp3 = #"add path"
        self.wrong_mp3 = #"add path"

        try:
            master.iconbitmap(self.icon_path)
        except:
            print("Icon not loaded.")

        self.levels = ["easy", "medium", "hard"]
        self.username = ""
        self.show_user_screen()

    def play_background_music(self):
        if os.path.exists(self.music_path):
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(0.5)  # Default volume
                pygame.mixer.music.play(-1)  # Loop forever
            except Exception as e:
                print(f"Music error: {e}")

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def animate_background(self):
        self.bg = Image.open(self.bg_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((600, 500))) for frame in ImageSequence.Iterator(self.bg)]

        def update(index):
            frame = self.frames[index]
            self.bg_label.configure(image=frame)
            self.master.after(100, update, (index + 1) % len(self.frames))

        update(0)

    def show_user_screen(self):
        self.clear_screen()
        tk.Label(self.ui_frame, text="Welcome!", font=("Comic Sans MS", 24, "bold"), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=10)
        tk.Label(self.ui_frame, text="Enter your name:", font=("Arial", 16), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=5)

        self.name_entry = tk.Entry(self.ui_frame, font=("Arial", 16), justify='center', bg="white", relief="flat",
                                   highlightthickness=2, highlightbackground="#D6CDEA")
        self.name_entry.pack(pady=10, ipadx=10, ipady=5)

        tk.Label(self.ui_frame, text="Choose Level:", font=("Arial", 14), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=5)
        self.level_var = tk.StringVar(value=self.levels[0])
        self.level_menu = tk.OptionMenu(self.ui_frame, self.level_var, *self.levels)
        self.level_menu.config(font=("Arial", 12), bg=PASTEL_BTN, fg=PASTEL_TEXT, relief="flat")
        self.level_menu["menu"].config(bg="white", fg="black", font=("Arial", 10))
        self.level_menu.pack(pady=5)

        # Volume control
        tk.Label(self.ui_frame, text="Music Volume", font=("Arial", 12), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=5)
        self.volume_slider = tk.Scale(self.ui_frame, from_=0, to=1, resolution=0.1, orient='horizontal',
                                      bg=PASTEL_BG, fg=PASTEL_TEXT, length=200,
                                      command=self.set_music_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=5)

        start_btn = tk.Button(self.ui_frame, text="Start Game", font=("Arial", 14), bg=PASTEL_ACCENT, fg=PASTEL_TEXT,
                              relief="flat", command=self.start_game)
        start_btn.pack(pady=20, ipadx=10, ipady=5)

        start_btn.bind("<Enter>", lambda e: start_btn.config(bg="#A2D2C9"))
        start_btn.bind("<Leave>", lambda e: start_btn.config(bg=PASTEL_ACCENT))

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter your name to continue.")
            return
        self.username = name
        self.current_level = self.levels.index(self.level_var.get())
        self.correct_count = 0
        self.incorrect_count = 0
        self.used_words = []
        self.load_game_ui()

    def load_game_ui(self):
        self.clear_screen()
        self.words = self.load_words(self.levels[self.current_level])
        self.used_words = []
        self.total_words = len(self.words)

        tk.Label(self.ui_frame, text=f"Welcome, {self.username}!", font=("Arial", 14, "bold"), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=5)
        tk.Label(self.ui_frame, text="Type what you hear!", font=("Arial", 20), bg=PASTEL_BG, fg=PASTEL_TEXT).pack(pady=10)

        self.listen_img = self.load_icon(self.listen_path)
        self.submit_img = self.load_icon(self.submit_path)

        self.listen_button = tk.Button(self.ui_frame, image=self.listen_img, command=self.play_word, bd=0, bg=PASTEL_BG)
        self.listen_button.pack(pady=5)

        self.entry = tk.Entry(self.ui_frame, font=("Arial", 18), justify='center', bg="white", relief="flat",
                              highlightthickness=2, highlightbackground="#D6CDEA")
        self.entry.pack(pady=10, ipady=6)
        self.entry.bind("<Return>", lambda event: self.check_word())

        self.submit_button = tk.Button(self.ui_frame, image=self.submit_img, command=self.check_word, bd=0, bg=PASTEL_BG)
        self.submit_button.pack(pady=5)

        self.feedback = tk.Label(self.ui_frame, text="", font=("Arial", 14), bg=PASTEL_BG)
        self.feedback.pack(pady=5)

        self.progress_label = tk.Label(self.ui_frame, text=f"Level: {self.levels[self.current_level].capitalize()}",
                                       font=("Arial", 12), bg=PASTEL_BG, fg=PASTEL_TEXT)
        self.progress_label.pack()

        self.score_label = tk.Label(self.ui_frame, text="✅ 0   ❌ 0", font=("Arial", 12), bg=PASTEL_BG, fg=PASTEL_TEXT)
        self.score_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.ui_frame, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)
        self.progress["maximum"] = self.total_words
        self.progress["value"] = 0

        self.animate_feedback("")
        self.next_word()

    def clear_screen(self):
        for widget in self.ui_frame.winfo_children():
            widget.destroy()

    def load_icon(self, path, size=(50, 50)):
        try:
            image = Image.open(path).resize(size)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def load_words(self, level):
        with open(f"words/{level}.txt", "r") as f:
            return [word.strip() for word in f.readlines() if word.strip()]

    def speak_word(self, word):
        tts = gTTS(text=word, lang='en')
        filename = "word.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

    def play_word(self):
        self.speak_word(self.current_word)

    def check_word(self):
        typed_word = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if typed_word == self.current_word.lower():
            self.correct_count += 1
            self.feedback.config(fg="green")
            self.animate_feedback("✅ Correct!")
            self.play_sound(self.correct_mp3)

            star_img = self.load_icon(self.star_path, size=(40, 40))
            if star_img:
                star_label = tk.Label(self.ui_frame, image=star_img, bg=PASTEL_BG)
                star_label.image = star_img
                star_label.place(x=500, y=10)
                self.master.after(1000, star_label.destroy)
        else:
            self.incorrect_count += 1
            self.feedback.config(fg="red")
            self.animate_feedback(f"❌ It was: {self.current_word}")
            self.play_sound(self.wrong_mp3)

        self.used_words.append(self.current_word)
        self.update_score_label()
        self.progress["value"] = len(self.used_words)
        self.master.after(1500, self.next_word)

    def play_sound(self, path):
        if os.path.exists(path):
            try:
                playsound(path)
            except Exception as e:
                print(f"Sound error: {e}")

    def update_score_label(self):
        self.score_label.config(text=f"✅ {self.correct_count}   ❌ {self.incorrect_count}")

    def next_word(self):
        remaining_words = [word for word in self.words if word not in self.used_words]
        if not remaining_words:
            response = messagebox.askyesno("Great Job!", "You've completed all words!\nGo to next level?")
            if response:
                if self.current_level < len(self.levels) - 1:
                    self.current_level += 1
                    self.correct_count = 0
                    self.incorrect_count = 0
                    self.words = self.load_words(self.levels[self.current_level])
                    self.used_words = []
                    self.total_words = len(self.words)
                    self.progress_label.config(text=f"Level: {self.levels[self.current_level].capitalize()}")
                    self.progress["maximum"] = self.total_words
                    self.progress["value"] = 0
                    self.update_score_label()
                    self.master.after(1000, self.next_word)
                else:
                    messagebox.showinfo("Finished!", "All levels completed!")
                    self.show_user_screen()
            else:
                self.show_user_screen()
            return

        self.current_word = random.choice(remaining_words)
        self.master.after(100, self.play_word)

    def animate_feedback(self, text):
        self.feedback.config(text=text)
        self.feedback.after(1000, lambda: self.feedback.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = DyslexiaApp(root)
    root.mainloop()
