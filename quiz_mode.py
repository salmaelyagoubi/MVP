import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import os
import pygame
import pyttsx3
import cv2
from PIL import Image, ImageTk
import importlib

class SignLanguageApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The ASL App")
        self.root.geometry("900x700")
        
                

        # Define color scheme
        self.BG_COLOR = "#F0F4F8"  # Light grayish blue
        self.ACCENT_COLOR = "#4A90E2"  # Blue
        self.TEXT_COLOR = "#333333"  # Dark gray
        self.BUTTON_COLOR = "#5CB85C"  # Green

        self.root.configure(bg=self.BG_COLOR)
        
        pygame.init()  # Initialize all pygame modules
        pygame.mixer.init()  # Specifically initialize the mixer module 
        
        self.play_welcome_sound()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.BG_COLOR)
        self.style.configure("TButton", font=("Arial", 12), padding=5, background=self.BUTTON_COLOR)
        self.style.configure("TLabel", font=("Arial", 12), background=self.BG_COLOR, foreground=self.TEXT_COLOR)
        self.style.configure("LargeButton.TButton", font=("Arial", 14, "bold"), padding=10, background=self.BUTTON_COLOR)
        
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except Exception as e:
            print(f"Failed to initialize text-to-speech engine: {e}")
            self.engine = None


        self.categories = {
            "Beginner": {
                "Numbers": [
                    {"image": "1.png", "answer": "One", "description": "Extend index finger upward."},
                    {"image": "2.png", "answer": "Two", "description": "Extend index and middle fingers upward."}
                ],
                "Letters": [
                    {"image": "A.png", "answer": "A", "description": "Fist with thumb on side."},
                    {"image": "B.png", "answer": "B", "description": "Open palm, fingers straight up."}
                ]
            },
            "Intermediate": {
                "Animals": [
                    {"image": "cat.png", "answer": "Cat", "description": "Mime stroking whiskers."},
                    {"image": "dog.png", "answer": "Dog", "description": "Pat leg and snap fingers."}
                ],
                "Food": [
                    {"image": "apple.png", "answer": "Apple", "description": "Knuckle to cheek, twist twice."},
                    {"image": "banana.png", "answer": "Banana", "description": "Mime peeling a banana."}
                ]
            },
            "Advanced": {
                "Greetings": [
                    {"image": "hello.png", "answer": "Hello", "description": "Salute from forehead."},
                    {"image": "goodbye.png", "answer": "Goodbye", "description": "Wave palm outward."}
                ],
                "Colors": [
                    {"image": "red.png", "answer": "Red", "description": "Touch lips, move down."},
                    {"image": "blue.png", "answer": "Blue", "description": "Shake 'B' sign sideways."}
                ]
            }
        }

        self.placement_questions = [
            {"image": "A.png", "answer": "A", "options": ["A", "B", "C", "D"]},
            {"image": "L.PNG", "answer": "L", "options": ["K", "L", "M", "N"]},
            {"image": "help.png", "answer": "Help", "options": ["Hello", "Help", "Happy", "Home"]},
            {"image": "i love you.png", "answer": "I love you", "options": ["I love you", "Thank you", "Good morning", "How are you"]},
            {"image": "again.png", "answer": "Again", "options": ["Again", "Always", "After", "About"]}
        ]

        self.favorites = set()
        self.slow_mode = False

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.BG_COLOR)
        self.style.configure("MenuButton.TButton", font=("Arial", 14, "bold"), padding=10, background="#4CAF50", foreground="white")
        self.style.map("MenuButton.TButton",
                       background=[('active', '#45a049')],
                       relief=[('pressed', 'sunken')])

        self.create_main_menu()


    def switch_to_main_app(self):
        self.root.destroy()
        main_app = importlib.import_module("final_pred")
        app = main_app.Application()
        app.root.mainloop()
        
    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(main_frame, text="The ASL App", font=("Arial", 36, "bold"), foreground=self.ACCENT_COLOR)
        title_label.pack(pady=20)

        description = "Learn conversational ASL with many signs and phrases. Easy navigation, multiple signers, and interactive features make learning accessible and fun."
        desc_label = ttk.Label(main_frame, text=description, wraplength=600, justify="center", font=("Arial", 12))
        desc_label.pack(pady=10)

        image_path = os.path.join(os.path.dirname(__file__), "logo.png")
        img = Image.open(image_path)
        img = img.resize((150, 150), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(img)
        logo_label = ttk.Label(main_frame, image=self.logo_image, background=self.BG_COLOR)
        logo_label.pack(pady=20)

        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=20)

        buttons = [
            ("Beginner", lambda: self.show_categories("Beginner")),
            ("Intermediate", lambda: self.show_categories("Intermediate")),
            ("Advanced", lambda: self.show_categories("Advanced")),
            ("Placement Test", self.start_placement_test),
            ("Categories", self.show_all_categories),
            ("Favorites", self.show_favorites),
            ("Games", self.show_games),
            ("Real-Time", self.switch_to_main_app)
        ]

        colors = ["#4CAF50", "#F44336", "#2196F3", "#FF9800", "#9C27B0", "#00BCD4", "#795548", "#607D8B", "#E91E63"]

        for i, (text, command) in enumerate(buttons):
            canvas = tk.Canvas(button_frame, width=150, height=50, highlightthickness=0)
            canvas.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            color = colors[i]
            btn = canvas.create_rounded_rectangle(0, 0, 150, 50, radius=25, fill=color)
            canvas.create_text(75, 25, text=text, fill="white", font=("Arial", 12, "bold"))
            
            canvas.tag_bind(btn, "<Button-1>", lambda e, cmd=command: cmd())
            canvas.tag_bind(btn, "<Enter>", lambda e, c=canvas, col=color: c.itemconfig(btn, fill=self.lighten_color(col)))
            canvas.tag_bind(btn, "<Leave>", lambda e, c=canvas, col=color: c.itemconfig(btn, fill=col))

        # Ensure buttons expand to fill space
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        for i in range(3):
            button_frame.rowconfigure(i, weight=1)
            
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

            
    def lighten_color(self, color):
        # Convert color to RGB
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        # Lighten
        r, g, b = [min(255, c + 20) for c in (r, g, b)]
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def show_options(self):
        messagebox.showinfo("Options", "Options menu is not implemented yet.")
        
    
        
    def show_all_categories(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="All Categories", font=("Arial", 24, "bold"), foreground="#4B0082").pack(pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        row = 0
        col = 0
        for level, categories in self.categories.items():
            for category in categories:
                ttk.Button(button_frame, text=f"{level} - {category}", command=lambda l=level, c=category: self.start_category(l, c), 
                        style="LargeButton.TButton").grid(row=row, column=col, pady=10, padx=20, sticky="ew")
                col += 1
                if col > 1:
                    col = 0
                    row += 1

        ttk.Button(main_frame, text="Back to Main Menu", command=self.create_main_menu, 
                style="LargeButton.TButton").pack(pady=20)
        

    
    def play_welcome_sound(self):
        try:
            pygame.mixer.music.load("welcome.wav")
            pygame.mixer.music.play()
            # Schedule the creation of the main menu after 3 seconds
            self.root.after(3000, self.create_main_menu)
        except Exception as e:
            print(f"Failed to play welcome sound: {e}")
            # If sound fails, create the main menu immediately
            self.create_main_menu()
    def show_games(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#4ECCA3")

        top_frame = ttk.Frame(self.root, style="TopFrame.TFrame")
        top_frame.pack(fill="x", pady=(20, 10))

        back_button = ttk.Button(top_frame, text="< Back", command=self.create_main_menu, style="Back.TButton")
        back_button.pack(side="left", padx=20)

        title_label = ttk.Label(top_frame, text="Play time", font=("Arial", 24, "bold"), foreground="white", background="#4ECCA3")
        title_label.pack(side="right", padx=20)

        game_frame = ttk.Frame(self.root, style="GameFrame.TFrame")
        game_frame.pack(expand=True, fill="both", padx=20, pady=20)

        game_items = [
            "Ball", "Balloon", "Bike", "Airplane"
        ]

        self.game_images = []
        for i, item in enumerate(game_items):
            frame = ttk.Frame(game_frame, style="ItemFrame.TFrame")
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")

            image_path = os.path.join(os.path.dirname(__file__), f"{item.lower()}.png")
            try:
                img = Image.open(image_path)
                img.thumbnail((200, 200))  # Resize image while maintaining aspect ratio
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                photo = None

            if photo:
                canvas = tk.Canvas(frame, width=photo.width(), height=photo.height(), highlightthickness=0, bg="#4ECCA3")
                canvas.pack(expand=False)
                canvas.create_image(0, 0, image=photo, anchor="nw")
                self.game_images.append(photo)
            
            text_label = ttk.Label(frame, text=item, font=("Arial", 14), background="#4ECCA3", foreground="white")
            text_label.pack(side="top", pady=(5, 0))

            play_button = ttk.Button(frame, text="▶ Play", command=lambda i=item: self.play_video(i), style="Play.TButton")
            play_button.pack(side="bottom", pady=(5, 10))

        # Configure grid
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(1, weight=1)
        for i in range(4):
            game_frame.rowconfigure(i, weight=1)

        # Update styles
        self.style.configure("TopFrame.TFrame", background="#4ECCA3")
        self.style.configure("GameFrame.TFrame", background="#4ECCA3")
        self.style.configure("ItemFrame.TFrame", background="#4ECCA3")
        self.style.configure("Back.TButton", font=("Arial", 12), background="#4ECCA3", foreground="white")
        self.style.configure("Play.TButton", font=("Arial", 12), background="#5CB85C", foreground="white")
        self.style.map("Play.TButton", background=[('active', '#4CAF50')])
    def play_video(self, item):
        video_path = os.path.join(os.path.dirname(__file__), f"{item.lower()}.mp4")
        if not os.path.exists(video_path):
            messagebox.showerror("Error", f"Video file not found: {item.lower()}.mp4")
            return

        # Create a new top-level window for the video
        video_window = tk.Toplevel(self.root)
        video_window.title(f"ASL Sign for {item}")
        video_window.geometry("640x480")

        video_frame = ttk.Frame(video_window)
        video_frame.pack(expand=True, fill="both")

        video_label = ttk.Label(video_frame)
        video_label.pack(expand=True, fill="both")

        cap = cv2.VideoCapture(video_path)

        def play():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                video_label.config(image=photo)
                video_label.image = photo
                video_window.after(33, play)  # About 30 fps
            else:
                cap.release()
                video_window.destroy()

        play()

    def return_to_games(self):
        # Remove the video frame
        if hasattr(self, 'video_frame'):
            self.video_frame.destroy()
        
        # Show the game frame again
        self.game_frame.pack(pady=20)
    
    def show_categories(self, level):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text=f"{level} Categories", font=("Arial", 24, "bold"), foreground="#4B0082").pack(pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        for category in self.categories[level]:
            ttk.Button(button_frame, text=category, command=lambda l=level, c=category: self.start_category(l, c), 
                    style="LargeButton.TButton").pack(pady=10, padx=20, fill="x")

        ttk.Button(main_frame, text="Back to Main Menu", command=self.create_main_menu, 
                style="LargeButton.TButton").pack(pady=20)

    def start_category(self, level, category):
        self.current_level = level
        self.current_category = category
        self.flashcards = self.categories[level][category]
        self.current_flashcard_index = 0
        self.create_flashcard_widgets(f"{level} - {category}")
        self.show_flashcard()

    def show_favorites(self):
        if not self.favorites:
            messagebox.showinfo("Favorites", "You haven't added any favorites yet.")
            return

        self.flashcards = [card for level in self.categories.values() 
                           for category in level.values()
                           for card in category if card['answer'] in self.favorites]
        self.current_flashcard_index = 0
        self.create_flashcard_widgets("Favorites")
        self.show_flashcard()

    def toggle_slow_mode(self):
        self.slow_mode = not self.slow_mode
        messagebox.showinfo("Slow Mode", f"Slow mode is now {'On' if self.slow_mode else 'Off'}")

    def start_placement_test(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.placement_score = 0
        self.current_placement_question = 0

        self.create_placement_test_widgets()
        self.load_placement_question()

    def create_placement_test_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(main_frame, text="Placement Test", font=("Arial", 22, "bold"), foreground="#4B0082")
        title_label.pack(pady=10)

        self.image_label = ttk.Label(main_frame)
        self.image_label.pack(pady=10)

        self.option_frame = ttk.Frame(main_frame)
        self.option_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(2):
            for j in range(2):
                btn = tk.Button(self.option_frame, text="", width=20, height=2, font=("Arial", 12),
                                command=lambda idx=i*2+j: self.check_placement_answer(idx),
                                relief=tk.RAISED, bg="#F0F0F0", activebackground="#D0D0D0")
                btn.grid(row=i, column=j, padx=10, pady=10)
                self.option_buttons.append(btn)

    def load_placement_question(self):
        if self.current_placement_question >= len(self.placement_questions):
            self.finish_placement_test()
            return

        question = self.placement_questions[self.current_placement_question]
        image_path = os.path.join(os.path.dirname(__file__), question["image"])
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.LANCZOS)
        self.imgtk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.imgtk)

        options = question["options"]
        random.shuffle(options)
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, bg="#F0F0F0", state=tk.NORMAL)

    def check_placement_answer(self, index):
        selected_answer = self.option_buttons[index].cget("text")
        correct_answer = self.placement_questions[self.current_placement_question]["answer"]

        if selected_answer == correct_answer:
            self.placement_score += 1
            self.option_buttons[index].config(bg="lightgreen")
            self.speak("Correct! Great job!")
        else:
            self.option_buttons[index].config(bg="lightcoral")
            for btn in self.option_buttons:
                if btn.cget("text") == correct_answer:
                    btn.config(bg="lightgreen")
            self.speak("That's not quite right. Keep practicing!")

        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)

        self.root.after(2000, self.next_placement_question)

    def next_placement_question(self):
        self.current_placement_question += 1
        self.load_placement_question()

    def finish_placement_test(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        if self.placement_score <= 1:
            recommended_level = "Beginner"
        elif self.placement_score <= 3:
            recommended_level = "Intermediate"
        else:
            recommended_level = "Advanced"

        ttk.Label(main_frame, text="Placement Test Results", font=("Arial", 22, "bold"), foreground="#4B0082").pack(pady=10)
        ttk.Label(main_frame, text=f"Score: {self.placement_score}/5", font=("Arial", 18)).pack(pady=10)
        ttk.Label(main_frame, text=f"Recommended Level: {recommended_level}", font=("Arial", 18, "bold"), foreground="#008080").pack(pady=10)
        ttk.Button(main_frame, text="Start Flashcards", command=lambda: self.show_categories(recommended_level), style="LargeButton.TButton").pack(pady=10)
        ttk.Button(main_frame, text="Back to Main Menu", command=self.create_main_menu, style="LargeButton.TButton").pack(pady=10)

    def create_flashcard_widgets(self, category):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text=f"{category} Flashcards", font=("Arial", 22, "bold"), foreground=self.ACCENT_COLOR).pack(pady=10)

        image_frame = ttk.Frame(main_frame, style="TFrame")
        image_frame.pack(pady=10)
        image_frame.configure(style="Card.TFrame")
        self.style.configure("Card.TFrame", background="white", relief="raised", borderwidth=2)

        self.image_label = ttk.Label(image_frame, background="white")
        self.image_label.pack(padx=10, pady=10)

        self.answer_label = ttk.Label(main_frame, text="", font=("Arial", 18, "bold"), foreground=self.ACCENT_COLOR)
        self.answer_label.pack(pady=5)

        self.description_label = ttk.Label(main_frame, text="", font=("Arial", 14), wraplength=600, justify="center")
        self.description_label.pack(pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        buttons = [
            ("Previous", self.previous_flashcard),
            ("Speak", self.speak_flashcard),
            ("Next", self.next_flashcard),
            ("Favorite", self.toggle_favorite)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command, style="LargeButton.TButton").pack(side=tk.LEFT, padx=10)

        ttk.Button(main_frame, text="Back to Categories", command=lambda: self.show_categories(self.current_level), style="LargeButton.TButton").pack(pady=10)
        ttk.Button(main_frame, text="Back to Main Menu", command=self.create_main_menu, style="LargeButton.TButton").pack(pady=5)

    def show_flashcard(self):
            flashcard = self.flashcards[self.current_flashcard_index]
            image_path = os.path.join(os.path.dirname(__file__), flashcard["image"])
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.LANCZOS)
            self.imgtk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.imgtk)
            self.answer_label.config(text=flashcard["answer"])
            self.description_label.config(text=flashcard["description"])

    def previous_flashcard(self):
        if self.current_flashcard_index > 0:
            self.current_flashcard_index -= 1
            self.show_flashcard()

    def next_flashcard(self):
        if self.current_flashcard_index < len(self.flashcards) - 1:
            self.current_flashcard_index += 1
            self.show_flashcard()

    def speak_flashcard(self):
        flashcard = self.flashcards[self.current_flashcard_index]
        text_to_speak = f"{flashcard['answer']}. {flashcard['description']}"
        if self.slow_mode:
            text_to_speak = '. '.join(text_to_speak.split()) # Add pauses between words
        self.speak(text_to_speak)

    def toggle_favorite(self):
        current_flashcard = self.flashcards[self.current_flashcard_index]
        if current_flashcard["answer"] in self.favorites:
            self.favorites.remove(current_flashcard["answer"])
            messagebox.showinfo("Favorites", f"Removed {current_flashcard['answer']} from favorites")
        else:
            self.favorites.add(current_flashcard["answer"])
            messagebox.showinfo("Favorites", f"Added {current_flashcard['answer']} to favorites")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def run(self):
        self.root.mainloop()
        
    def on_enter(self, button):
        style = ttk.Style()
        style.configure("MenuButton.TButton.active", background="your_color", foreground="your_color")

    def on_leave(self, button):
        style = ttk.Style()
        style.configure("MenuButton.TButton.active", background="your_color", foreground="your_color")
    
    tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

if __name__ == "__main__":
    app = SignLanguageApp()
    app.run()
    