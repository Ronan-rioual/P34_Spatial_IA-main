
import tkinter as tk
from tsp_graph_init import *
from tsp_sa import TSP_SA


class Affichage(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1300x800")
        self.create_widget()
        self.v=tk.IntVar()


    def create_widget(self):
                
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        """Titre"""
        self.champ_titre=tk.Label(self,text="Géomatique",padx="10",pady="10")
        self.champ_titre.config(font=("Helvetica", 44), fg='#7be50a')
        self.champ_titre.pack(side="top")

        """Fenêtre principale"""
        self.appli=tk.Frame(self)
        self.appli.config(bg = '#cdcdcd')
        self.appli.pack(fill ="both", expand="yes")
        self.draw_graph(self.appli) #appel à la fonction draw_graph

#fonction qui dessine le graphe
    def draw_graph(self, canvas):  
        self.DIAM_CERCLE = 9
        self.NB_iteration = 100
        self.canvas = tk.Canvas(self.appli, width=800, height=700, bg = 'white')
        self.canvas.pack()

        self.TSP = TSP_SA(800, 600, 100) #instanciation de l'objet TSP_SA
        self.liste_lieux = self.TSP.graphe.liste_lieux  #appel de la fonction qui créer la liste des lieux

        #création d'un dictionnaire pour y ranger les lieux par numéro, avec leur coordonnées
        self.dico_lieux = {}
        for x in range(len(self.liste_lieux)):
            self.dico_lieux[x] = [self.liste_lieux[x].x, self.liste_lieux[x].y]

  
        #boucle for qui dessine les points et écrit le numéro à l'interieur
        for x in range(len(self.liste_lieux)):
            if x == 0:
                color = 'red'
            else:
                color = 'silver'
            self.canvas.create_oval((self.dico_lieux[x][0]-self.DIAM_CERCLE, self.dico_lieux[x][1]-self.DIAM_CERCLE), ((self.dico_lieux[x][0]+self.DIAM_CERCLE), (self.dico_lieux[x][1]+self.DIAM_CERCLE)), width = 1, fill = color, tags='points')
            self.canvas.create_text((self.dico_lieux[x][0], self.dico_lieux[x][1]),text=x, tags='text')


# # appel de la fonction qui trouve la première route
        self.premiere_route = self.TSP.heuristique()
        self.best_distance = self.TSP.distance_zero

        #traçage de la première route
        for x in self.premiere_route:
            try:
                self.canvas.create_line((self.dico_lieux[self.premiere_route[x]][0], self.dico_lieux[self.premiere_route[x]][1]), ((self.dico_lieux[self.premiere_route[x+1]][0]), (self.dico_lieux[self.premiere_route[x+1]][1])), width = 3, dash=(3), fill = 'red',tags='best')
            except KeyError:
                self.canvas.create_line((self.dico_lieux[x][0], self.dico_lieux[x][1]), ((self.dico_lieux[0][0]), (self.dico_lieux[0][1])), width = 3, dash=(3), fill = 'red',tags='best')
        canvas.update()
        #self.canvas.delete('route')


#appel de la fonction qui dessine les routes suivantes
        self.route_suivante = self.TSP.two_opt(self.premiere_route)

        while self.route_suivante:
            canvas.update()
            try:
                best, test, cheapest = next(self.route_suivante)
            except StopIteration:
                pass
            #print(self.route_suivante)
            #self.route_suivante = list(self.route_suivante)
            #result = next(itertools.islice(x, 1))

            if self.best_distance > cheapest:
                self.canvas.delete('best')
                for x in range(len(test)-1):
                    try:
                        self.canvas.create_line((self.dico_lieux[best[x]][0], self.dico_lieux[best[x]][1]), ((self.dico_lieux[best[x+1]][0]), (self.dico_lieux[best[x+1]][1])), width = 3, dash=(4,1), fill = 'blue', tags = 'best')
                    except KeyError:
                        self.canvas.create_line((self.dico_lieux[x][0], self.dico_lieux[x][1]), ((self.dico_lieux[0][0]), (self.dico_lieux[0][1])), width = 3, dash=(3), fill = 'blue',tags='best')          
            else:
                for x in range(len(test)-1):
                    print('coucou')
                    try:
                        self.canvas.create_line((self.dico_lieux[test[x]][0], self.dico_lieux[test[x]][1]), ((self.dico_lieux[test[x+1]][0]), (self.dico_lieux[test[x+1]][1])), width = 3, dash=(4,1), fill = 'grey',tags='route')
                    except KeyError:
                        self.canvas.create_line((self.dico_lieux[x][0], self.dico_lieux[x][1]), ((self.dico_lieux[0][0]), (self.dico_lieux[0][1])), width = 3, dash=(3), fill = 'grey',tags='route')   


            canvas.update()
            self.canvas.delete('route')
 
# appel de la fonction qui trouve la route optimale
        # self.meilleur_route = self.TSP.chemin_2opt

        # #traçage de la meilleur route
        # for x in self.meilleur_route:
        #     try:
        #         self.canvas.create_line((self.dico_lieux[self.meilleur_route[x]][0], self.dico_lieux[self.meilleur_route[x]][1]), ((self.dico_lieux[self.meilleur_route[x+1]][0]), (self.dico_lieux[self.meilleur_route[x+1]][1])), width = 3, dash=(4,1), fill = 'red',tags='route2')
        #     except KeyError:
        #         self.canvas.create_line((self.dico_lieux[x][0], self.dico_lieux[x][1]), ((self.dico_lieux[0][0]), (self.dico_lieux[0][1])), width = 3, dash=(3), fill = 'red',tags='route2') 
        # self.canvas.tag_raise('points') #je remet les points et le texte au premier plan
        # self.canvas.tag_raise('text')  

        # canvas.update()
   
        # affichage du texte en bas de la fenêtre TK
        self.affichage_distance = tk.Label(self.appli,text='distance : '+ str(self.TSP.distance_zero),padx="10",pady="10")
        self.affichage_distance.pack()


def geomatique():

  app=Affichage()
  app.mainloop()


geomatique()