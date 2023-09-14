
# !!! THIS PROJECT IS UNDER MIT LICENCE !!!


#ENGLISH VERSION:
"""
Copyright © 2023 ItsPyDevs (https://github.com/ItsPyDevs)

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the “Software”), 
to deal in the Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, 
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#FRENCH VERSION:
"""
Copyright © 2023 ItsPyDevs (https://github.com/ItsPyDevs)

L'autorisation est accordée gratuitement à toute personne obtenant une copie
de ce logiciel et des fichiers de documentation associés (le « Logiciel »),
utiliser le Logiciel sans restriction, y compris, sans limitation, les droits d'utilisation,
copier, modifier, fusionner, publier, distribuer, accorder des sous-licences et/ou vendre des copies du Logiciel,
et permettre aux personnes à qui le Logiciel est fourni de le faire, sous réserve des conditions suivantes :
L'avis de droit d'auteur ci-dessus et cet avis d'autorisation doivent être inclus dans toutes les copies ou
des parties substantielles du Logiciel.

LE LOGICIEL EST FOURNI « EN L'ÉTAT »,
SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU IMPLICITE,
Y COMPRIS MAIS SANS LIMITATION LES GARANTIES DE QUALITÉ MARCHANDE,
APTITUDE À UN USAGE PARTICULIER ET NON-VIOLATION.
EN AUCUN CAS LES AUTEURS OU LES TITULAIRES DES DROITS D'AUTEUR NE SERONT RESPONSABLES DE TOUTE RÉCLAMATION,
DOMMAGES OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS UNE ACTION DE CONTRAT,
DÉLIT OU AUTRE, DÉCOULANT DE,
HORS OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES AFFAIRES DANS LE LOGICIEL.
"""
import sys
import threading
import os
from tkinter import (LabelFrame, Tk, Label, Text, messagebox, Toplevel, Entry, Button, END, Menu, LEFT, RIGHT, Frame, X, Y, BOTTOM)

dark_mode = True #Change if you want Default Dark mod or white mode at start (Value accepted: True/False)

class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, text): self.text_widget.insert(END, text)  ;  self.text_widget.see(END)


class ExecutionThread(threading.Thread):
    def __init__(self, code, console):
        super().__init__()  ;  self.code = code ; self.console = console
    def run(self):
        self.redirect_output()
        try: exec(compile(self.code, "<string>", "exec"), globals())
        except Exception as e: print("Error:", e)
        finally: self.restore_output()

    def redirect_output(self):
        self.original_streams = sys.stdout, sys.stderr  ;  sys.stdout, sys.stderr = ConsoleRedirect(self.console), ConsoleRedirect(self.console)
    def restore_output(self):
        sys.stdout, sys.stderr = self.original_streams

def execute_code():
    code = code_editor.get("1.0", END) ; console.delete("1.0", END) ; execute(execute_code_in_thread, code)
def execute(func, *args):
    threading.Thread(target=func, args=args).start()

def execute_code_in_thread(code):
    ExecutionThread(code, console).start()

def exit_application():
    if messagebox.askyesno("Confirm", "Do you really want to exit the application?"): root.destroy()


def run(command, text_widget):
    try:
        
        text_widget.insert(END, os.system(command))
    except Exception as e: text_widget.insert(END, str(e))

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    setTheme(dark_mode)

def setTheme(dark_mode):
    theme_color = {
        'bg':"black",
        'fg':"white",
        'cursor': 'white'
    }
    if dark_mode:
        theme_color = {
            'bg':"black",
            'fg':"white",
            'cursor': 'white'
        }
    else:
        theme_color = {
            'bg':"white",
            'fg':"black",
            'cursor': 'black'
        }
    
    root.configure(bg=theme_color['bg'])
    root.tk_setPalette(background=theme_color['bg'], foreground=theme_color['fg'])
    widget = []
    widget.append(code_editor)
    widget.append(console)
    for i in widget:
        i.config(bg=theme_color['bg'], fg=theme_color['fg'])
        if isinstance(i, Entry) or isinstance(i, Text):
            i.config(insertbackground=theme_color['cursor'])

def popup():
    popup = Toplevel(root)  ;  popup.title("Enter Hex Color Code")  ;  label = Label(popup, text="Enter a valid HEX color code:") ; label.pack(padx=10, pady=5) ; entry = Entry(popup) ; entry.pack(padx=10, pady=5)  ;  error_label = Label(popup, text="", fg="red") ; error_label.pack(padx=10, pady=5)
    def apply_color():
        color_code = entry.get()
        if len(color_code) == 7 and color_code[0] == "#" and all(c in "0123456789abcdefABCDEF" for c in color_code[1:]):
            for button in [run_button, quit_button, dark_mode_button, configuration_button]:
                button.config(bg=color_code)
            popup.destroy()
        else: error_label.config(text="Invalid HEX color code")
    
    apply_button = Button(popup, text="Apply", command=apply_color)  ;  apply_button.pack(padx=10, pady=5)

root = Tk()  ;  root.configure(bg="black")  ;  root.geometry("1075x600")  ;  root.title("PyCoré")   ;   root.resizable(False, False)
menu_bar = Menu(root)  ;  root.config(menu=menu_bar)
code_menu = Menu(menu_bar, tearoff=0) ; code_menu.add_command(label="Run", command=execute_code) ; code_menu.add_separator() ; code_menu.add_command(label="Quit", command=exit_application) ; menu_bar.add_cascade(label="Code", menu=code_menu) ; config_menu = Menu(menu_bar, tearoff=0) ; config_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode) ; config_menu.add_command(label="Button Color", command=popup) ; menu_bar.add_cascade(label="Configuration", menu=config_menu)

code_frame = LabelFrame(root, text="Code Editor", labelanchor="n") ; code_frame.pack(side=LEFT, padx=10, pady=10, fill=Y) ; console_frame = LabelFrame(root, text="Console", labelanchor="n") ; console_frame.pack(side=RIGHT, padx=10, pady=10, fill=Y)
module_frame = LabelFrame(root, text="Module Console", labelanchor="n") ; module_frame.pack(side=BOTTOM, padx=10, pady=10, fill=X)
code_editor = Text(code_frame, height=15, width=40, wrap=None) ; code_editor.pack(fill=X, padx=10, pady=5)
console = Text(console_frame, height=15, width=40) ; console.pack(fill=X, padx=10, pady=5)

button_frame = Frame(root) ; button_frame.pack(side=LEFT, fill=Y)

run_button = Button(button_frame, text="Run", command=execute_code) ; run_button.pack(fill=X,padx=3, side=LEFT)
quit_button = Button(button_frame, text="Quit", command=exit_application) ; quit_button.pack(fill=X, side=LEFT,padx=3)
dark_mode_button = Button(root, text="Toggle Dark Mode", command=toggle_dark_mode) ; dark_mode_button.pack(side=LEFT,padx=3)
configuration_button = Button(root, text="Set Button Color", command=popup) ; configuration_button.pack(side=LEFT,padx=3)

console.bind("<Key>", lambda e: "break")

if __name__ == "__main__":
    setTheme(dark_mode)
    root.mainloop()
