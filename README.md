# NetLingo
A small project that uses lang-chain, python, and ollama that takes a pcap or csv file, parses the pcap or csv, outputs to a readable format for the LLM to analyze. It's a work in progress.

You will need to install Ollama: https://github.com/ollama/ollama

and Wireshark: https://www.wireshark.org/

You will also need to install the requirements using the requirements.txt file and the NetLingoDepInstaller.bat script.

To run: py NetLingo.py

Extra:

Try using a different model from huggingface.co!

Download and test the model to ensure it is working with ollama:

Download the gguf from huggingface, create the Modelfile using echo. > Modelfile, then open with text editor and add: FROM C:\Users\username\Downloads\NameOfModel.gguf, then run the command: ollama create NameOfModel -f Modelfile, then to run: ollama run NameOfModel

Edit the code to use the new model instead of llama3, that should do it!


