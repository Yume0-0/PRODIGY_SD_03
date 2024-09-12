import customtkinter as ctk
import re

app = ctk.CTk()
app.geometry('550x500')
app.title('Simple Contact Management System')
ctk.set_default_color_theme("dark-blue")

contacts = {}
phone_pattern = r"^\+?(\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
"""
Breakdown of the Regular Expression:

^:This symbol marks the start of the string. It ensures that the match begins at the beginning of the input.

\+?:\+ matches the plus sign (+) literally. ? means that the plus sign is optional. This allows the pattern to match numbers with or without a leading plus sign.

(\d{1,3})?:\d{1,3} matches 1 to 3 digits. This is typically used for the country code.
The parentheses () group these digits together.The ? after the group makes the entire group optional, allowing the phone number to have a country code or not.

[-.\s]?:[-.\s] matches a hyphen (-), period (.), or whitespace (\s).
The ? makes this character optional, allowing for various formats of separation between number sections.

\(?\d{3}\)?: \( matches an opening parenthesis (() literally, but it is made optional with ?.
\d{3} matches exactly 3 digits, typically the area code.\)? matches a closing parenthesis ()) literally and is also optional.
This pattern allows for area codes to be enclosed in parentheses or not.

[-.\s]?: Again matches an optional separator (-, ., or whitespace) between number groups.

\d{3}:Matches exactly 3 digits, usually the first part of the local number.

[-.\s]?: Matches an optional separator between number groups.

\d{4}: Matches exactly 4 digits, typically the last part of the phone number.
$:

Marks the end of the string, ensuring the entire input matches the pattern completely.
"""

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def update_contact_list():
    contact_list = "\n".join([f"{name} - phone : {info['phone']} - email : {info['email']}" for name, info in contacts.items()])
    view_contacts.configure(text=contact_list if contact_list else "No contacts available.")

def clear_entries():
    name.set('')
    phone.set('')
    email.set('')


def add_contact():
    name_to_add = name.get()
    phone_to_add = phone.get()
    email_to_add = email.get()
    if name_to_add and re.match(phone_pattern, phone_to_add) and re.match(email_pattern, email_to_add):
        contacts[name_to_add] = {"phone": phone_to_add, "email": email_to_add}
        result_var.set("Contact added successfully.")
        update_contact_list()
    else:
        result_var.set("Invalid format. Please enter valid details.")
    clear_entries()

def edit_contact():
    name_to_edit = edit_name.get()
    name_change = new_name.get()
    phone_change = edit_phone.get()
    email_change = edit_email.get()

    if name_to_edit in contacts:
        if name_change:
            contacts[name_change] = contacts.pop(name_to_edit)
            if phone_change:
                contacts[name_change]["phone"] = phone_change
            if email_change:
                contacts[name_change]["email"] = email_change

            edit_result_var.set("Contact updated successfully.")
        else:
            if phone_change:
                contacts[name_to_edit]["phone"] = phone_change
            if email_change:
                contacts[name_to_edit]["email"] = email_change

            if not phone_change and not email_change:
                edit_result_var.set("No changes made.")
            else:
                edit_result_var.set("Contact updated successfully.")

        #make the contacts appear in the view Tab
        update_contact_list()
    else:
        # Contact not found in the contacts dictionary
        edit_result_var.set("Contact not found.")

def delete_contact():
    name_to_delete = edit_name.get()
    if name_to_delete in contacts:
        del contacts[name_to_delete]
        edit_result_var.set("Contact deleted successfully.")
        update_contact_list()
    else:
        edit_result_var.set("Contact not found.")

tabs = ctk.CTkTabview(app)
tabs.pack(expand=True, fill='both')

add_tab = tabs.add("Add Contact")
name = ctk.StringVar()
phone = ctk.StringVar()
email = ctk.StringVar()
result_var = ctk.StringVar()

ctk.CTkLabel(add_tab, text="Name").pack(pady=5)
ctk.CTkEntry(add_tab, textvariable=name).pack(pady=5)
ctk.CTkLabel(add_tab, text="Phone").pack(pady=5)
ctk.CTkEntry(add_tab, textvariable=phone).pack(pady=5)
ctk.CTkLabel(add_tab, text="Email").pack(pady=5)
ctk.CTkEntry(add_tab, textvariable=email).pack(pady=5)
ctk.CTkButton(add_tab, text="Add Contact", command=add_contact).pack(pady=10)
ctk.CTkLabel(add_tab, textvariable=result_var).pack(pady=5)

view_tab = tabs.add("View Contacts")
view_contacts = ctk.CTkLabel(view_tab, text="No contacts available.")
view_contacts.pack(pady=20)


edit_tab = tabs.add("Edit/Delete Contact")
edit_name = ctk.StringVar()
new_name = ctk.StringVar()
edit_phone = ctk.StringVar()
edit_email = ctk.StringVar()
edit_result_var = ctk.StringVar()

ctk.CTkLabel(edit_tab, text="Name to Edit/Delete").pack(pady=5)
ctk.CTkEntry(edit_tab, textvariable=edit_name).pack(pady=5)
ctk.CTkLabel(edit_tab, text= "New name").pack(pady=5)
ctk.CTkEntry(edit_tab, textvariable= new_name).pack(pady=5)
ctk.CTkLabel(edit_tab, text="New Phone").pack(pady=5)
ctk.CTkEntry(edit_tab, textvariable=edit_phone).pack(pady=5)
ctk.CTkLabel(edit_tab, text="New Email").pack(pady=5)
ctk.CTkEntry(edit_tab, textvariable=edit_email).pack(pady=5)
ctk.CTkButton(edit_tab, text="Edit Contact", command=edit_contact).pack(pady=15 )
ctk.CTkButton(edit_tab, text="Delete Contact", command=delete_contact).pack(pady=5)
ctk.CTkLabel(edit_tab, textvariable=edit_result_var).pack(pady=5)

app.mainloop()
