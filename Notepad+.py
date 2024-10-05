import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkFont

# Create the main application window
root = tk.Tk()
root.title("Simple Notepad")
root.geometry("600x400")

# Create a Text widget for the main text area
text_area = tk.Text(root, undo=True, wrap="word")
text_area.pack(expand=1, fill='both')

# Function to create a new file
def new_file():
    root.title("Untitled - Simple Notepad")
    text_area.delete(1.0, tk.END)

# Function to open an existing file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
            root.title(f"{file_path} - Simple Notepad")

# Function to save the current file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
            root.title(f"{file_path} - Simple Notepad")

# Function to exit the application
def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.quit()

# Search and Replace function
def search_text():
    search_window = tk.Toplevel(root)
    search_window.title("Search & Replace")
    search_window.geometry("350x150")

    tk.Label(search_window, text="Find:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(search_window, text="Replace:").grid(row=1, column=0, padx=10, pady=5)

    find_entry = tk.Entry(search_window, width=30)
    find_entry.grid(row=0, column=1, padx=10, pady=5)
    replace_entry = tk.Entry(search_window, width=30)
    replace_entry.grid(row=1, column=1, padx=10, pady=5)

    def find():
        text_area.tag_remove('found', '1.0', tk.END)
        find_text = find_entry.get()
        if find_text:
            idx = '1.0'
            while True:
                idx = text_area.search(find_text, idx, nocase=1, stopindex=tk.END)
                if not idx: break
                lastidx = f"{idx}+{len(find_text)}c"
                text_area.tag_add('found', idx, lastidx)
                idx = lastidx
            text_area.tag_config('found', foreground='white', background='blue')

    def replace():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        content = text_area.get(1.0, tk.END)
        new_content = content.replace(find_text, replace_text)
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, new_content)

    tk.Button(search_window, text="Find", command=find).grid(row=2, column=0, padx=10, pady=5)
    tk.Button(search_window, text="Replace", command=replace).grid(row=2, column=1, padx=10, pady=5)

# Font customization window
def change_font():
    font_window = tk.Toplevel(root)
    font_window.title("Font Customization")
    font_window.geometry("300x200")

    tk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=5)

    font_family = tk.StringVar(value="Arial")
    font_family_entry = tk.Entry(font_window, textvariable=font_family, width=20)
    font_family_entry.grid(row=0, column=1, padx=10, pady=5)

    font_size = tk.IntVar(value=12)
    font_size_entry = tk.Entry(font_window, textvariable=font_size, width=20)
    font_size_entry.grid(row=1, column=1, padx=10, pady=5)

    def apply_font():
        selected_font = tkFont.Font(family=font_family.get(), size=font_size.get())
        text_area.configure(font=selected_font)

    tk.Button(font_window, text="Apply", command=apply_font).grid(row=2, column=1, padx=10, pady=5)

# Rich text formatting functions
def make_bold():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
        text_area.tag_config("bold", font=tkFont.Font(weight="bold"))

def make_italic():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
        text_area.tag_config("italic", font=tkFont.Font(slant="italic"))

def make_underline():
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
        text_area.tag_config("underline", font=tkFont.Font(underline=True))

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=text_area.edit_undo)
edit_menu.add_command(label="Redo", command=text_area.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda: text_area.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: text_area.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: text_area.event_generate("<<Paste>>"))
edit_menu.add_command(label="Select All", command=lambda: text_area.event_generate("<<SelectAll>>"))
edit_menu.add_command(label="Search/Replace", command=search_text)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Bold", command=make_bold)
format_menu.add_command(label="Italic", command=make_italic)
format_menu.add_command(label="Underline", command=make_underline)
menu_bar.add_cascade(label="Format", menu=format_menu)

# Add Font option in the menu
menu_bar.add_command(label="Change Font", command=change_font)

# Help menu
def about_notepad():
    messagebox.showinfo("About", "Simple Notepad app using Python and Tkinter")

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About Notepad", command=about_notepad)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Run the main event loop
root.mainloop()
