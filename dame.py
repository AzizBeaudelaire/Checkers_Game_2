from tkinter import *

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

    def peutBougerVers(self, dest):
        # Simplification de la méthode
        return Mouvement().get_chemin_possible(self)  # Utilisation de la méthode de la classe Mouvement pour obtenir les mouvements possibles

class Damier(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, width=800, height=800, bg="blue")
        self.canvas.pack()
        self.creer_plateau()

        # Création de l'étiquette pour afficher le score
        self.score_label = Label(self, text="Player 1 : 0 vs J : 0", bg="#add8e6", padx=10, pady=5)
        self.score_label.pack(side=TOP, pady=10)

    def creer_plateau(self):
        global tout_les_cases
        TAILLE_GRILLE = 10
        TAILLE_CASE = 80  # Taille d'une case en pixels
        tout_les_cases = []
        for row in range(TAILLE_GRILLE):
            for col in range(TAILLE_GRILLE):
                if (row + col) % 2 == 0:
                    couleur_case = "black"
                else:
                    couleur_case = "white"
                x1 = col * TAILLE_CASE
                y1 = row * TAILLE_CASE
                x2 = x1 + TAILLE_CASE
                y2 = y1 + TAILLE_CASE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur_case)
                if (row + col) % 2 == 0:  # Placer les pions sur les cases noires
                    if row < 4:
                        couleurPion = "#9feb87"
                        pion = 1
                    elif row > 5:
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

    def creeCase(self, x1, y1, x2, y2, couleurCase):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleurCase)

    def reset(self):
        # Réinitialiser le damier en remettant tous les pions à leurs positions initiales
        for case in tout_les_cases:
            if case.pion == 1:
                case.setPion(0)
                case.setCouleurPion("")
        self.creer_plateau()

