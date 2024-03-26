from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_json(data):
    with open("data.json", 'w') as file:
        json.dump(data, file, indent=4)  # Saving updated data


def save():
    site = site_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    new_data = {
        site: {
            "user": user,
            "password": password,
        }
    }

    if len(site) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", 'r') as file:
                data = json.load(file)  # Reading old data
        except FileNotFoundError:
            save_json(new_data)
        else:
            data.update(new_data)  # Updating old data with new data
            save_json(data)
        finally:
            site_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        site = site_entry.get()
        if site in data:
            user = data[site]["user"]
            password = data[site]["password"]
            messagebox.showinfo(title=site, message=f"User: {user} \nPassword: {password}")
        else:
            messagebox.showwarning(title="Warning", message=f"No details for the website '{site}' exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
site_label = Label(text="Website:")
site_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
site_entry = Entry(width=33)
site_entry.grid(column=1, row=1)
site_entry.focus()
user_entry = Entry(width=53)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "ionme")
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Buttons
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()
