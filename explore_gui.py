import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import os
import math

# ========== PERSONALIZATION SETTINGS ========== 
YOUR_NAME = "Kushal"
PARTNER_NAME = "Kushu"
PRIMARY_COLOR = "#FF69B4"  # Bright pink
SECONDARY_COLOR = "#FFC1CC"  # Light pink
FONT_STYLE = "Comic Sans MS"  # Romantic font

# ========== MUSIC SETUP ========== 
def setup_music():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("romantic_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except pygame.error as e:
        print(f"Music error: {e}")
        print("Could not load music. Please ensure the 'romantic_music.mp3' file is in the correct directory.")

# ========== IMAGE HANDLING ========== 
def load_image_safe(path):
    try:
        img = Image.open(path)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Image error: {e}")
        img = Image.new('RGB', (800, 600), PRIMARY_COLOR)  # Fallback to solid background if image fails
        return ImageTk.PhotoImage(img)

# ========== ENHANCED HEART ANIMATION ========== 
class HeartAnimator:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.hearts = []
        self.symbols = ["❤️", "💖", "💘", "💝", "💓", "💗", "💞", "💌", "💫"]
        self.screen_width = self.root.winfo_width()
        self.screen_height = self.root.winfo_height()
        
        # Heart colors - various shades of pink/red
        self.heart_colors = [
            "#FF69B4", "#FF1493", "#DB7093", "#FFC0CB", 
            "#FFB6C1", "#FF82AB", "#FF34B3", "#FF00FF"
        ]
        self.heart_creation_allowed = False

    def create_heart(self):
        # Check if heart creation is allowed
        if not self.heart_creation_allowed:
            return
        
        # Get current window dimensions in case of resize
        self.screen_width = self.root.winfo_width()
        self.screen_height = self.root.winfo_height()
        
        # Start from random position at the bottom (just below visible area)
        x = random.randint(20, self.screen_width - 20)
        y = self.screen_height + 20  # Start below the window
        size = random.randint(20, 36)  # Larger size range
        
        # Random properties for each heart
        symbol = random.choice(self.symbols)
        color = random.choice(self.heart_colors)
        speed = random.uniform(1.5, 3.5)  # Floating speed
        wiggle_amount = random.uniform(0.5, 2.0)  # Horizontal movement amount
        rotation_speed = random.uniform(-2, 2)  # For slight rotation effect
        
        heart = tk.Label(
            self.root,
            text=symbol,
            font=("Arial", size),
            bg='white',
            fg=color,
            bd=0
        )
        heart.place(x=x, y=y)
        
        # Store heart properties
        heart_data = {
            "widget": heart,
            "x": x,
            "y": y,
            "speed": speed,
            "wiggle_amount": wiggle_amount,
            "wiggle_counter": random.uniform(0, 6.28),  # Random starting point for sine wave
            "rotation": 0,
            "rotation_speed": rotation_speed,
            "size": size
        }
        
        self.hearts.append(heart_data)
        self.animate_heart(heart_data)

    def animate_heart(self, heart_data):
        if not heart_data["widget"].winfo_exists():
            self.hearts.remove(heart_data)
            return

        # Update vertical position (float upwards)
        heart_data["y"] -= heart_data["speed"]
        
        # Update horizontal position (gentle wiggle)
        heart_data["wiggle_counter"] += 0.1
        x_offset = math.sin(heart_data["wiggle_counter"]) * heart_data["wiggle_amount"]
        
        # Update rotation
        heart_data["rotation"] += heart_data["rotation_speed"]
        
        # Apply movement (no font change)
        new_x = heart_data["x"] + x_offset
        heart_data["widget"].place(
            x=new_x,
            y=heart_data["y"]
        )
        
        # Remove heart when it moves off-screen at the top
        if heart_data["y"] < -50:
            heart_data["widget"].destroy()
            self.hearts.remove(heart_data)
        else:
            # Continue animation
            self.root.after(30, lambda: self.animate_heart(heart_data))

    def start(self):
        # Only start heart creation once animation is allowed
        self.heart_creation_allowed = True
        self.create_heart()
        # Random interval between heart creation for organic feel
        self.root.after(random.randint(300, 700), self.start)

    def stop_heart_creation(self):
        # Stop the heart creation when needed
        self.heart_creation_allowed = False

    def clear_hearts(self):
        # Clear all hearts from the screen
        for heart in self.hearts:
            heart["widget"].destroy()
        self.hearts = []

# ========== MAIN APPLICATION ========== 
class LoveApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_background()
        self.setup_content()
        
        # Initialize heart_animator after content is set up
        self.heart_animator = HeartAnimator(self.root, self.canvas)
        
        # Set up music after initializing the animator
        setup_music()
        
        # Create the replay button early
        self.replay_button = self.create_replay_button()
        self.replay_button.place(x=750, y=550)  # Position at the bottom-right corner
        
        # Start heart animation after window is ready
        self.root.after(1000, self.heart_animator.start)

    def setup_window(self):
        self.root.title(f"{YOUR_NAME}'s Love Message")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        
    def setup_background(self):
        # Load and display the background image
        self.bg_image = load_image_safe("romantic_background.jpg")  # Ensure the image exists in your directory
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Make sure the background takes up the whole window
        
    def setup_content(self):
        # Canvas with smaller size
        self.canvas = tk.Canvas(
            self.root,
            width=300,  # Reduced size
            height=120,  # Reduced size
            bg=SECONDARY_COLOR,
            highlightthickness=0
        )
        
        # Draw a custom rounded rectangle
        self.create_rounded_rectangle(self.canvas, 10, 10, 290, 110, 20, PRIMARY_COLOR, SECONDARY_COLOR)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        
        self.message_label = tk.Label(
            self.canvas,
            text=f"{PARTNER_NAME}, will you explore my heart with me? 💖",
            bg=SECONDARY_COLOR,
            fg=PRIMARY_COLOR,  # Bright pink font color
            font=(FONT_STYLE, 14, 'bold'),
            wraplength=270
        )
        self.message_label.pack(pady=(30, 20))
        
        button_frame = tk.Frame(self.canvas, bg=SECONDARY_COLOR)
        button_frame.pack(pady=10)
        
        button_style = {
            'bg': PRIMARY_COLOR,
            'fg': 'white',
            'font': (FONT_STYLE, 12, 'bold'),
            'activebackground': '#FF1493',
            'relief': 'raised',
            'borderwidth': 3,
            'padx': 20,
            'pady': 8
        }

        self.yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=self.on_yes,
            **button_style
        )
        self.yes_button.pack(side='left', padx=20, ipadx=10)
        
        self.absolutely_button = tk.Button(
            button_frame,
            text="Absolutely!",
            command=self.on_absolutely,
            **button_style
        )
        self.absolutely_button.pack(side='right', padx=20, ipadx=10)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, outline, fill):
        """Draw a rounded rectangle on the canvas"""
        # Top-left corner
        canvas.create_oval(x1, y1, x1 + radius*2, y1 + radius*2, outline=outline, fill=fill)
        # Top-right corner
        canvas.create_oval(x2 - radius*2, y1, x2, y1 + radius*2, outline=outline, fill=fill)
        # Bottom-left corner
        canvas.create_oval(x1, y2 - radius*2, x1 + radius*2, y2, outline=outline, fill=fill)
        # Bottom-right corner
        canvas.create_oval(x2 - radius*2, y2 - radius*2, x2, y2, outline=outline, fill=fill)

        # Top edge
        canvas.create_rectangle(x1 + radius, y1, x2 - radius, y1 + radius, outline=outline, fill=fill)
        # Bottom edge
        canvas.create_rectangle(x1 + radius, y2 - radius, x2 - radius, y2, outline=outline, fill=fill)
        # Left edge
        canvas.create_rectangle(x1, y1 + radius, x1 + radius, y2 - radius, outline=outline, fill=fill)
        # Right edge
        canvas.create_rectangle(x2 - radius, y1 + radius, x2, y2 - radius, outline=outline, fill=fill)

    def on_yes(self):
        print("Yes button clicked")  # Debugging print statement
        self.create_heart_burst()
        self.message_label.config(text=f"I knew you'd say yes, {PARTNER_NAME}! 😊")
        self.remove_buttons()
        self.show_next_button()

    def on_absolutely(self):
        print("Absolutely button clicked")  # Debugging print statement
        self.create_heart_burst()
        self.message_label.config(text=f"My heart belongs to you, {PARTNER_NAME} 💘")
        self.remove_buttons()
        self.root.after(2000, self.show_final_message)

    def remove_buttons(self):
        # Hide the buttons after one is clicked
        self.yes_button.pack_forget()
        self.absolutely_button.pack_forget()

    def create_heart_burst(self):
        # Trigger a burst of hearts from the bottom of the screen
        for _ in range(10):  # Reduce the burst size to 10
            self.heart_animator.create_heart()

    def show_next_button(self):
        next_button = tk.Button(
            self.canvas,
            text="Next",
            command=self.hide_next_button,
            bg=PRIMARY_COLOR,
            fg="white",
            font=(FONT_STYLE, 12, 'bold'),
            relief="raised",
            borderwidth=3,
            padx=20,
            pady=8
        )
        next_button.pack(pady=20)

    def hide_next_button(self):
        # Remove the "Next" button after it is clicked
        next_button = self.canvas.winfo_children()[-1]
        next_button.pack_forget()
        self.show_final_message()

    def show_final_message(self):
        self.canvas.config(height=250)
        self.message_label.config(
            text=f"{YOUR_NAME}'s love for you, {PARTNER_NAME}:\n\n"
                 "Like stars in the night sky,\n"
                 "My love for you will never fade ✨\n"
                 "you the love of my life kushu,you deserve all the happiness the world has to offer\n"
                 "I LOVE YOU MY DEAR!",
            font=(FONT_STYLE, 16, 'bold')
        )

    def create_replay_button(self):
        """Create and return a replay button."""
        return tk.Button(
            self.root,
            text="Replay",
            command=self.replay,
            bg=PRIMARY_COLOR,
            fg="white",
            font=(FONT_STYLE, 12, 'bold'),
            relief="raised",
            borderwidth=3,
            padx=20,
            pady=8
        )

    def replay(self):
        # Reset the application to its initial state
        self.canvas.destroy()
        self.setup_content()
        self.heart_animator.clear_hearts()  # Clear all hearts before restarting animation
        self.heart_animator.stop_heart_creation()
        self.root.after(1000, self.heart_animator.start)


if __name__ == "__main__":
    app = LoveApp()
    app.root.mainloop()
