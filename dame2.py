from tkinter import *


class Case:
    def __init__(self, x1, y1, x2, y2, couleurCase, couleurPion, pion):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.couleurCase = couleurCase
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
        return [self.x1 + 15, self.y1 + 15, self.x2 - 15, self.y2 - 15]

    def setPion(self, val):
        self.pion = val

    def setCouleurPion(self, val):
        self.couleurPion = val

    def creeCase(self):
        can.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.couleurCase)

    def placerPion(self):
        if self.pion:
            can.create_oval(
                self.x1 + 35,
                self.y1 + 35,
                self.x2 - 35,
                self.y2 - 35,
                fill=self.couleurPion,
            )

    def peutBougerVers(self, dest):
        caseDest = trouverCase(dest)
        if not caseDest:
            return False
        else:
            if (
                caseDest.pion
                or abs(dest[0] - self.x1) != 40
                or abs(dest[1] - self.y1) != 40
            ):
                return False
            return True


def creer_plateau():
    global can, score, tout_les_cases
    TAILLE_GRILLE = 10
    TAILLE_CASE = 40  # Taille d'une case en pixels
    tout_les_cases = []
    for row in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            if (row + col) % 2 == 0:
                couleur_case = "#f07ab7"
            else:
                couleur_case = "white"
            x1 = col * TAILLE_CASE
            y1 = row * TAILLE_CASE
            x2 = x1 + TAILLE_CASE
            y2 = y1 + TAILLE_CASE
            can.create_rectangle(x1, y1, x2, y2, fill=couleur_case)
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
                tout_les_cases.append(
                    Case(x1, y1, x2, y2, couleur_case, couleurPion, pion)
                )
                tout_les_cases[-1].creeCase()
                if tout_les_cases[-1].pion:
                    tout_les_cases[-1].placerPion()


def trouverCase(coord):
    if coord:  # Vérifie si coord n'est pas une liste vide
        for case in tout_les_cases:
            if (
                case.x1 == coord[0]
                and case.y1 == coord[1]
                and case.x2 == coord[2]
                and case.y2 == coord[3]
            ):
                return case
    return None


def click(event):
    global case_depart, pion_clicker
    x, y = event.x, event.y
    pion_clicker = 0
    case_depart = 0
    for case in tout_les_cases:
        if case.x1 < x < case.x2 and case.y1 < y < case.y2:
            if case.pion:
                case_depart = case
                pion_clicker = can.create_oval(
                    case.x1 + 5,
                    case.y1 + 5,
                    case.x2 - 5,
                    case.y2 - 5,
                    fill=case.couleurPion,
                )
                return


def bouger(event):
    global case_depart, pion_clicker
    x, y = event.x, event.y
    if case_depart and pion_clicker:
        coord = can.coords(pion_clicker)
        dx = x - coord[0] - 20
        dy = y - coord[1] - 20
        can.move(pion_clicker, dx, dy)


def deplacement_normal(coord_depart, coord_arrivee):
    dx = coord_arrivee[0] - coord_depart[0]
    dy = coord_arrivee[1] - coord_depart[1]
    # Vérifie si le déplacement est diagonal
    if abs(dx) == abs(dy):
        # Vérifie si le déplacement est vers l'avant
        if coord_arrivee[1] > coord_depart[1]:
            # Vérifie si la case d'arrivée est vide
            case_dest = trouverCase(coord_arrivee)
            if not case_dest.pion:
                return True
        else:
            # Si le pion atteint la dernière rangée adverse, il devient une dame
            if case_depart.pion == 1 and coord_arrivee[1] == 0:
                case_depart.pion = 3
            elif case_depart.pion == 2 and coord_arrivee[1] == 350:
                case_depart.pion = 4
            return True
    return False


def deplacement_capture(coord_depart, coord_arrivee):
    dx = coord_arrivee[0] - coord_depart[0]
    dy = coord_arrivee[1] - coord_depart[1]
    # Vérifie si le déplacement est diagonal avec une distance de 2 cases
    if abs(dx) == 100 and abs(dy) == 100:
        # Calculer les coordonnées de la case intermédiaire
        x_intermediaire = (coord_depart[0] + coord_arrivee[0]) / 2
        y_intermediaire = (coord_depart[1] + coord_arrivee[1]) / 2
        case_intermediaire = trouverCase([x_intermediaire, y_intermediaire, 0, 0])
        if case_intermediaire and case_intermediaire.pion != case_depart.pion:
            # Vérifier si la case d'arrivée est vide
            case_dest = trouverCase(coord_arrivee)
            if not case_dest.pion:
                # Capture le pion adverse
                can.delete(case_intermediaire.pion)
                case_intermediaire.pion = 0
                return True
    return False


def deplacement(event):
    global case_depart, pion_clicker
    x, y = event.x, event.y
    if case_depart and pion_clicker:
        coord_arrivee = [x - 20, y - 20, x + 20, y + 20]
        if deplacement_capture(pion_clicker, coord_arrivee):
            can.coords(pion_clicker, coord_arrivee)
            return
        elif deplacement_normal(pion_clicker, coord_arrivee):
            can.coords(pion_clicker, coord_arrivee)


# Initialisation des variables
tout_les_cases = []
caseDepart = None
pionClicker = None

# Création de la fenêtre principale
fen = Tk()
fen.title("Jeu de Dame")

# Création du canevas pour le plateau de jeu
can = Canvas(fen, width=400, height=400, bg="pink")
can.pack()

# Création du plateau de jeu
creer_plateau()

# Liaison des événements de souris
can.bind("<Button-1>", click)
can.bind("<B1-Motion>", bouger)

# Démarrage de la boucle principale Tkinter
fen.mainloop()
