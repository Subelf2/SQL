import tkinter as tk
import mysql.connector
import random
from db_credentials import db

books = []
genres = []

# database connection
mydb = mysql.connector.connect(
    host=db['host'],
    user=db['user'],
    password=db['password'],
    database='Library_simulator'
)

mycursor = mydb.cursor()

sql_genres = "SELECT * FROM genres"
mycursor.execute(sql_genres)
myresult = mycursor.fetchall()
for x in myresult:
    genres.append(x)

#function to add a book to the database
def add_book_to_db(title, author, genre, year):
    sql_get_genre_id = "SELECT style_id FROM genres WHERE name = %s"
    mycursor.execute(sql_get_genre_id, (genre,))
    genre_id = mycursor.fetchone()
    sql = "INSERT INTO Books (Title, Author, Style_id, year_of_publication) VALUES (%s, %s, %s, %s)"
    val = (title, author, genre_id[0], year)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


# GUI creation

# Window creation
window = tk.Tk()
window.title("Library Simulator")

# Adjust the window size
window.geometry("1400x700")

# Canvas creation
canvas = tk.Canvas(window, width=1400, height=700, bg="light gray")  # Match canvas size to window
canvas.pack()

# Drawing a rectangle with a darker outline (match the window size)
main_rectangle = canvas.create_rectangle(40, 40, 1360, 660, outline="#7B3F00", width=40)

# Drawing small rectangles for each book inside the main rectangle
num_books = len(books)
book_to_rectangle = {}  # Dictionary to map books to their rectangles
book_to_title = {}  # Dictionary to map books to their title text

colors = ["#008000", "#4682B4", "#600000", "#000070", "#003300", "#40E0D0"]  # Colors for rectangles
#shuffle the colors to randomize their order
random.shuffle(colors)

# Function to display the "Add Book" frame
def show_add_book_frame():
    # Hide the main canvas
    canvas.pack_forget()

    # Create a new frame for adding a book
    add_book_frame = tk.Frame(window, bg="light gray")
    add_book_frame.pack(fill="both", expand=True)

    # Fields for book details
    tk.Label(add_book_frame, text="Add a New Book", font=("Arial", 24, "bold"), bg="light gray").pack(pady=20)

    tk.Label(add_book_frame, text="Title:", font=("Arial", 14), bg="light gray").pack(pady=5)
    title_entry = tk.Entry(add_book_frame, font=("Arial", 14), width=30)
    title_entry.pack(pady=5)

    tk.Label(add_book_frame, text="Author:", font=("Arial", 14), bg="light gray").pack(pady=5)
    author_entry = tk.Entry(add_book_frame, font=("Arial", 14), width=30)
    author_entry.pack(pady=5)

    tk.Label(add_book_frame, text="Genre:", font=("Arial", 14), bg="light gray").pack(pady=5)
    genre_entry = tk.Entry(add_book_frame, font=("Arial", 14), width=30)
    genre_entry.pack(pady=5)

    tk.Label(add_book_frame, text="Year of Publication:", font=("Arial", 14), bg="light gray").pack(pady=5)
    year_entry = tk.Entry(add_book_frame, font=("Arial", 14), width=30)
    year_entry.pack(pady=5)

    # Add a "Confirm" button
    def confirm_add_book():
        # Get the values from the fields
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()

        # Clear any previous error message
        error_label.config(text="")

        # Validate the inputs
        if not title.strip():
            error_label.config(text="Error: Title cannot be empty.")
            return
        if not author.strip():
            error_label.config(text="Error: Author cannot be empty.")
            return
        if not genre.strip() in [genre[1] for genre in genres]:
            error_label.config(text="Error: Genre must be one of the predefined genres.")
            return
        if not year.isdigit():
            error_label.config(text="Error: Year of Publication must be a number.")
            return

        # Print the entered details (for now)
        add_book_to_db(title, author, genre, year)

        # Go back to the library
        add_book_frame.pack_forget()
        canvas.pack(fill="both", expand=True)
        redraw_books()  # Redraw the books to include the new one

    # Add an error label to display validation messages
    error_label = tk.Label(add_book_frame, text="", font=("Arial", 12), fg="red", bg="light gray")
    error_label.pack(pady=5)

    tk.Button(add_book_frame, text="Confirm", command=confirm_add_book, font=("Arial", 14), bg="green", fg="white").pack(pady=20)

    # Add a "Back" button to return to the library
    def go_back():
        add_book_frame.pack_forget()
        canvas.pack(fill="both", expand=True)

    tk.Button(add_book_frame, text="Back to Library", command=go_back, font=("Arial", 14), bg="#7B3F00", fg="white").pack(pady=10)

