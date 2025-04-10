import tkinter as tk
from PIL import Image, ImageTk

# Function to load the background image without blur
def load_background_image(image_path):
    try:
        original_image = Image.open(image_path)
        return ImageTk.PhotoImage(original_image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Function to handle button clicks
def on_button_click(option):
    print(f"You selected: {option}")
    animate_box()

# Function to animate the box moving upward
def animate_box():
    # Hide the current text and buttons
    message_label.place_forget()
    yes_button.place_forget()
    definitely_yes_button.place_forget()

    # Move the entire canvas upward
    for i in range(150):  # Adjust the range for speed
        canvas.move(box, 0, -1)  # Move the box upward
        root.update()  # Update the canvas
        root.after(10)  # Delay for animation effect

    # Clear the canvas and display new text and image after the box has moved
    display_love_message()

# Function to display the love message and image
def display_love_message():
    # Clear the canvas
    canvas.delete("all")

    # Display the background color where the box was
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill='white', outline='')

    love_message = tk.Label(root, text="There is my love for you", bg='white', fg='black', font=('Arial Rounded MT Bold', 20))
    love_message.place(relx=0.5, rely=0.5, anchor='center')

    # Load and display the love image
    love_image = load_background_image("love_image.jpg")  # Replace with your image path
    if love_image:
        love_image_label = tk.Label(root, image=love_image)
        love_image_label.image = love_image  # Keep a reference to avoid garbage collection
        love_image_label.place(relx=0.5, rely=0.7, anchor='center')

# Function to create a rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, fill, outline, width):
    points = [
        x1 + radius, y1,  # Top side
        x2 - radius, y1,  # Top side
        x2, y1 + radius,  # Top right corner
        x2, y2 - radius,  # Bottom right corner
        x2 - radius, y2,  # Bottom side
        x1 + radius, y2,  # Bottom left corner
        x1, y2 - radius,  # Bottom left corner
        x1, y1 + radius,  # Top left corner
    ]
    return canvas.create_polygon(points, fill=fill, outline=outline, width=width)

# Create the main window
root = tk.Tk()
root.title("Explore Beyond")
root.geometry("800x600")

# Load and set the background image
background_image = load_background_image("romantic_background.jpg")  # Replace with your image path

if background_image is None:
    print("Background image could not be loaded.")
else:
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Create a canvas for the rounded box
    canvas_width = 300
    canvas_height = 150
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white', highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor='center')

    # Create a filled rounded rectangle
    box = create_rounded_rectangle(canvas, 0, 0, canvas_width, canvas_height, radius=20, fill='#FFC1CC', outline='', width=0)

    # Create a smooth outline by drawing a slightly larger rounded rectangle
    create_rounded_rectangle(canvas, -2, -2, canvas_width + 2, canvas_height + 2, radius=20, fill='', outline='#FFC1CC', width=2)

    # Add the message with a smaller font size
    message_label = tk.Label(canvas, text="Do you wanna explore what's beyond this world?", 
                              bg='#FFC1CC', fg='black', font=('Arial Rounded MT Bold', 12), wraplength=280)
    message_label.place(relx=0.5, rely=0.4, anchor='center')

    # Add buttons with bright pink background and flat appearance
    bright_pink = '#FF69B4'  # Bright pink color
    yes_button = tk.Button(canvas, text="Yes", command=lambda: on_button_click("Yes"), 
                           bg=bright_pink, fg='white', font=('Helvetica', 10), relief='flat')  # Flat appearance
    yes_button.place(relx=0.3, rely=0.7, anchor='center')

    definitely_yes_button = tk.Button(canvas, text="Definitely Yes", command=lambda: on_button_click("Definitely Yes"), 
                                       bg=bright_pink, fg='white', font=('Helvetica', 10), relief='flat')  # Flat appearance
    definitely_yes_button.place(relx=0.7, rely=0.7, anchor='center')

# Start the main loop
root.mainloop()