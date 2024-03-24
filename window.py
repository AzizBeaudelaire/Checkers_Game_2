import tkinter as tk
from dame import Damier
from button import MyButton
from dame import Mouvement  # Importez votre classe Mouvement depuis le fichier approprié

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu de Dame")
        self.geometry("1060x1060")
        
        ## Création du damier à intégrer dans la fenêtre
        self.damier = Damier(self)
        self.damier.pack(fill=tk.BOTH, expand=True)

        # Création de l'instance de la classe Mouvement
        self.mouvement = Mouvement(self.damier.canvas, self.damier.score_label, self.damier)  # Ajout de l'instance de Damier

        # Liaison des événements de clic de la souris à la classe Mouvement
        self.damier.canvas.bind("<Button-1>", self.mouvement.click)
        self.damier.canvas.bind("<Button-2>", self.mouvement.click_choice)
        self.damier.canvas.bind("<B1-Motion>", self.mouvement.bouger)
        self.damier.canvas.bind("<ButtonRelease-1>", self.mouvement.arret)
        
        # Création des boutons pour quitter et recommencer
        self.quit_button = MyButton(self, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.restart_button = MyButton(self, text="Recommencer", command=self.restart)
        self.restart_button.pack(side=tk.RIGHT)

        # Liaison de l'instance de Damier avec l'instance de Mouvement
        self.mouvement.set_damier(self.damier)  # Ajout de cette ligne


    def restart(self):
        # Fonction à appeler pour recommencer le jeu
        self.damier.reset()
