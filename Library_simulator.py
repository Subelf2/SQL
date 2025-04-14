import tkinter as tk
import mysql.connector
import random
from db_credentials import db

books = []

# database connection
mydb = mysql.connector.connect(
    host=db['host'],
    user=db['user'],
    password=db['password'],
    database='Library_simulator'
)

mycursor = mydb.cursor()
sql = "SELECT * FROM Books"

params = []

mycursor.execute(sql)
res = mycursor.fetchall()

for x in res:
    books.append(x)

# GUI creation

# Window creation
window = tk.Tk()
window.title("Dark Brown Rectangle")

# Set the window size to match the rectangle dimensions (doubled)
window.geometry("1240x540")  # Width: 1200 + 40 padding, Height: 500 + 40 padding

# Canvas creation (doubled dimensions)
canvas = tk.Canvas(window, width=1240, height=540, bg="light gray")
canvas.pack()

# Drawing a rectangle with a darker outline (doubled dimensions)
canvas.create_rectangle(40, 40, 1200, 500, outline="#7B3F00", width=40)

# Drawing small rectangles for each book inside the main rectangle (doubled dimensions)
num_books = len(books)
if num_books > 0:

    # Updated colors for the small rectangles using HEX codes
    colors = ["#008000", "#4682B4", "#600000", "#000070", "#003300", "#40E0D0"]  # Green, Steel Blue, Dark Red, Dark Blue, Dark Green, Turquoise
    
    for i in range(num_books):
        color = colors[i % len(colors)]  # Cycle through colors
        x1 = 60 + (i * 100) + (i * 2)  # Adjust x-coordinate for padding (doubled)
        y1 = 60
        x2 = x1 + 100  # Doubled width
        y2 = y1 + 420  # Doubled height

        # Ensure the rectangles fit within the main rectangle
        if x2 <= 1200 and y2 <= 500:
            canvas.create_rectangle(
                x1,  # Generate a floating-point number
                y1 * (random.randint(100, 135) / 100),  # Generate a floating-point number
                x2,
                y2,
                outline="black",
                fill=color
            )
            # Add book title as text inside the rectangle (vertically)
            book_title = books[i][1]  # Assuming the title is in the second column of the database

            # If the title is longer than 30 characters, insert a newline around the middle
            if len(book_title) > 30:
                mid_index = len(book_title) // 2
                # Find a space near the middle to split the string cleanly
                if " " in book_title[mid_index - 10:mid_index + 10]:
                    split_index = book_title.rfind(" ", 0, mid_index + 10)
                    book_title = book_title[:split_index] + "\n" + book_title[split_index + 1:]
                else:
                    book_title = book_title[:mid_index] + "\n" + book_title[mid_index:]

            # Determine text color based on rectangle color brightness
            dark_colors = ["#600000", "#000070", "#003300"]  # Darker colors
            text_color = "white" if color in dark_colors else "black"

            canvas.create_text(
                (x1 + x2) / 2,  # Center horizontally
                (y1 + y2) / 2,  # Center vertically
                text=book_title,
                fill=text_color,  # Use white for dark rectangles, black otherwise
                angle=90,  # Rotate text vertically
                font=("Arial", 20)  # Doubled font size
            )

# Main function, so the UI starts and interacts with the user.
window.mainloop()