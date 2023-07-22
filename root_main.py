import tkinter as tk
from io import BytesIO

import customtkinter
import tkinter.messagebox

from tkinter import ttk

import requests

from guicomps import config, styles
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow

from utils import icon
from core import main

TITLE = 'YouTube Transcription'
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class CustomTkApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.geometry('800x600')
        self.set_title('YouTube Transcription')
        self.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
        self.update_icon()

        self.label = customtkinter.CTkLabel(self, text="YouTube Video URL")
        self.label.grid(row=0, column=1, padx=20, pady=(20, 5))

        self.url_entry = customtkinter.CTkEntry(self, placeholder_text="Enter YouTube Video URL")
        self.url_entry.grid(row=1, column=1, padx=20, pady=(5, 5), sticky="ew")

        # create and pos button
        button = customtkinter.CTkButton(self, text="Submit", command=self.button_click)
        button.grid(row=2, column=1, padx=20, pady=(5, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=0, columnspan=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Bind Ctrl+F to the find_text method
        self.textbox.bind("<Control-f>", self.find_text)

        # Create a text tag named "highlight" for highlighting the found text
        self.textbox.tag_config("highlight", background="#FFFF00", selectbackground="#FFFF00", selectforeground="black")

        # option menu
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Set row and column weights to make the textbox and submit button expand with window resize
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # add methods to app

    def button_click(self):
        url = self.url_entry.get()
        try:
            x = main.video_id(url)
            v = f"https://img.youtube.com/vi/{x}/hqdefault.jpg"
            self.textbox.delete(1.0, tk.END)
            self.display_jpg(v)
            y = main.get_transcript(x)
            self.display_transcript(y)
        except Exception as e:
            self.textbox.delete(1.0, tk.END)
            tkinter.messagebox.showerror("Error", "Transcript not available for the provided video.")

    def set_title(self, title):
        self.wm_title(title)

    def display_jpg(self, url):
        response = requests.get(url)
        image_file = BytesIO(response.content)
        my_image = customtkinter.CTkImage(light_image=Image.open(image_file), size=(260, 260))
        image_label = customtkinter.CTkLabel(self, image=my_image, text="")  # display image with a CTkLabel
        image_label.grid(row=0, column=1)

    def display_transcript(self, y):
        for entry in y:
            text = entry['text']
            self.textbox.insert(tk.END, text + '\n')

    def find_text(self, event):
        # Display a search dialog to enter keywords
        self.dialog = customtkinter.CTkInputDialog(text="Enter text to find:", title="Find")
        self.dialog.bind("<Key>", self.update_highlight)

    def update_highlight(self, event):
        # Get the current search string from the search entry
        self.clear_highlight()
        search_string = self.dialog.get_input()
        if search_string:
            self.search_text(search_string)

    def search_text(self, target):
        start_pos = "1.0"
        while True:
            start_pos = self.textbox.search(target, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(target)}c"
            self.textbox.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos

    def clear_highlight(self):
        # Remove previous highlighting
        self.textbox.tag_remove("highlight", "1.0", tk.END)

    def update_icon(self):
        # Set the application icon periodically
        self.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
        # Schedule the next icon update after 500 milliseconds (adjust as needed)
        self.after(1, self.update_icon)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


app = CustomTkApp()
app.mainloop()
