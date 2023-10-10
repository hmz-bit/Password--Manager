from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    pw_entry.delete(0, END)
    pw_entry.insert(END, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip().title()
    email = info_entry.get().strip()
    pw = pw_entry.get().strip()
    new_data = {website: {
        "email": email,
        "password": pw
    }
    }

    if len(website) == 0 or len(email) == 0 or len(pw) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if website in data:
                is_sure = messagebox.askyesno(title=website, message="Are you sure to change the password?")
                if is_sure:
                    data[website]["password"] = pw
                    with open("data.json", mode="w") as data_file:
                        json.dump(data, data_file, indent=4)
            else:
                is_ok = messagebox.askokcancel(title=website,
                                               message=f"These are the details entered: \nEmail: {email}"
                                                       f"\nPassword: {pw} \nIs it ok to save?")
                if is_ok:
                    data.update(new_data)
                    with open("data.json", mode="w") as data_file:
                        json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pw_entry.delete(0, END)


# ---------------------------- SEARCH DATA ------------------------------- #
def search():
    website = website_entry.get().strip().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "no data file found.".title())
    else:
        if website == "":
            messagebox.showinfo(title="Oops", message="Please don't leave the website field empty!")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(website, f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo("Error", "No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

img = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

info_label = Label(text="Email/Username:")
info_label.grid(column=0, row=2)

pw_label = Label(text="Password:")
pw_label.grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky=EW)
website_entry.focus()

info_entry = Entry(width=35)
info_entry.grid(column=1, row=2, columnspan=2, sticky=EW)
info_entry.insert(END, "xxx123@gmail.com")

pw_entry = Entry(width=21)
pw_entry.grid(column=1, row=3, sticky=EW)

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky=EW)

pw_generator_button = Button(text="Generate Password", command=generate_password)
pw_generator_button.grid(column=2, row=3, sticky=EW)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW)

window.mainloop()
