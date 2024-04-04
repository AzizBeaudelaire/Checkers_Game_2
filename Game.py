import pandas as pd
from dame import Damier, Mouvement, Case

class Game:
    def __init__(self):
        self.historique_coups = []
        self.damier = None
    
    @staticmethod
    def demarrer_partie():
        # Créer une instance de la classe Damier
        damier_instance = Damier()
        damier_instance.creer_plateau()  # Créer le plateau de jeu

        # Vous pouvez ajouter d'autres logiques d'initialisation ici, comme la distribution des pions, etc.

        # Retourner l'instance du damier
        return damier_instance


    def enum_infos_requises(self, nom_joueur, nb_coups, coord_pion, nb_pions_vivants):
        infos = {
            'Nom Joueur': nom_joueur,
            'Nombre de Coups': nb_coups,
            'Coordonnées Pion': coord_pion,
            'Nombre de Pions Vivants': nb_pions_vivants
        }
        return infos

    def enregistrer_historique(self):
        # Liste pour stocker les informations de chaque coup
        historique = []
    
        # Parcours de la liste des coups
        for coup in self.historique_coups:
            # Utilisation de la fonction enum_infos_requises pour obtenir les informations requises
            infos = self.enum_infos_requises(coup['Nom Joueur'], coup['Nombre de Coups'], coup['Coordonnées Pion'], coup['Nombre de Pions Vivants'])
            historique.append(infos)
    
        # Création du DataFrame à partir de la liste des informations
        df = pd.DataFrame(historique)
    
        # Enregistrement dans un fichier CSV
        df.to_csv('historique_partie.csv', index=False)
        print("Historique de la partie enregistré dans 'historique_partie.csv'.")
    
    def creer_tour(self):
        # Logique pour créer un tour de jeu
        # Vous pouvez ajouter ici la logique pour déplacer les pièces, vérifier les règles du jeu, etc.
        print("Un nouveau tour de jeu est créé.")


    def deroulement_du_jeu(self, score_label):
        # Créer une instance de Damier
        damier = Damier()  # Créez une instance de la classe Damier
    
        # Appel à la méthode pour démarrer la partie
        self.demarrer_partie()
    
        # Créer une instance de Mouvement en passant canvas, score_label et damier comme arguments
        mouvement = Mouvement(damier.canvas, score_label, damier)
    
        # Initialiser les scores en utilisant la méthode calculer_score de l'instance de Mouvement
        scoreJ, scoreV = mouvement.calculer_score()
        
        i = 0
        while scoreJ < 12 and scoreV < 12:
            # Appeler la fonction qui gère un tour de jeu
            # Par exemple, vous pouvez appeler la fonction pour choisir un mouvement à effectuer
            # et ensuite mettre à jour le score en fonction du mouvement effectué.
            # Voici un exemple de ce que cela pourrait ressembler :
            # mouvement = self.choisir_mouvement()
            # self.effectuer_mouvement(mouvement)
        
            # Mettre à jour le score en utilisant la méthode calculer_score de l'instance de Mouvement
            scoreJ, scoreV = mouvement.calculer_score()
        
            # Vérifier si l'un des joueurs a gagné
            mouvement.victoire(scoreJ, scoreV)
        
            i += 1
    