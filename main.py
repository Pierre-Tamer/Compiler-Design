from tkinter import filedialog, END, messagebox
import os
from PIL import Image, ImageTk
import customtkinter as ctk
from Code.Scanner import Scanner
from Code.Parser import Parser
from Code import Util
from Code.lexical_analyzer import lexical_analysis, check_lexical_errors


graphviz_bin_path = os.path.abspath(os.path.join(os.getcwd(), 'Graphviz', 'bin'))
os.environ["PATH"] += os.pathsep + graphviz_bin_path

def open_file():
    global filepath, file_opened
    filepath = filedialog.askopenfilename(title="Select A Text File")
    if filepath:
        if not filepath.split('.')[1] == "txt":
            output_text.configure(state="normal")
            textbox.configure(state="normal")
            textbox.delete("1.0", END)
            output_text.delete("1.0", END)
            textbox.configure(state="disabled")
            output_text.configure(state="disabled")
            messagebox.showerror("File Type Error", "Please choose a Text file!!")
        else:
            file_opened = True
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
                textbox.configure(state="normal")
                textbox.delete("1.0", END)
                textbox.insert(END, file_content)
                textbox.configure(state="normal")  # Set state to normal to enable editing
    else:
        file_opened = False
        output_text.configure(state="normal")
        textbox.configure(state="normal")
        textbox.delete("1.0", END)
        output_text.delete("1.0", END)
        messagebox.showerror("File Error", "Pick a file!")
        textbox.configure(state="disabled")
        output_text.configure(state="disabled")

def check_syntax():
    global filepath
    if not file_opened:
        messagebox.showerror("File Error", "Please choose a file before doing any operation!!")
    else:
        obj = Scanner()
        tokens = obj.tokenize(filepath)
        pr_obj = Parser()
        pr_obj.tokens = tokens
        try:
            pr_obj.program()
            messagebox.showinfo("Syntax Check", "No syntax errors found!")
        except ValueError:
            messagebox.showerror("Syntax Error", "Syntax error detected. Please correct your code.")

def scan():
    global filepath
    if not file_opened:
        output_text.configure(state="normal")
        lexeme_Def.configure(state="normal")
        lexeme_Def.delete("1.0", END)
        output_text.delete("1.0", END)
        messagebox.showerror("File Error", "Pick a file 👍")
        lexeme_Def.configure(state="disabled")
        output_text.configure(state="disabled")
    else:
        # Read content from the textbox instead of filepath
        file_content = textbox.get("1.0", END)
        # Temporarily write content to a temporary file
        temp_file_path = os.path.join(os.path.expanduser('~'), 'temp_file.txt')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(file_content)
        
        obj = Scanner()
        obj.tokenize(temp_file_path)
        obj.export()

        # Read the tokens and lexemes from the file
        with open(os.path.join(os.path.expanduser('~'), 'Tokens.txt'), "r", encoding='utf-8') as file:
            lines = file.readlines()
            tokens = [line.split(',')[0].strip() for line in lines]
            lexemes = [line.split(',')[1].strip() for line in lines]

        # Join tokens and lexemes for display
        tokens_text = '\n'.join(tokens)
        lexemes_text = '\n'.join(lexemes)

        # Display tokens in output_text and lexemes in lexeme_Def
        output_text.configure(state="normal")
        output_text.delete("1.0", END)
        output_text.insert(END, tokens_text)
        output_text.configure(state="disabled")

        lexeme_Def.configure(state="normal")
        lexeme_Def.delete("1.0", END)
        lexeme_Def.insert(END, lexemes_text)
        lexeme_Def.configure(state="disabled")

        # Delete the temporary file
        os.remove(temp_file_path)

def parse():
    global status
    # scanning
    global filepath
    if not file_opened:
        output_text.configure(state="normal")
        textbox.configure(state="normal")
        textbox.configure("1.0", END)
        output_text.delete("1.0", END)
        messagebox.showerror("File Error", "Pick a file 👍")
        textbox.configure(state="disabled")
        output_text.configure(state="disabled")
    else:
        # Read content from the textbox instead of filepath
        file_content = textbox.get("1.0", END)
        # Temporarily write content to a temporary file
        temp_file_path = os.path.join(os.path.expanduser('~'), 'temp_file.txt')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(file_content)
        
        obj = Scanner()
        tokens = obj.tokenize(temp_file_path)
        obj.export()
        # parsing
        pr_obj = Parser()
        pr_obj.tokens = tokens
        try:
            pr_obj.program()
        except ValueError as v:
            messagebox.showerror("Error", "Syntax error\n"
                                          "This code is not accepted by Tiny language")
        else:
            output_text.configure(state="normal")
            parse_tree = Util.generate_Parse_Tree(pr_obj.Nodes)
            if parse_tree:
                output_text.insert(END, "\n\nParse Tree:\n")
                output_text.insert(END, parse_tree)  # Insert the parse tree into the textbox
            else:
                # Don't add the "No parse tree generated" message
                pass
            output_text.configure(state="disabled")

        # Delete the temporary file
        os.remove(temp_file_path)

