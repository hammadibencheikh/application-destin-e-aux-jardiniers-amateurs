
import os
from tkinter import* 
from calendar import monthcalendar
from time import localtime 
from datetime import datetime 
from mon_jardin.agenda import Agenda 


class Calendrier(object) :
    "Classe instanciant le calendrier"

    def __init__(self, fenetre = None):
        "Constructeur"
        
        self.y = localtime()[0] 
        self.m = localtime()[1] 
        self.d = localtime()[2] 
        self.c = monthcalendar(self.y, self.m)
        self.w = datetime(self.y, self.m, self.d)
        self.w = self.w.isocalendar()[1]

        self.months =   ((1, 'Janvier'),
                        (2, 'Février'), 
                        (3, 'Mars'), 
                        (4, 'Avril'), 
                        (5, 'Mai'), 
                        (6, 'Juin'), 
                        (7, 'Juillet'), 
                        (8, 'Août'), 
                        (9, 'Septembre'), 
                        (10, 'Octobre'), 
                        (11, 'Novembre'), 
                        (12, 'Décembre'))

        self.days = ('S', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di')
        
        self.directory = os.getcwd()
        
        self.fenetre = fenetre
        if self.fenetre == None:
            self.fenetre = Tk()
        self.fenetre.title('Mon calendrier')
        self.mainframe = Frame(self.fenetre, bg='white')
        self.mainframe.grid()

    def calendrier(self) : 
        "Méthode de création du calendrier"
        
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = "green"
                
        # Création d'un widget Frame pour placer les widgets de la ligne 0:
        
        self.subframe = Frame(self.mainframe, bg = 'white')
        self.subframe.grid()

        # Création d'un widget Frame pour placer tous les widgets Button et les noms de chaque jour:
        
        self.subframe2 = Frame(self.mainframe, bg = 'white')
        self.subframe2.grid(row = 1)

        # Création du bouton en forme de triangle permettant d'afficher le mois précédent:
        
        self.left_triangle1 = Button(self.subframe, bg = 'white', fg = self.read_color, text = u"\u25C0",\
                              bd = 0, highlightthickness=0, padx = 0, pady = 0,\
                              activebackground = '#E4E4E4',\
                              command = self.prev_month)
        self.left_triangle1.grid(row = 0, column = 0, padx = 10, sticky='w')

        # Création du widget Label qui affiche le mois en cours:
         
        for i in range(0, len(self.months)) :
            for i2 in range(0, len(self.months[i])):
                if self.months[i][i2] == self.m :
                    self.month = Label(self.subframe,  bg = 'white', text = self.months[i][i2+1],\
                                 font = 'Times 14', padx = 10,pady = 10)
                    self.month.grid(row = 0, column = 1, columnspan = 2, sticky = 'w')

        # Création du bouton en forme de triangle permettant d'afficher le mois suivant:
        
        self.right_triangle1 = Button(self.subframe,  bg = 'white', fg = self.read_color, text = u"\u25B6",\
                               bd = 0,highlightthickness = 0, padx = 0, pady = 0,\
                               activebackground = '#E4E4E4', command = self.next_month)
        self.right_triangle1.grid(row = 0, column = 3, padx = 10, sticky = 'w')
    
        # Création du bouton en forme de triangle permettant d'afficher l'année précédente:
        
        self.left_triangle2 = Button(self.subframe,  bg = 'white', fg = self.read_color, text = u"\u25C0",\
                              bd = 0, highlightthickness = 0, padx = 0, pady = 0,\
                              activebackground = '#E4E4E4', command = self.prev_year)
        self.left_triangle2.grid(row = 0, column = 4, padx = 10, sticky = 'e')

        # Création du widget Label qui affiche l'année:
        
        self.year = Label(self.subframe,  bg = 'white', text = str(self.y),\
                    font = 'Times 14', padx = 10, pady = 10)
        self.year.grid(row = 0, column = 5, columnspan = 2, sticky = 'e')

        # Création du bouton en forme de triangle permettant d'afficher l'année suivante :
        
        self.right_triangle2 = Button(self.subframe,  bg = 'white', fg = self.read_color, text = u"\u25B6",\
                               bd = 0, highlightthickness = 0,             padx=0, pady=0,\
                               activebackground='#E4E4E4', command = self.next_year)
        self.right_triangle2.grid(row = 0, column = 7, padx = 10, sticky = 'e')

        # Création des widgets Label affichant les deux premières lettres de chaque jour de la semaine :
        
        for i in range(0, len(self.days)):
            self.day = Label(self.subframe2, bg = self.read_color, fg = 'white',\
                       text = self.days[i], padx = 10, pady = 10)
            self.day.grid(row = 0, column = i, sticky = 'nsew')


    def buttons(self) :
        "Création des boutons affichant chaque jour du mois"
        
        self.buttonlist = [] 
        self.row_numb = 1 # numéro de ligne
        self.col_numb = 1  
        for child in self.subframe2.winfo_children(): 
            if child.winfo_class() == 'Button':
                child.destroy()
        for i in range(0, len(self.c)) :
            self.sub_buttonlist = []
            for i2 in range(0, len(self.c[i])):
                if self.c[i][i2] == 0 : # Si le jour est absent , itération de la colonne.
                    self.col_numb +=1
                    if self.col_numb % 8 == 0 : # A la huitième colonne, itération de la ligne. 
                        self.row_numb += 1
                        self.col_numb = 1 # Nouvelle ligne : Le numéro de colonne repasse à 1. 
                else : # Création des jours proprement dits :
                    self.button = Button(self.subframe2, text = str(self.c[i][i2]), relief='flat', bd=1, bg='white', padx = 10, pady = 10) 
                    self.button.grid(row = self.row_numb, column = self.col_numb, sticky ='nsew')
                    self.sub_buttonlist.append(self.button)
                    self.sub_buttonlist.append(str(self.c[i][i2]))
                    self.buttonlist.append(self.sub_buttonlist)
                    self.sub_buttonlist = []
                    # Le bouton du jour courant est vert :
                    if self.c[i][i2] == localtime()[2] and self.m == localtime()[1] and self.y == localtime()[0] :
                        self.button.configure(bg=self.read_color, fg='white')
                        self.row_curweek = self.row_numb # Récupération de la rangée de la semaine en cours
                    self.col_numb += 1
                    if self.col_numb % 8 == 0 :
                        self.row_numb += 1
                        self.col_numb = 1
                    self.last_row = self.row_numb # Valeur de la dernière ligne
        # Appel de la méthode pages du module Agenda.    
        for i in range(0, len(self.buttonlist)):
             # Création de l'objet "agenda" et configuration de la commande de chaque bouton :
            self.d = int(self.buttonlist[i][0]['text'])
            self.agenda = Agenda(self.d, self.m, self.y)
            self.buttonlist[i][0]['command'] = self.agenda.pages

        #self.current_week()

#----------------------------------------------------------------------------------------------------------

    def current_week(self) :
        "Affichage des n° de semaines du mois en cours"
        i = self.row_curweek # Variables D'itération
        self.curweek = datetime(self.y, self.m, self.d)
        self.curweek = self.curweek.isocalendar()[1] # Retourne l'année et le n° de semaine en cours.
        while i >= 1 : # Création des boutons avec les n° de semaine --> direction passé
            self.week = Button(self.subframe2, bg=self.read_color,fg='white',text=str(self.curweek), padx=10, pady=10)
            self.week.grid(row = i, column = 0, sticky = 'nsew')
            self.curweek -= 1            
            i -= 1

        i = self.row_curweek + 1
        self.curweek = datetime(self.y, self.m, self.d)
        self.curweek = self.curweek.isocalendar()[1] + 1 # Réinitialisation de la variable.
        while i <= self.last_row : # Création des boutons avec les n° de semaine --> direction futur
            self.week = Button(self.subframe2, bg=self.read_color,fg='white',text=str(self.curweek), padx=10, pady=10)
            self.week.grid(row = i, column = 0, sticky = 'nsew')
            self.curweek += 1            
            i += 1

        self.fenetre.mainloop() # Démarrage du réceptionnaire d'événements

#----------------------------------------------------------------------------------------------------------

    def weeks(self) :
        "Affichage des n° de semaine du mois précédent ou du mois suivant" 
        self.row = 1
        for i in range(0, len(self.c)): # Boucle de 0 jusqu'au nombre de semaines dans le mois courant.
            i2 = 0
            while i2 < len(self.c[i]): # Boucle de 0 jusqu'au nombre de jours dans chaque semaine du mois.
                if self.c[i][i2] != 0  : 
                    self.curweek = datetime(self.y, self.m, self.c[i][i2])
                    break # Interruption de la boucle si la valeur est != 0
                i2 += 1
            self.curweek = self.curweek.isocalendar()[1] # Réinitialisation de la variable.
            # Création des nouveaux boutons de semaines :
            self.week = Button(self.subframe2, bg=self.read_color,fg='white',text=str(self.curweek), padx=10, pady=10)
            self.week.grid(row = self.row, column = 0, sticky = 'nsew')
            self.row +=1



#----------------------------------------------------------------------------------------------------------

    def prev_month(self) :
        "Affiche le mois précédent"
        
        if self.m == 1 :
            self.m = 12
            self.y -= 1
            self.month['text'] = self.months[11][1]
            self.c = monthcalendar(self.y, 12)
            self.year.configure(text = str(self.y))


        else :
            self.m-=1
            self.month['text'] = self.months[self.m-1][1]
            self.c = monthcalendar(self.y, self.m)
            
        self.buttons()
        self.weeks()

#----------------------------------------------------------------------------------------------------------

    def next_month(self) :
        "Affiche le mois suivant"
        if self.m == 12 :
            self.m = 1
            self.y += 1
            self.month['text'] = self.months[0][1]
            self.c = monthcalendar(self.y, self.m)
            self.year.configure(text = str(self.y))
            
        else :
            self.m += 1
            self.month['text'] = self.months[self.m-1][1]
            self.c = monthcalendar(self.y, self.m)
        self.buttons()
        self.weeks()

#----------------------------------------------------------------------------------------------------------

    def prev_year(self) :
        "Recul d'une année dans le passé" 
     
        for i in range(12):
            self.prev_month()

#----------------------------------------------------------------------------------------------------------

    def next_year(self) :
        "Projection d'une année dans le futur"
        for i in range(12):
            self.next_month()

    
#=========== MAIN PROGRAMM ================================================================================

if __name__ == "__main__":

    fenetre = Tk()

    calendrier = Calendrier(fenetre)
    calendrier.calendrier()
    calendrier.buttons()
    calendrier.current_week()
    
    fenetre.mainloop()