# Function to redraw all books on the canvas
def redraw_books():
    sql_books = "SELECT Book_id, Title, Author, G.name, year_of_publication FROM Books JOIN genres G ON books.Style_id = G.style_id"
    # Clear the previous books list
    books.clear()
    mycursor.execute(sql_books)

    res = mycursor.fetchall()
    for x in res:
        books.append(x)
    
    canvas.delete("all")  # Clear the canvas
    # Redraw the main rectangle
    canvas.create_rectangle(40, 40, 1360, 660, outline="#7B3F00", width=40)

    # Redraw all books
    book_to_rectangle.clear()
    book_to_title.clear()
    for i, book in enumerate(books):
        color = colors[i % len(colors)]  # Cycle through colors
        x1 = 60 + (i * 100) + (i * 2)  # Adjust x-coordinate for padding
        y1 = 60 
        x2 = x1 + 100
        y2 = 640 

        # Draw the rectangle
        rect = canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

        # Add book title as text inside the rectangle (vertically)
        book_title = book[1]
        if len(book_title) > 30:
            mid_index = len(book_title) // 2
            if " " in book_title[mid_index - 10:mid_index + 10]:
                split_index = book_title.rfind(" ", 0, mid_index + 10)
                book_title = book_title[:split_index] + "\n" + book_title[split_index + 1:]
            else:
                book_title = book_title[:mid_index] + "\n" + book_title[mid_index:]

        text_color = "white" if color in ["#600000", "#000070", "#003300"] else "black"
        text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=book_title, fill=text_color, angle=90, font=("Arial", 20))

        # Bind click events to the rectangle and text
        canvas.tag_bind(rect, "<Button-1>", lambda event, book=book: show_book_details(book))
        canvas.tag_bind(text, "<Button-1>", lambda event, book=book: show_book_details(book))

        # Map the book to its rectangle and title text
        book_to_rectangle[book] = rect
        book_to_title[book] = text

    # Add the "Add Book" button after the last book
    add_button_x1 = 60 + (len(books) * 100) + (len(books) * 2)
    add_button_x2 = add_button_x1 + 100
    add_button_y1 = 240
    add_button_y2 = 440

    add_button = canvas.create_rectangle(add_button_x1, add_button_y1, add_button_x2, add_button_y2, outline="light gray", fill="light gray")
    add_text = canvas.create_text((add_button_x1 + add_button_x2) / 2, (add_button_y1 + add_button_y2) / 2, text="Add\nBook", fill="black", angle=0, font=("Arial", 14))

    # Bind click event to the "Add Book" button
    canvas.tag_bind(add_button, "<Button-1>", lambda event: show_add_book_frame())
    canvas.tag_bind(add_text, "<Button-1>", lambda event: show_add_book_frame())

# Function to display book details in the same window
def show_book_details(book):
    # Hide the main canvas
    canvas.pack_forget()

    # Create a new frame for the book details
    details_frame = tk.Frame(window, bg="light gray")
    details_frame.pack(fill="both", expand=True)

    # Display book details
    tk.Label(details_frame, text=f"{book[1]}", font=("Arial", 34, "bold"), bg="light gray").pack(pady=60)
    tk.Label(details_frame, text=f"This book was written by {book[2]} \nand published in {book[4]}. It belongs to the genre {book[3]}.", font=("Arial", 24), bg="light gray").pack(pady=5)

    # Add a "Back" button to return to the main canvas
    def go_back():
        details_frame.pack_forget()  # Hide the details frame
        canvas.pack(fill="both", expand=True)  # Show the main canvas

    tk.Button(details_frame, text="Back To Library", command=go_back, font=("Arial", 20), bg="#7B3F00", fg="white").pack(pady=30)

    # Add a "Remove Book" button
    def remove_book():
        # Confirmation dialog
        confirmation_frame = tk.Frame(details_frame, bg="light gray")
        confirmation_frame.pack(pady=20)

        tk.Label(confirmation_frame, text="Are you sure you want to remove this book?", font=("Arial", 14), bg="light gray").pack(pady=10)

        def confirm_removal():
            # Remove the book from the list
            books.remove(book)
            # Redraw the canvas to shift books
            redraw_books()
            confirmation_frame.pack_forget()  # Hide the confirmation frame
            go_back()  # Return to the main canvas

        def cancel_removal():
            confirmation_frame.pack_forget()  # Hide the confirmation frame

        # Add "Yes" and "No" buttons with proper padding and alignment
        button_frame = tk.Frame(confirmation_frame, bg="light gray")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Yes", command=confirm_removal, font=("Arial", 12), bg="red", fg="white").pack(side="left", padx=20)
        tk.Button(button_frame, text="No", command=cancel_removal, font=("Arial", 12), bg="green", fg="white").pack(side="right", padx=20)

    tk.Button(details_frame, text="Remove Book", command=remove_book, font=("Arial", 20), bg="#600000", fg="white").pack(pady=10)

# Initial drawing of books
redraw_books()

# Main function to start the UI
window.mainloop()