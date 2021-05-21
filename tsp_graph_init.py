import numpy as np
import random
import pandas as pd

random.seed(1)
np.random.seed(1)

class Lieu:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def distance(cls, lieu1, lieu2):
        return np.sqrt((lieu1.x-lieu2.x)**2 + (lieu1.y-lieu2.y)**2)


class Graph:

    def __init__(self, largeur, hauteur, array_lieux, nb_lieux=10):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        if np.any(array_lieux) :
            self.liste_lieux = self.creer_liste_lieux(array_lieux)
        else :
            self.liste_lieux = self.creer_liste_lieux_aleatoire(nb_lieux)
        self.NB_LIEUX = len(self.liste_lieux)
        print("#####", self.NB_LIEUX)
        self.matrice_od = self.calcul_matrice_cout_od()
        self.ordre_aleatoire = Route.def_ordre(self.NB_LIEUX)
        self.distance = Route.calcul_distance_route(self.ordre_aleatoire, self.matrice_od)

    def creer_liste_lieux(self, array):
        liste_lieux=[]
        for k in range(len(array)):
            liste_lieux.append(Lieu(array[k,0], array[k,1]))
        return liste_lieux


    def creer_liste_lieux_aleatoire(self,nb_lieux):
        self.liste_lieux=[]
        for i in range(nb_lieux):
            x = random.uniform(0, self.LARGEUR)
            y = random.uniform(0, self.HAUTEUR)
            point = Lieu(x,y)
            self.liste_lieux.append(point)
        return self.liste_lieux

    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((self.NB_LIEUX, self.NB_LIEUX))
        for i in range(self.NB_LIEUX):
            for j in range(self.NB_LIEUX):
                if i == j:
                    self.matrice_od[i,j] = np.inf
                if i != j:
                    self.matrice_od[i,j] = Lieu.distance(self.liste_lieux[i], self.liste_lieux[j])
        return self.matrice_od
    
    @classmethod
    def plus_proche_voisin(cls, lieu, matrice_od) :
        cls.le_plus_proche_voisin = np.argmin(matrice_od[lieu])
        return cls.le_plus_proche_voisin

    def sauvegarder_graph(self, path):
        self.df = pd.DataFrame([(lieu.x, lieu.y) for lieu in self.liste_lieux], columns =['x','y'])
        self.df.to_csv(path, index=False)
    
    @classmethod
    def charger_graph(cls, path):
        return pd.read_csv(path).values


class Route:
    
    @classmethod
    def def_ordre(cls, nb_lieux):
        cls.ordre = [0]
        tmp = list(range(1,nb_lieux))
        random.shuffle(tmp)
        cls.ordre.extend(tmp)
        cls.ordre.append(0)
        return cls.ordre

    @classmethod
    def calcul_distance_route(cls, ordre, matrice_od) :
        cls.distance = 0
        for i in range(len(ordre)-1):
            cls.distance += matrice_od[ordre[i],ordre[i+1]]
        return cls.distance


def generer(name, l, h, np):

    graphe = Graph(l, h, np)

    print("liste des lieux à visiter :")
    print([(lieu.x, lieu.y) for lieu in graphe.liste_lieux])
    print("matrice des distances :")
    print(graphe.matrice_od)

    print("*"*65)

    print("nombre de lieux :", graphe.NB_LIEUX, "__ ordre de visite aléatoire :", graphe.ordre_aleatoire)

    print("distance totale :", graphe.distance)

    graphe.sauvegarder_graph(f"{name}.csv")


#generer("points", 10, 10, 5)





# if __name__ == "__main__":
#     import sys
#     generer(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))


# """pour appeler la fonction "generer" via l'invite de commande : 
#     $ python tsp_graph_init.py name l w np

#     Args:
#         name (str): nom du fichier csv qui sera généré
#         l (int): largeur de l'espace 
#         h (int): hauteur de l'espace
#         np (int): nombre de points
# """