class Mouvement:
    def __init__(self, canvas, score_label, damier):
        self.canvas = canvas
        self.score_label = score_label
        self.damier = damier  # Ajout de la référence à l'instance de Damier
    
    def set_damier(self, damier_instance):
        self.damier = damier_instance 
    
    def trouverCase(self, coord):
        """Trouve et retourne la case correspondant aux coordonnées spécifiées."""
        for case in tout_les_cases:  # Utilisation de la liste globale de toutes les cases du damier
            if case and case.getCoordCase() == coord:
                return case
        return None


    def click(self, event):
        global caseDepart, pionClicker, session
        x, y = event.x, event.y
        pionClicker = 0
        caseDepart = 0
        clicker = self.canvas.find_overlapping(x, y, x, y)
        if len(clicker) > 1:
            coord = self.canvas.coords(clicker[0])
            caseDepart = self.trouverCase(coord)  # Assurez-vous que trouverCase est une méthode de votre classe
            if caseDepart and caseDepart.couleurPion == session:
                pionClicker = 0
            else:
                pionClicker = clicker[1]
        # Affiche le chemin possible lors du clic
        chemin_possible = self.get_chemin_possible(caseDepart)
        for case in chemin_possible:
            self.canvas.create_rectangle(
                case.getCoordCase(), outline="green", width=2, dash=(4, 4)
            )

    def click_choice(self, event):
        global caseDepart, pionClicker
        x, y = event.x, event.y
        if caseDepart and pionClicker:
            coord = self.canvas.coords(pionClicker)
            cases_diagonales = self.get_cases_diagonales_libres(caseDepart)
            for case in cases_diagonales:
                if case.getCoordCase() == [x, y, x, y]:
                    self.deplacer_pion(case)
                    self.manger_pion(caseDepart, case)
                    break

    def bouger(self, event):
        global caseDepart, pionClicker
        x, y = event.x, event.y
        if caseDepart and pionClicker:
            coord = self.canvas.coords(pionClicker)
            deplacement = [[x - 10, y - 10, x + 10, y + 10]]
            self.canvas.coords(pionClicker, deplacement[0])

    def arret(self, event):
        global caseDepart, pionClicker, session
        global scoreV, scoreJ
        x, y = event.x, event.y
        collision = self.canvas.find_overlapping(x - 10, y - 10, x + 10, y + 10)
        coord = self.canvas.coords(collision[0])
        caseSupprimer = None
        if not caseDepart.peutBougerVers(coord):  # Assurez-vous que peutBougerVers est une méthode de votre classe
            self.canvas.coords(pionClicker, caseDepart.getCoordPion())
        else:
            caseDest = self.trouverCase(coord)  # Assurez-vous que trouverCase est une méthode de votre classe
            if not caseDepart.__eq__(caseDest):
                session = caseDepart.couleurPion
            caseDest.setPion(1)
            caseDest.setCouleurPion(caseDepart.couleurPion)
            self.canvas.coords(pionClicker, caseDest.getCoordPion())
            caseDepart.setPion(0)
            caseDest.setCouleurPion("")

            if caseDest.__eq__(caseDepart.gauche().gauche()):
                caseSupprimer = caseDepart.gauche()
            elif caseDest.__eq__(caseDepart.droite().droite()):
                caseSupprimer = caseDepart.droite()
            elif caseDest.__eq__(caseDepart.haut().haut()):
                caseSupprimer = caseDepart.haut()
            elif caseDest.__eq__(caseDepart.bas().bas()):
                caseSupprimer = caseDepart.bas()

            if caseSupprimer:
                if caseSupprimer.couleurPion == "#9feb87":
                    scoreJ += 1
                else:
                    scoreV += 1
                self.score_label.configure(text="V : {} vs J : {}".format(scoreV, scoreJ))

                if scoreJ >= 12:
                    self.score_label.configure(text="Victoire de J : {}".format(scoreJ))
                elif scoreV >= 12:
                    self.score_label.configure(text="Victoire de V : {}".format(scoreV))
                c = caseSupprimer.getCoordPion()
                pionSuppprimer = self.canvas.find_overlapping(c[0], c[1], c[2], c[3])
                self.canvas.delete(pionSuppprimer[1])
                caseSupprimer.setPion(0)

    def get_chemin_possible(self, case_depart):
        chemin_possible = []
        # Vérifiez si la case de départ est valide
        if case_depart:
            # Obtenez les coordonnées de la case de départ
            x, y = case_depart.getCoordPion()[0], case_depart.getCoordPion()[1]
            # Obtenez les cases diagonales possibles
            cases_diagonales = [case_depart.gauche().haut(), case_depart.droite().haut()]
            # Ajoutez les cases diagonales possibles à la liste du chemin possible
            for case_diagonale in cases_diagonales:
                if case_diagonale and self.is_case_vide(case_diagonale):
                    chemin_possible.append(case_diagonale)
        return chemin_possible

    def deplacer_pion(self, case_dest):
        """Déplace le pion vers la case de destination."""
        global caseDepart, pionClicker
        if caseDepart and pionClicker and case_dest:
            # Déplacez le pion vers la case de destination
            coord = case_dest.getCoordPion()
            self.canvas.coords(pionClicker, coord)
            # Mettez à jour les attributs de caseDepart et pionClicker
            caseDepart.setPion(0)
            caseDepart.setCouleurPion("")
            case_dest.setPion(1)
            case_dest.setCouleurPion(caseDepart.couleurPion)
            caseDepart = None
            pionClicker = None

    def manger_pion(self, case_depart, case_dest):
        """Vérifie et effectue si possible la capture d'un pion adverse."""
        global caseDepart, pionClicker, session, scoreV, scoreJ
        if case_depart and case_dest:
            # Vérifiez si le déplacement est valide pour la capture
            if self.is_case_adverse(case_dest):
                # Effectuez le déplacement et retirez le pion adverse du damier
                coord = case_dest.getCoordPion()
                self.canvas.coords(pionClicker, coord)
                caseDepart.setPion(0)
                caseDepart.setCouleurPion("")
                case_dest.setPion(1)
                case_dest.setCouleurPion(caseDepart.couleurPion)
                # Mettez à jour les scores
                if case_dest.couleurPion == "#9feb87":
                    scoreJ += 1
                else:
                    scoreV += 1
                self.score_label.configure(text="V : {} vs J : {}".format(scoreV, scoreJ))
                # Vérifiez s'il y a une victoire
                if scoreJ >= 12:
                    self.score_label.configure(text="Victoire de J : {}".format(scoreJ))
                elif scoreV >= 12:
                    self.score_label.configure(text="Victoire de V : {}".format(scoreV))
                # Supprimez le pion adverse
                c = case_dest.getCoordPion()
                pionSuppprimer = self.canvas.find_overlapping(c[0], c[1], c[2], c[3])
                self.canvas.delete(pionSuppprimer[1])
                case_dest.setPion(0)
                case_dest.setCouleurPion("")

    def is_case_valide(self, coord):
        """Vérifie si les coordonnées spécifiées représentent une case valide sur le damier."""
        # Vérifiez si les coordonnées sont à l'intérieur du damier
        return 0 < coord[0] < 600 and 0 < coord[1] < 600

    def is_case_vide(self, case):
        """Vérifie si la case spécifiée est vide."""
        return case and case.pion == 0

    def is_case_adverse(self, case):
        """Vérifie si la case spécifiée contient un pion adverse."""
        return case and case.pion == 1 and case.couleurPion != session

    def is_case_blanche(self, case):
        """Vérifie si la case spécifiée contient un pion du joueur blanc."""
        return case and case.pion == 1 and case.couleurPion == "#ffde01"

    def is_case_noire(self, case):
        """Vérifie si la case spécifiée contient un pion du joueur noir."""
        return case and case.pion == 1 and case.couleurPion == "#9feb87"

    def get_cases_diagonales_libres(self, case):
        """Retourne une liste des cases diagonales adjacentes à la case spécifiée qui sont vides."""
        cases_diagonales = []
        if case:
            # Obtenez les cases diagonales adjacentes
            gauche_haut = case.gauche().haut()
            droite_haut = case.droite().haut()
            # Vérifiez si les cases diagonales sont vides
            if self.is_case_vide(gauche_haut):
                cases_diagonales.append(gauche_haut)
            if self.is_case_vide(droite_haut):
                cases_diagonales.append(droite_haut)
        return cases_diagonales


