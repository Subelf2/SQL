import tkinter as tk

# Window creation
window = tk.Tk()
# window.geometry("350x200")
window.title("first GUI")

# frame init
frm = tk.Frame(window, background="light blue", padx=5, pady=5)
frm.pack()

password_val = tk.StringVar()
user_val = tk.StringVar()
text_button_1 = tk.StringVar(value="User")

# labels init
user_lbl = tk.Label(frm, textvariable = text_button_1, background = 'light blue', font=("Arial", 24))
user_lbl.grid(column=1, row=1)
lbl2 = tk.Label(frm, text="Label 2", background = 'light blue', font=("Arial", 24)) 
lbl2.grid(column=1, row=2)

# entries init
user_entry = tk.Entry(frm, textvariable = user_val, font=("arial", 24))
ent2 = tk.Entry(frm, textvariable = password_val, font=("arial", 24))
user_entry.grid(column=2, row=1)
ent2.grid(column=2, row=2)

# function for button
def log_in():
    if (user_val.get() == "" or password_val.get() == ""):
        print("Enter your username and password.")
    else:
        print(user_val.get())
        print(password_val.get())

# button init
btn = tk.Button(window, text="log in", command = log_in)
btn.pack()

window.bind('<Return>', log_in)

# Main function, so the UI starts and interacts with the user.
window.mainloop()