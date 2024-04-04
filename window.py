import tkinter as tk
from dame import Damier
from Game import Game

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu de Dame")
        self.geometry("1060x1060")

        # Ajout du bouton "Lancer la partie"
        self.start_button = tk.Button(self, text="Lancer la partie", command=self.lancer_partie)
        self.start_button.pack(side=tk.BOTTOM)

        # Création des boutons pour quitter et recommencer
        self.quit_button = tk.Button(self, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.restart_button = tk.Button(self, text="Recommencer", command=self.restart)
        self.restart_button.pack(side=tk.RIGHT)

    def restart(self):
        # Fonction à appeler pour recommencer le jeu
        self.damier.reset()

    def lancer_partie(self):
        # Création d'une instance de la classe Game
        game = Game()

        # Création de l'instance de Damier
        self.damier = Damier(self)
        self.damier.pack(fill=tk.BOTH, expand=True)

        # Appel à la méthode deroulement_du_jeu de l'instance game
        game.deroulement_du_jeu(score_label=self.damier.score_label)  # Passer score_label du damier

        # Liaison des événements de clic de la souris à la classe Mouvement
        self.damier.canvas.bind("<Button-1>", self.damier.mouvement.click)
        self.damier.canvas.bind("<B1-Motion>", self.damier.mouvement.bouger)
        self.damier.canvas.bind("<ButtonRelease-1>", self.damier.mouvement.arret)

        # Affichage du graphe des scores
        #self.damier.afficher_graphe_scores()
