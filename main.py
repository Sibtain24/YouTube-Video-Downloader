import tkinter as tk
import customtkinter as ct
from pytubefix import YouTube
import os
import threading

# Progress Bar Calculation

def on_progress(stream, chunk, bytes_remanining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remanining
    size_mb = total_size / 1048576
    downloaded_mb  = bytes_downloaded / 1048576
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=f"{per}% ({round(downloaded_mb, 2)} MB of {round(size_mb, 2)} MB)")
    pPercentage.update()
    progressBar.set(float(percentage_of_completion / 100))

# Download Functions

def startDownload():
    try:
        ytLink = url_var.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        yt_title.configure(text=f"Downloading: {ytObject.title}")
        video = ytObject.streams.get_highest_resolution()
        folder_path = r"C:\YouTube Video Downloader\Downloads"
        video.download(output_path=folder_path)
        status_label.configure(text="Video Downloaded in 'C:\\YouTube Video Downloader\\Downloads'")
    except:
        status_label.configure(text="ERROR: Try again!", text_color="red")

# Create a new thread to run the startDownload function

def threadedDownload():
    download_thread = threading.Thread(target=startDownload)
    download_thread.start()

# Open output folder

def open_output():
    folder_path = r"C:\YouTube Video Downloader\Downloads"
    os.startfile(folder_path)

# Open output folder

def reset():
    link_entry.configure(link_entry.delete(0, tk.END))
    status_label.configure(text="")
    pPercentage.configure(text="0% (0 MB of 0 MB)")
    progressBar.set(0)
    yt_title.configure(text="")

# System and UI Settings

ct.set_appearance_mode("system")
ct.set_default_color_theme("green")

def change_theme(choice):
    ct.set_appearance_mode(choice)

# Our app frame

app = ct.CTk()
app.geometry("700x500")
app.resizable("False", "False")
app.title("Free YouTube Video Downloader")
app.iconbitmap("icon.ico")

# Adding UI Elements

title = ct.CTkLabel(app, text="YouTube Video Downloader", font=("Comicsans", 40, "bold"), text_color="#ffbb03")
title.pack(padx=10, pady=20)

sub_title = ct.CTkLabel(app, text="Enter a YouTube Video Link", font=("Comicsans", 20, "bold"))
sub_title.pack(padx=10)

# Link Entry Widget

url_var = tk.StringVar()
link_entry = ct.CTkEntry(app, width=400, height=40, textvariable=url_var)
link_entry.pack(pady=10)

# Video Title

yt_title = ct.CTkLabel(app, text="")
yt_title.pack(pady=5)

# Finished Downloading

status_label = ct.CTkLabel(app, text="")
status_label.pack()

# Progress Bar

pPercentage = ct.CTkLabel(app, text="0% (0 MB of 0 MB)")
pPercentage.pack()

progressBar = ct.CTkProgressBar(app, width=400, height=11)
progressBar.set(0)
progressBar.pack(pady=10)

# Download Button

download_btn= ct.CTkButton(app, text="Download", command=threadedDownload)
download_btn.pack(pady=5)

# Open Output Folder

output_btn = ct.CTkButton(app, text="Show in Folder", command=open_output)
output_btn.pack(pady=5)

# Reset Button

reset_btn = ct.CTkButton(app, text="Reset", command=reset)
reset_btn.pack(pady=5)

# App Theme

theme_var = tk.StringVar(value="System")
theme_combo = ct.CTkComboBox(app, values=["System", "Light", "Dark"], command=change_theme, variable=theme_var)
theme_combo.pack(anchor="se", padx=5, pady=5, side="bottom")


app.mainloop()