def perform_lexical_analysis():
    global filepath
    if not file_opened:
        messagebox.showerror("File Error", "Please choose a file before performing lexical analysis!")
    else:
        # Read the content from the textbox instead of the file
        code_content = textbox.get("1.0", END)

        # Check for lexical errors
        lexical_errors = check_lexical_errors(code_content)

        if lexical_errors:
            messagebox.showerror("Lexical Errors Found", "Lexical errors were found in the code:\n" + '\n'.join(lexical_errors))
        else:
            # No lexical errors, proceed with lexical analysis
            analysis_results = lexical_analysis(filepath)  # Pass filepath to maintain compatibility with the function
            messagebox.showinfo("Lexical Analysis Results", analysis_results)

def on_scroll(*args):
    output_text.yview(*args)
    lexeme_Def.yview(*args)

status = False
root = ctk.CTk()
root.resizable(False, False)
root.title('Tiny Language Compiler')

# Define a main frame to hold other frames
main_frame = ctk.CTkFrame(root, width=1400, height=700)
main_frame.pack(pady=50, padx=50)

###################### Frame 1 ######################
frame1 = ctk.CTkFrame(main_frame, width=600, height=700)
frame1.pack(side='left', padx=25, pady=20)

code_preview_icon = Image.open("Graphviz\Icons\code.png") 
code_preview_icon = code_preview_icon.resize((30, 30))  # Adjust the size as needed
code_preview_icon = ImageTk.PhotoImage(code_preview_icon)

label_frame1 = ctk.CTkLabel(frame1, text="Code Preview", fg_color="transparent", text_color="#ffffff", padx=5, pady=10, font=("Poppins", 15, "bold"),image=code_preview_icon, compound="left")
label_frame1.pack()

textbox = ctk.CTkTextbox(frame1, width=350, height=300, font=("Poppins", 15), activate_scrollbars=True)
textbox.pack(pady=20, padx=20)
textbox.configure(state="normal")

###################### Buttons ######################
buttongroup = ctk.CTkFrame(main_frame, width=600, height=700)
buttongroup.pack(side='left', padx=20, pady=20)

button = ctk.CTkButton(buttongroup, text="Upload Code", command=open_file, fg_color="red", width=150, font=("Poppins", 13, "bold"), hover_color="#cc0000", text_color="#ffffff")
button.pack(pady=10, padx=10)
button1 = ctk.CTkButton(buttongroup, text="Error Scan", command=perform_lexical_analysis, fg_color="red", width=150, font=("Poppins", 13, "bold"), hover_color="#cc0000", text_color="#ffffff")
button1.pack(pady=10, padx=10)
button2 = ctk.CTkButton(buttongroup, text="Lexical Analyzer", command=scan, fg_color="red", width=150, font=("Poppins", 13, "bold"), hover_color="#cc0000", text_color="#ffffff")
button2.pack(pady=10, padx=10)
button3 = ctk.CTkButton(buttongroup, text="Parse Tree", command=parse, fg_color="red", width=150, font=("Poppins", 13, "bold"), hover_color="#cc0000", text_color="#ffffff")
button3.pack(pady=10, padx=10)

###################### Frame 2 ######################
frame2 = ctk.CTkFrame(main_frame, width=600, height=700)
frame2.pack(side='right', padx=20, pady=20)

lexeme_analyzer_icon = Image.open("Graphviz\Icons\language.png") 
lexeme_analyzer_icon = lexeme_analyzer_icon.resize((30, 30)) 
lexeme_analyzer_icon = ImageTk.PhotoImage(lexeme_analyzer_icon)

label_frame2 = ctk.CTkLabel(frame2, text="Lexeme Analyzer", fg_color="transparent", text_color="#ffffff", padx=5, pady=10, font=("Poppins", 15, "bold"),image=lexeme_analyzer_icon, compound="left")
label_frame2.pack()

output_text = ctk.CTkTextbox(frame2, width=100, height=300, font=("Poppins", 15), activate_scrollbars=False)
output_text.pack(side="left", pady=20, padx=20)
output_text.configure(state="disabled")

lexeme_Def = ctk.CTkTextbox(frame2, width=250, height=300, font=("Poppins", 15), activate_scrollbars=False)
lexeme_Def.pack(side="left", pady=10, padx=10)
lexeme_Def.configure(state="disabled")

scrollbar = ctk.CTkScrollbar(frame2, command=on_scroll)
scrollbar.pack(side="right", fill="y")

# Bind the scrollbar to the text widgets
output_text.configure(yscrollcommand=scrollbar.set)
lexeme_Def.configure(yscrollcommand=scrollbar.set)

root.mainloop()
