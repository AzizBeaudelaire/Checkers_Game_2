import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import Canvas, Label, Frame, messagebox, TOP  # Importez la classe Frame

class Case:
    def __init__(self, master=None, x1=0, y1=0, x2=0, y2=0, couleur_case="", couleurPion="", pion=0):
        self.master = master
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.couleur_case = couleur_case
        self.couleurPion = couleurPion
        self.pion = pion
    
    def __eq__(self, other):
        return (
            self.x1 == other.x1
            and self.y1 == other.y1
            and self.x2 == other.x2
            and self.y2 == other.y2
        )
    
    def getCoordCase(self):
        return [self.x1, self.y1, self.x2, self.y2]
    
    def getCoordPion(self):
        return [self.x1 + 10, self.y1 + 10, self.x2 - 10, self.y2 - 10]
    
    def setPion(self, val):
        self.pion = val
    
    def setCouleurPion(self, val):
        self.couleurPion = val
    
    def placerPion(self, canvas):
        if self.pion:
            canvas.create_oval(
                self.x1 + 10,
                self.y1 + 10,
                self.x2 - 10,
                self.y2 - 10,
                fill=self.couleurPion,
            )
    
    def gauche(self):
        # Retourne la case à gauche de la case actuelle
        return Case(self.master, self.x1 - (self.x2 - self.x1), self.y1, self.x1, self.y2, self.couleur_case, self.couleurPion, self.pion)
    
    def droite(self):
        # Retourne la case à droite de la case actuelle
        return Case(self.master, self.x2, self.y1, self.x2 + (self.x2 - self.x1), self.y2, self.couleur_case, self.couleurPion, self.pion)
    
    def haut(self):
        # Retourne la case au-dessus de la case actuelle
        return Case(self.master, self.x1, self.y1 - (self.y2 - self.y1), self.x2, self.y1, self.couleur_case, self.couleurPion, self.pion)
    
    def bas(self):
        # Retourne la case en-dessous de la case actuelle
        return Case(self.master, self.x1, self.y2, self.x2, self.y2 + (self.y2 - self.y1), self.couleur_case, self.couleurPion, self.pion)
    
    def peutBougerVers(self, dest):
        """Vérifie si la case peut se déplacer vers la case de destination."""
        if isinstance(dest, Case):  # Vérifie si dest est une instance de la classe Case
            if dest:
                # Vérifier si la destination est une case vide
                if dest.pion == 0:
                    # Vérifier si la destination est accessible selon les règles des pions
                    if self.pion == 1:  # Si c'est un pion blanc
                        if dest.x1 > self.x1:  # Le pion blanc ne peut se déplacer que vers le bas
                            return True
                    elif self.pion == 2:  # Si c'est un pion noir
                        if dest.x1 < self.x1:  # Le pion noir ne peut se déplacer que vers le haut
                            return True
                else:
                    # Vérifier si la destination est accessible selon les règles des dames
                    if self.pion == 1:  # Si c'est un pion blanc
                        if dest.x1 > self.x1:  # La dame blanche peut se déplacer vers le bas ou l'avant
                            return True
                    elif self.pion == 2:  # Si c'est un pion noir
                        if dest.x1 < self.x1:  # La dame noire peut se déplacer vers le haut ou l'arrière
                            return True
        return False
    
class Damier(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.scoreJ = 0
        self.scoreV = 0
        self.canvas = Canvas(self, width=800, height=800, bg="blue")
        self.canvas.pack()
        self.creer_plateau()
        # Création de l'étiquette pour afficher le score
        self.score_label = Label(self, text="Player 1 : 0 vs J : 0", bg="#add8e6", padx=10, pady=5)
        self.score_label.pack(side=tk.TOP, pady=10)
        # Initialisation de l'attribut mouvement avec une instance de la classe Mouvement
        self.mouvement = Mouvement(self.canvas, self.score_label, self) 
        
    def creer_plateau(self):
        global tout_les_cases
        TAILLE_GRILLE = 10
        TAILLE_CASE = 80  # Taille d'une case en pixels
        tout_les_cases = []
        # Créer une grille de coordonnées avec NumPy
        x = np.arange(0, 800, TAILLE_CASE)
        y = np.arange(0, 800, TAILLE_CASE)
        X, Y = np.meshgrid(x, y)
        for i in range(TAILLE_GRILLE):
            for j in range(TAILLE_GRILLE):
                if (i + j) % 2 == 0:
                    couleur_case = "black"
                else:
                    couleur_case = "white"
                x1, y1 = X[i, j], Y[i, j]
                x2, y2 = x1 + TAILLE_CASE, y1 + TAILLE_CASE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur_case)
                if (i + j) % 2 == 0:  # Placer les pions sur les cases noires
                    if i < 4:
                        couleurPion = "#9feb87"
                        pion = 1
                    elif i > 5:
                        couleurPion = "#ffde01"
                        pion = 2
                    else:
                        couleurPion = ""
                        pion = 0
                    # Créer une instance de la classe Case
                    case = Case(master=self, x1=x1, y1=y1, x2=x2, y2=y2, couleur_case=couleur_case, couleurPion=couleurPion, pion=pion)
                    tout_les_cases.append(case)
                    if case.pion:
                        case.placerPion(self.canvas)  # Passer canvas comme argument
                        
    def afficher_graphe_scores(self):
        joueurs = ['Player1', 'IA']
        scores = [self.scoreV, self.scoreJ]
        plt.bar(joueurs, scores, color=['blue', 'green'])
        plt.xlabel('Joueurs')
        plt.ylabel('Scores')
        plt.title('Scores des joueurs')
        plt.show()
        
    def creeCase(self, x1, y1, x2, y2, couleurCase):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleurCase)
        
    def reset(self):
        # Détruire le canvas existant
        self.canvas.destroy()
        
        # Créer un nouveau canvas et plateau de jeu
        self.canvas = Canvas(self, width=800, height=800, bg="blue")
        self.canvas.pack()
        self.creer_plateau()
        
