import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from scapy.all import *
from langchain_community.llms import Ollama
import threading

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

def open_file_dialog():
    input_file = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap *.pcapng")])
    if input_file:
        process_pcap_file(input_file)

def process_pcap_file(input_file):
    try:
        pcap_contents = parse_pcap(input_file)
        if pcap_contents:
            question = "Does this look malicious?\n"
            input_text = question + pcap_contents

            # Start the progress bar
            progress_bar.pack(pady=10, fill='x')
            progress_bar.start()
            response_label.config(text="Processing...")
            threading.Thread(target=invoke_llm, args=(input_text,)).start()
    except Exception as e:
        response_text.configure(state='normal')
        response_text.delete(1.0, tk.END)
        response_text.insert(tk.END, f"Error: {e}")
        response_text.configure(state='disabled')

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

# Create a frame for content
frame = tk.Frame(root, bg=bg_color)
frame.pack(fill='both', expand=True, padx=10, pady=10)

# Create a button to open the file dialog
open_file_button = tk.Button(frame, text="Open PCAP File", command=open_file_dialog, bg=bg_color, fg=text_color)
open_file_button.pack(pady=20)

# Create a progress bar
progress_bar = ttk.Progressbar(frame, mode='indeterminate')

# Create a label to display the response from the language model
response_label = tk.Label(frame, text="", bg=bg_color, fg=text_color)
response_label.pack(pady=10)

# Create a scrollable text widget to display the response from the language model
response_text = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    bg=bg_color,
    fg=text_color,
    insertbackground=text_color,  # Cursor color
    font=("Consolas", 12),
    padx=10,
    pady=10
)
response_text.pack(fill='both', expand=True)

# Make the text widget read-only
response_text.configure(state='disabled')

# Start the Tkinter event loop
root.mainloop()
