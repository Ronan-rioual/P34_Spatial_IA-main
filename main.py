from tsp_graph_init import Graph
import numpy as np
import random
from affichage import Affichage

random.seed(1)
np.random.seed(1)

LARGEUR = 800
HAUTEUR = 600

mat_lieux = Graph.charger_graph("graph_5.csv")

app=Affichage(LARGEUR, HAUTEUR, array_lieux=mat_lieux, nb_lieux=5)
"""
Args:
    l (int): largeur de l'espace
    h (int): hauteur de l'espace
    array_lieux (array or bool): Matrice des points à calculer. Si la valeur de 'array_lieu' est initialisée à 'False'\
        le programme générera automatiquement une liste de lieux à partir du nombre de lieux spécifié pour 'nb_lieux'
    nb_lieux (int, optional): Nombre de lieux à utiliser pour la génération de lieux aléatoires si `array_lieux` = `False`.\
        Defaults to 25.
"""
app.mainloop()