class Mouvement:
    def __init__(self, canvas, score_label, damier):
        self.score_label = score_label
        self.damier = damier
        self.canvas = canvas
        self.caseDepart = None
        self.pionClicker = None
        self.session = ""  # Initialisation de la session ici

    def is_case_vide(self, case):
        return case and case.pion == 0
    
    def click(self, event):
        x, y = event.x, event.y
        clicker = self.canvas.find_overlapping(x, y, x, y)
        if len(clicker) > 1:
            coord = self.canvas.coords(clicker[0])
            self.caseDepart = self.trouverCase(coord)
            if self.caseDepart and self.caseDepart.couleurPion == self.session:
                self.pionClicker = None
            else:
                self.pionClicker = clicker[1]
        chemin_possible = self.get_chemin_possible(self.caseDepart)
        self.afficher_chemin_possible(chemin_possible)

    def bouger(self, event):
        x, y = event.x, event.y
        if self.caseDepart and self.pionClicker:
            caseCible = self.trouverCase([x, y, x, y])  # Trouver la case cible selon les coordonnées du clic
            if caseCible in self.get_chemin_possible(self.caseDepart):  # Vérifier si la case cible est valide
                coord = caseCible.getCoordPion()  # Obtenir les coordonnées de la case cible
                self.canvas.coords(self.pionClicker, coord)  # Déplacer le pion vers la case cible
                self.caseDepart.setPion(0)
                caseCible.setPion(1)
                caseCible.setCouleurPion(self.caseDepart.couleurPion)
                self.caseDepart.setCouleurPion("")
                self.caseDepart = None
                self.pionClicker = None

    def arret(self, event):
        x, y = event.x, event.y
        collision = self.canvas.find_overlapping(x - 10, y - 10, x + 10, y + 10)
        if collision:  # Vérifier si collision n'est pas vide
            coord = self.canvas.coords(collision[0])
            caseDest = self.trouverCase(coord)
            if caseDest:
                if self.caseDepart and not self.caseDepart.peutBougerVers(coord):
                    self.canvas.coords(self.pionClicker, self.caseDepart.getCoordPion())
                else:
                    if caseDest != self.caseDepart:
                        self.session = self.caseDepart.couleurPion
                    caseDest.setPion(1)
                    caseDest.setCouleurPion(self.caseDepart.couleurPion)
                    self.canvas.coords(self.pionClicker, caseDest.getCoordPion())
                    self.caseDepart.setPion(0)
                    self.caseDepart.setCouleurPion("")
                    self.caseDepart = None
                    self.pionClicker = None
                    self.check_and_remove_opponent_piece(caseDest)

    def get_chemin_possible(self, case_depart):
        chemin_possible = []
        if case_depart:
            cases_diagonales = [
                case_depart.gauche().haut(),
                case_depart.droite().haut(),
                case_depart.gauche().bas(),
                case_depart.droite().bas()
            ]
            for case_diagonale in cases_diagonales:
                if case_diagonale and self.is_case_vide(case_diagonale):
                    chemin_possible.append(case_diagonale)
        return chemin_possible

    def afficher_chemin_possible(self, cases):
        for case in cases:
            self.canvas.create_rectangle(
                case.getCoordCase(), outline="green", width=2, dash=(4, 4)
            )

    def trouverCase(self, coord):
        for case in tout_les_cases:
            if case and case.getCoordCase() == coord:
                return case
        return None

    def check_and_remove_opponent_piece(self, case_dest):
        global scoreV, scoreJ
        if case_dest:
            # Vérifier si une pièce adverse est présente à proximité
            cases_adjacentes = [
                case_dest.gauche().gauche(),
                case_dest.droite().droite(),
                case_dest.haut().haut(),
                case_dest.bas().bas()
            ]
            for case_adjacente in cases_adjacentes:
                if case_adjacente and not self.is_case_vide(case_adjacente) and self.is_case_adverse(case_adjacente):
                    scoreV += 1 if case_adjacente.couleurPion == "#ffde01" else 0
                    scoreJ += 1 if case_adjacente.couleurPion == "#9feb87" else 0
                    self.score_label.configure(text="V : {} vs J : {}".format(scoreV, scoreJ))
                    self.canvas.delete(case_adjacente.pion_id)
                    case_adjacente.setPion(0)
                    case_adjacente.setCouleurPion("")
    
    def calculer_score(self):
        scoreJ = sum(1 for case in tout_les_cases if case.couleurPion == "#9feb87")
        scoreV = sum(1 for case in tout_les_cases if case.couleurPion == "#ffde01")
        return scoreJ, scoreV
    
    def afficher_score(self, scoreV, scoreJ):
        self.score_label.configure(text="V : {} vs J : {}".format(scoreV, scoreJ))
        
    def victoire(self, scoreJ, scoreV):
        if scoreJ >= 12:
            messagebox.showinfo("Fin de partie", "Victoire de J : {}".format(scoreJ))
            return True
        elif scoreV >= 12:
            messagebox.showinfo("Fin de partie", "Victoire de IA : {}".format(scoreV))
            return True
        return False
    
#Pensez a return dans un excel la le mouvement effectué ainsi que la liste de pions restants 
#Pensez a utiliser matplolib pour afficher un diagramme des coups joués
#supprimer le drag and drope et juste click sur le pion, click sur la case ou ddeplacer
