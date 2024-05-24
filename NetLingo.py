import os
import tkinter as tk
from tkinter import filedialog
from scapy.all import *
from langchain_community.llms import Ollama

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
    try:
        input_file = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap *.pcapng")])
        if input_file:
            pcap_contents = parse_pcap(input_file)
            if pcap_contents:
                question = "Does this look malicious?\n"
                input_text = question + pcap_contents
                response = llm.invoke(input_text)
                response_label.config(text=response)
    except Exception as e:
        response_label.config(text=f"Error: {e}")

# Create the main application window
root = tk.Tk()
root.title("PCAP Parser")

# Create a button to open the file dialog
open_file_button = tk.Button(root, text="Open PCAP File", command=open_file_dialog)
open_file_button.pack(pady=20)

# Create a label to display the response from the language model
response_label = tk.Label(root, text="")
response_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
