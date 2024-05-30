import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from scapy.all import *
from langchain_community.llms import Ollama
import threading
import csv
import chardet

llm = Ollama(model="llama3")

def parse_pcap(input_file):
    try:
        if input_file.lower().endswith('.pcapng'):
            packets = rdpcapng(input_file)
        else:
            packets = rdpcap(input_file)
        pcap_contents = ""
        for packet in packets:
            pcap_contents += str(packet) + '\n'
        return pcap_contents
    except Exception as e:
        return f"Error parsing PCAP: {e}"

def parse_csv(input_file):
    try:
        # Detect the file's encoding
        with open(input_file, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        
        csv_contents = ""
        with open(input_file, 'r', encoding=encoding) as file:
            reader = csv.reader(file)
            for row in reader:
                csv_contents += ','.join(row) + '\n'
        return csv_contents
    except Exception as e:
        return f"Error parsing CSV: {e}"


def open_file_dialog(file_type):
    if file_type == "pcap":
        input_file = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap *.pcapng")])
        if input_file:
            file_label.config(text=f"Selected file: {os.path.basename(input_file)}")
            threading.Thread(target=load_file_content, args=(input_file, parse_pcap)).start()
    elif file_type == "csv":
        input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if input_file:
            file_label.config(text=f"Selected file: {os.path.basename(input_file)}")
            threading.Thread(target=load_file_content, args=(input_file, parse_csv)).start()

def load_file_content(input_file, parser_func):
    try:
        contents = parser_func(input_file)
        file_contents_text.configure(state='normal')
        file_contents_text.delete(1.0, tk.END)
        file_contents_text.insert(tk.END, contents)
        file_contents_text.configure(state='disabled')
    except Exception as e:
        update_response(f"Error: {e}")

def process_file():
    try:
        user_question = question_entry.get()
        if not user_question:
            update_response("Please enter a question.")
            return

        file_contents = file_contents_text.get("1.0", tk.END)
        if file_contents:
            input_text = user_question + "\n" + file_contents

            # Start the progress bar
            response_label.config(text="Processing...")
            progress_bar.pack(pady=5, fill='x')  # Show the progress bar
            progress_bar.start()
            threading.Thread(target=invoke_llm, args=(input_text,)).start()
    except Exception as e:
        update_response(f"Error: {e}")

def invoke_llm(input_text):
    try:
        response = llm.invoke(input_text)
        update_response(response)
    except Exception as e:
        update_response(f"Error: {e}")
    finally:
        progress_bar.stop()
        progress_bar.pack_forget()  # Hide the progress bar after processing is complete

def update_response(response):
    response_text.configure(state='normal')
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, response)
    response_text.configure(state='disabled')
    response_label.config(text="")

# Create the main application window
root = tk.Tk()
root.title("NetLingo")

# Configure the dark mode theme
bg_color = "#1e1e1e"  # Dark background color
text_color = "#00ff00"  # Green text color
root.configure(bg=bg_color)
root.geometry("800x600")  # Set the window size

# Create a frame for content
frame = tk.Frame(root, bg=bg_color)
frame.pack(fill='both', expand=True, padx=10, pady=10)

# Create buttons to open the file dialog for PCAP and CSV files
open_pcap_button = tk.Button(frame, text="Open PCAP File", command=lambda: open_file_dialog("pcap"), bg=bg_color, fg=text_color)
open_pcap_button.pack(pady=5)

open_csv_button = tk.Button(frame, text="Open CSV File", command=lambda: open_file_dialog("csv"), bg=bg_color, fg=text_color)
open_csv_button.pack(pady=5)

# Create a label to display the selected file name
file_label = tk.Label(frame, text="", bg=bg_color, fg=text_color)
file_label.pack(pady=5)

# Create a text box for the user to enter their question
question_label = tk.Label(frame, text="Enter your question:", bg=bg_color, fg=text_color)
question_label.pack(pady=5)
question_entry = tk.Entry(frame, width=80, bg=bg_color, fg=text_color, insertbackground=text_color)
question_entry.pack(pady=5)

# Create a label to display the response from the language model
response_label = tk.Label(frame, text="", bg=bg_color, fg=text_color)
response_label.pack(pady=5)

# Create a progress bar
progress_bar = ttk.Progressbar(frame, mode='indeterminate')

# Create a scrollable text widget to display the file contents
file_contents_text = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    bg=bg_color,
    fg=text_color,
    insertbackground=text_color,  # Cursor color
    font=("Consolas", 10),
    padx=5,
    pady=5,
    height=10
)
file_contents_text.pack(fill='both', expand=True, pady=5)
file_contents_text.configure(state='disabled')

# Create a button to process the file with the user's question
submit_button = tk.Button(frame, text="Submit", command=process_file, bg=bg_color, fg=text_color)
submit_button.pack(pady=5)

# Pack the progress bar under the response label but keep it hidden initially
progress_bar.pack(pady=5, fill='x')
progress_bar.pack_forget()

# Create a scrollable text widget to display the response from the language model
response_text = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    bg=bg_color,
    fg=text_color,
    insertbackground=text_color,  # Cursor color
    font=("Consolas", 10),
    padx=5,
    pady=5,
    height=10
)
response_text.pack(fill='both', expand=True, pady=5)
response_text.configure(state='disabled')

# Start the Tkinter event loop
root.mainloop()
