import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master, text, command=None):
        self.text = text
        tk.Button.__init__(self, master, text=self.text, command=command)
        self.configure(width=10, height=2)  # Ajustez la largeur et la hauteur selon vos préférences
        self.configure(bg='#4CAF50', fg='white')  # Couleur de fond verte et texte blanc
        self.configure(font=('Arial', 14))  # Police et taille du texte
        self.configure(relief=tk.FLAT)  # Pas de relief sur le bouton
        self.configure(activebackground='#45a049')  # Couleur de fond au survol
        self.configure(activeforeground='white')  # Couleur du texte au survol
