import tkinter as tk
from dame import Damier
from button import MyButton

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu de Dame")
        self.geometry("860x845")
        
        ## Création du damier à intégrer dans la fenêtre
        self.damier = Damier(self)
        self.damier.pack(fill=tk.BOTH, expand=True)
        
        # Création des boutons pour quitter et recommencer
        self.quit_button = MyButton(self, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.restart_button = MyButton(self, text="Recommencer", command=self.restart)
        self.restart_button.pack(side=tk.RIGHT)

    def restart(self):
        # Fonction à appeler pour recommencer le jeu
        self.damier.reset()