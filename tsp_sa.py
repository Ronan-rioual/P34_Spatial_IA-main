from tsp_graph_init import Graph, Route
import numpy as np
import random
import time
import pandas as pd

random.seed(1)
np.random.seed(1)

class TSP_SA:

    def __init__(self, largeur, hauteur, liste_lieux=False, nb_lieux=10):

        #self.N = len(liste_lieux)


        self.graphe = Graph(largeur, hauteur, liste_lieux, nb_lieux)
        self.chemin_zero = self.heuristique()
        self.N = len(self.chemin_zero)-1
        #self.chemin_zero = list(range(nb_lieux))
        #random.shuffle(self.chemin_zero)
        self.distance_zero = Route.calcul_distance_route(self.chemin_zero, self.graphe.matrice_od)
        # b=time.time()
        # self.chemin_SA = self.two_opt(self.chemin_zero)
        # self.distance_SA = Route.calcul_distance_route(self.chemin_SA, self.graphe.matrice_od)
        # self.time_SA = time.time()-b 

        # self.chemin_SA = self.SA_two_opt(self.chemin_zero)
        # self.distance_SA = Route.calcul_distance_route(self.chemin_SA, self.graphe.matrice_od)
        # self.time_SA = time.time()-b      
        self.T0 = 0.50
        self.Tf = 0.25
        self.tau = 500
        self.kmax = min(self.N*10, 4_000)

    def heuristique(self):
        local_matrix = self.graphe.matrice_od.copy()
        points_a_explorer = list(range(1,self.graphe.NB_LIEUX))
        route_courte = [0]
        while points_a_explorer:
            last_point = route_courte[-1]
            plus_proche = self.graphe.plus_proche_voisin(last_point, local_matrix)
            local_matrix[:,last_point]= np.inf
            route_courte.append(plus_proche)
            points_a_explorer.remove(plus_proche)
        route_courte.append(0)

        return route_courte

    def two_opt(self, trajet):
        best = trajet.copy()
        trajet1 = trajet.copy()
        cheapest = Route.calcul_distance_route(best, self.graphe.matrice_od)
        better = True
        print("BEST", best, "- CHEAPEST", cheapest)
        print("Running 2opt")
        while better :
            better = False
            for i in range(1, len(trajet1)-2) :
                for j in range(i+1, len(trajet1)) :
                    if j-i == 1: 
                        continue
                    trajet2 = trajet1[:]
                    trajet2[i:j] = trajet1[j-1:i-1:-1]
                    #print("NEW ORDER TRY", trajet2)
                    #print("THIS COSTS", Route.calcul_distance_route(trajet2, self.graphe.matrice_od))
                    if Route.calcul_distance_route(trajet2, self.graphe.matrice_od) < cheapest:
                        best = trajet2
                        cheapest = Route.calcul_distance_route(best, self.graphe.matrice_od)
                        better = True
                        print("ORDER ACCEPTED")
                        print("NEW BEST ORDER :", trajet2)
                        print("THIS COSTS", Route.calcul_distance_route(trajet2, self.graphe.matrice_od))
            trajet1 = best
            yield best, trajet2, cheapest
        return best

    def SA_two_opt(self, trajet):
        best = trajet.copy()
        trajet1 = trajet.copy()
        cheapest = Route.calcul_distance_route(best, self.graphe.matrice_od)
        print("BEST", best, "- CHEAPEST", cheapest)
        T = self.T0
        k=0
        q=0
        while T>self.Tf and k<self.kmax:
            for i in range(1, len(trajet1)-2) :
                for j in range(i+1, len(trajet1)) :
                    if j-i == 1: 
                        continue
                    trajet2 = trajet1[:]
                    trajet2[i:j] = trajet1[j-1:i-1:-1]
                    cost2 = Route.calcul_distance_route(trajet2, self.graphe.matrice_od)
                    if cost2 < cheapest:
                        best = trajet1 = trajet2
                        cheapest = cost1 = cost2
                        print("ACCEPTED")
                        print("NEW BEST ORDER n°", q)
                        print("THIS COSTS", cost2)
                        q+=1
                    else :
                        a = np.random.uniform()
                        if a > np.exp(-0.5*T):
                            trajet1 = trajet2[:]
                            cost1 = cost2
            k+=1
            T = T*np.exp(-T/self.tau)           
            trajet1 = best
            print(k, "k", np.round(T,2), "°     THIS COSTS", cost2)
        return best

    def permutation(self, i, j, trajet):
        self.route = trajet[:]
        mini = min(i,j)
        maxi = max(i,j)
        self.route[mini:maxi] = self.route[mini:maxi].copy()[::-1]
        return self.route

    def recuit_simule(self):
        #initialisation des variables
        T = self.T0
        best = self.chemin_zero.copy()
        cheapest = self.distance_zero
        trajet1 = self.chemin_zero.copy()
        cost1 = self.distance_zero
        k=0
        while T>self.Tf and k<self.kmax:
            i = random.randint(1,self.N)
            j = random.randint(1,self.N)
            if j-i == 1: 
                continue
            trajet2 = self.permutation(i, j, trajet1)
            cost2 = Route.calcul_distance_route(trajet2, self.graphe.matrice_od)
            print("NEW ORDER TRY", trajet2, "    THIS COSTS", cost2)
            if cost2 < cheapest:
                best = trajet2[:]
                trajet1 = trajet2[:]
                cheapest = cost1 = cost2
                print("    BEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                x=input("continue?")
            else :
                if cost2 < cost1:
                    trajet1 = trajet2[:]
                    cost1 = cost2
                    #print("    ACCEPTED - better but not best")
                else :
                    a = np.random.uniform()
                    if a > np.exp(-0.5*T):
                        trajet1 = trajet2[:]
                        cost1 = cost2
                    #     print("    ACCEPTED but worst", np.round(a,3), ">" , np.round(np.exp(-0.5*T),3))
                    # else :
                    #     print("    REJECTED", np.round(a,3), "<" , np.round(np.exp(-0.5*T),3))
            k+=1
            T = T*np.exp(-T/self.tau)
            
            print(k, "k  ", np.round(T,2), "°")
            print("-  "*35)
        return best




# def test(l, h, npoints):
#     a=time.time()
#     algo = TSP_SA(l, h, npoints)
    
#     print("**route de départ**\t", algo.chemin_zero)
#     print("**distance zéro**", algo.distance_zero)
#     print("**route 2opt**\t\t", algo.chemin_2opt)
#     print("**distance 2opt**", algo.distance_2opt)
#     print("**temps de calcul 2opt**", np.round(algo.time_2opt), "s")
#     print("**route SA**\t\t", algo.chemin_SA)
#     print("**distance SA**", algo.distance_SA)
#     print("**temps de calcul SA**", np.round(algo.time_SA,2), "s")


