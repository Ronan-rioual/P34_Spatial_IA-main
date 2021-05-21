from tsp_graph_init import Graph, Lieu
from tsp_sa import TSP_SA
import numpy as np
import random
import time
import pandas as pd
from affichage import Affichage

random.seed(1)
np.random.seed(1)

LARGEUR = 800
HAUTEUR = 600

# def test(l, h, array_lieux, nb_lieux=25):
#     """
#     Args:
#         l (int): largeur de l'espace
#         h (int): hauteur de l'espace
#         array_lieux (array or bool): Matrice des points à calculer. Si la valeur de 'array_lieu' est initialisée à 'False'\
#             le programme générera automatiquement une liste de lieux à partir du nombre de lieux spécifié pour 'nb_lieux'
#         nb_lieux (int, optional): Nombre de lieux à utiliser pour la génération de lieux aléatoires si `array_lieux` = `False`.\
#             Defaults to 25.
#     """

#     algo = TSP_SA(l, h, array_lieux,nb_lieux)
    
#     print("**route de départ**\t", algo.chemin_zero)
#     print("**distance zéro**", algo.distance_zero)
#     print("**route SA**\t\t", algo.chemin_SA)
#     print("**distance SA**", algo.distance_SA)
#     print("**temps de calcul **", np.round(algo.time_SA,3), "s")


mat_lieux = Graph.charger_graph("graph_10.csv")



def geomatique():

  app=Affichage(LARGEUR, HAUTEUR, array_lieux=False, nb_lieux=100)
  app.mainloop()


geomatique()