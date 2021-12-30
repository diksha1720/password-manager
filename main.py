import string
from tkinter import *
from random import choice
from datetime import datetime
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_password():
    password_len = 10
    low_list = list(string.ascii_lowercase)
    up_list = list(string.ascii_uppercase)
    numbers = [str(i) for i in range(10)]
    special_char = ['!', '@', '$', '#', '%', '&', '*', '?', '/']

    password = ""
    for _ in range(password_len):
        password += choice(choice([low_list, up_list, special_char, numbers]))
    t_password.delete(0, END)
    t_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def search_data():
    user_website = t_website.get().title()

    try:
        with open("saved_info.json") as file:
            data = json.load(file)
        messagebox.showinfo(title=user_website, message=f"Email: {data[user_website]['email']}\n\nPassword: {data[user_website]['password']}")
        pyperclip.copy(data[user_website]["password"])
    except ValueError:
        messagebox.showinfo(title="Error", message="No saved passwords")
    except KeyError:
        messagebox.showinfo(title="Error", message=f"No saved passwords with {user_website}")


def save_details():
    user_website = t_website.get().title()
    user_email = t_email.get()
    user_pass = t_password.get()

    if len(user_website) == 0 or len(user_pass) == 0:
        messagebox.showinfo(title="Oops!!", message="Please fill out all the fields to proceed")
    else:
        is_ok = messagebox.askokcancel(title=user_website, message=f"These are the details you entered\n\nEmail : {user_email}\nPassword : {user_pass}\n\nDo you want to proceed?")
        if is_ok:
            c_date = datetime.today().strftime('%B %d, %Y')
            new_dict = {user_website:
            {
                "date": c_date,
                "email": user_email,
                "password": user_pass
            }}

            try:
                with open("saved_info.json", "r") as file:
                    data = json.load(file)
                    data.update(new_dict)
                with open("saved_info.json", "w") as file:
                    json.dump(data, file, indent=4)
            except FileNotFoundError:
                with open("saved_info.json", "w") as file:
                    json.dump(new_dict, file, indent=4)
            finally:
                refresh()


def refresh():
    t_website.delete(0, END)
    t_password.delete(0, END)
    t_website.focus()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)

p_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200,  highlightthickness=0)
canvas.create_image(100, 100, image=p_image)
canvas.grid(column=1, row=0)

l_website = Label(text="Website:")
l_website.grid(column=0, row=1)

l_email = Label(text="Email/Username:")
l_email.grid(column=0, row=2)

l_password = Label(text="Password:")
l_password.grid(column=0, row=3)

t_website = Entry(width=22)
t_website.grid(column=1, row=1)
t_website.focus()

t_email = Entry(width=40)
t_email.grid(column=1, row=2, columnspan=2)
t_email.insert(0, "diksha@test.com")

t_password = Entry(width=22)
t_password.grid(column=1, row=3)

b_search = Button(text="Search", width=14, command=search_data)
b_search.grid(column=2, row=1)

b_password = Button(text="Generate Password", width=14, command=gen_password)
b_password.grid(column=2, row=3)

b_add = Button(text="Add", width=35, command=save_details)
b_add.grid(column=1, row=4, columnspan=2)


window.mainloop()
