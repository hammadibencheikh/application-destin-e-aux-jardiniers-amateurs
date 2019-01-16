
from tkinter import*
import tkinter.filedialog 
import tkinter.messagebox
import os
from PIL import Image, ImageTk
import shutil
from datetime import datetime
from decimal import Decimal


class Species(object):
    "Création de la page de l'espèce sélectionnée"

    def __init__(self, key, tuple_species, file_varietes, file_notes, type_, type_2):
        "Méthode constructeur"
        
        
        self.directory = os.getcwd()
        self.key = key # Clé de dictionnaire
        self.tuple_species = tuple_species
        self.file_varietes = file_varietes
        self.file_notes = file_notes
        self.type_ = type_
        self.type_2 = type_2
        
        # Variables gérant le nombre de fois ou une fenêtre d'information s'affiche:
        
        self.only_once = 0
        self.only_1 = 0
        self.just_one = 0

    def species(self):
        "Création de la page de l'espèce sélectionnée"
        
        self.main_window = Tk()
        self.main_window.title("{}".format(self.type_2).capitalize())
        self.main_window.resizable(True, True)
        self.first_frame = Frame(self.main_window, bg= 'white',\
                          relief = 'ridge', bd = 0)
        self.first_frame.pack(expand = True, fill = BOTH) 
        self.main_frame = Frame(self.first_frame, bg= 'white',\
                          relief = 'ridge', bd = 1, padx = 10, pady = 10) 
        self.main_frame.pack(expand = True)
        
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = "green"
        
        # Importation et traitement des images:
        
        icones = ["/images/enregistrer.png", "/images/corbeille.png"]
        icones_open = [Image.open(self.directory + i) for i in icones]
        icones_size = (64, 64)
        icones_size2 = (32, 32)  
        [i.thumbnail(icones_size) for i in icones_open]
        self.photos_icones = [ImageTk.PhotoImage(i, master = self.main_window) for i in icones_open]

        label_donnees = LabelFrame(self.main_frame, bd = 0, bg = "white",\
                             highlightthickness = 0)
        label_donnees.grid(row = 0, column = 3, sticky = 'n')
        icones_open[1].thumbnail(icones_size2)
        self.trash_icon = ImageTk.PhotoImage(icones_open[1], master = self.main_window)
        trash = Button(label_donnees, bg ='white', bd = 1, image = self.trash_icon,\
                command = self.info_destroy_file)
        trash.pack(side = LEFT, anchor = N)
        titre_donnees = Label(label_donnees, text = "Données enregistrées", bd = 0,\
                        bg = 'white', fg = self.read_color, relief = 'ridge', font = "Times 16 bold",\
                        highlightthickness = 0, padx = 40)
        titre_donnees.pack(side = LEFT, anchor = W, fill = BOTH)
        
        # Création du widget "Données enregistrées" (pour chaque variété de l'espèce sélectionnée):

        self.editeur_scroll = Scrollbar(self.main_frame, bg = self.read_color, relief='ridge', width=18,\
                              orient = 'vertical', cursor ='hand2', troughcolor = 'white',\
                              activebackground = self.read_color)
        self.editeur_scroll.grid(row = 0, column = 4, rowspan = 2, sticky = 'ns')
        self.editeur = Text(self.main_frame, height = 24, width = 52, bg = 'white',\
                       highlightbackground = "grey", bd = 2, font = 'Times 16', padx = 11,\
                       pady = 8, wrap = 'word', yscrollcommand =  self.editeur_scroll.set)
        self.editeur.grid(row = 0, column = 3, rowspan = 2,padx = 2, pady = 5, sticky = 's')
        self.editeur_scroll.config(command = self.editeur.yview)
        
        # Création du widget "Bloc-notes":
        
        self.notes_scroll = Scrollbar(self.main_frame, bg = self.read_color, relief = 'ridge',\
                            width = 18,  orient = 'vertical', cursor = 'hand2',\
                            troughcolor = 'white', activebackground = self.read_color)
        self.notes_scroll.grid(row = 1,column = 2, sticky = 'nsw', pady = 10)
        self.notes = Text(self.main_frame, height = 8, width = 39, bg='white',\
                     highlightbackground = "grey", bd = 2, relief = 'flat', font='Times 16',\
                     padx=11, pady=8, wrap='word', yscrollcommand =  self.notes_scroll.set)
        self.notes.grid(row = 1, column = 0, columnspan = 2, pady = 10, sticky = 'nsew')
        self.notes_scroll.config(command = self.notes.yview)
        self.notes.insert(1.0, "Bloc-notes\n")
        self.notes.tag_add('titel', '1.0', '1.20')
        self.notes.tag_config('titel', foreground = self.read_color, justify='center', underline = 1,\
                             font='Times 16 bold')
        
        # Affichage du bloc-notes de la variété de l'espèce sélectionnée:
        
        file_ = open(self.file_notes, 'a')
        file_.close()
        with open(self.file_notes, 'r') as file_ :
            readfile = file_.readlines()
        [self.notes.insert('end', i) for i in readfile]
        
        # Import de l'image illustrant le bouton d'enregistrement du widget notes:
        
        icones_open[0].thumbnail(icones_size2)
        self.save_icon = ImageTk.PhotoImage(icones_open[0], master = self.main_window)
        self.save_button = Button(self.main_frame, bg ='white', bd = 1,\
                           image = self.save_icon, command = self.save_notes)
        self.save_button.grid(row = 1, column = 0, rowspan = 2, padx = 5,\
                             pady = 15, sticky = 'nw')
        
        self.method_widgets(self.tuple_species[0])
        
        
    def method_widgets(self, image_species = None):
        "Création de la fenêtre contenant les champs d'entrée"

        for child in self.main_frame.winfo_children():
            if child.winfo_class() == "Canvas":
                child.destroy()
        self.image_species = image_species
        try:
            image_open = Image.open(self.directory + self.image_species)
        except:
            image_open = Image.open(self.directory + "/images/default_image.png")
            with open("images_{}".format(self.type_), 'r') as file_:
                readfile = file_.readlines()
                for i in range(0, len(readfile)):
                    if self.image_species == readfile[i].strip():
                        readfile[i] = "/images/default_image.png\n"
            with open("images_{}".format(self.type_), 'w') as file_: 
                for i in readfile:
                    file_.write(i)

        # Traitement de l'image illustrant le légume:
        
        image_size = (96, 96)
        image_open.thumbnail(image_size)
        self.photo_legume = ImageTk.PhotoImage(image_open, master = self.main_window)

        # Création de la fenêtre contenant les champs d'entrée:

        self.widgets = Canvas(self.main_frame, height = 500, width = 800, bg = 'white',\
                       bd = 2, relief = 'ridge', highlightthickness = 0)
        self.widgets.grid(row = 0, column = 0, columnspan = 3, sticky = 'ns', pady = 3)
        self.picture_button = Button(self.widgets, bg = 'white', bd = 0, width = 96, height = 96,\
                              image = self.photo_legume, command = self.agrandir_remplacer)
        self.picture_button.grid(row = 0, column = 0, padx = 5, pady = 10)
        
        self.titre = Label(self.widgets, text = self.tuple_species[1], bg = 'white', fg = "black",\
                     font = 'Times 20 bold', padx = 5, pady = 5)
        self.titre.grid(row = 0,column = 1, columnspan = 2, sticky = 'n', padx = 5, pady = 5)
        self.espece = Label(self.widgets, text = 'Variétés :', font = 'Times 16', bg = 'white')
        self.espece.grid(row = 1, column = 0, sticky = 'ne', padx = 5, pady = 5)
        self.listbox_varietes()


    def listbox_varietes(self) :
        "Création de la Listbox affichant les variétés de l'espèce"
        
        for child in self.widgets.winfo_children():
            if child.winfo_class() == "Listbox":
                child.destroy()
        varietes = []
        file_ = open(self.file_varietes, 'a')
        file_.close()
        with open(self.file_varietes,'r') as file_:
            readfile = file_.readlines()
            for i in readfile:
                varietes.append(i.replace("\n", ""))
        
        listspecies = StringVar() 
        list_scroll = Scrollbar(self.widgets, bg = self.read_color, relief='ridge', width= 14,\
                      orient='vertical', cursor='hand2', troughcolor = 'white',\
                      activebackground = self.read_color)
        list_scroll.grid(row = 1, column = 2, sticky='nsw', pady = 6)
        
        self.liste = Listbox(self.widgets, listvariable = listspecies, activestyle = 'dotbox',\
                     bd = 1, bg = 'white', font = 'Times 16', selectmode = 'browse', width = 20,\
                     height = 5, selectbackground = self.read_color, selectforeground = 'white',\
                     selectborderwidth = 1, yscrollcommand = list_scroll.set)
        self.liste.grid(row = 1, column = 1, sticky = 'nsew', pady = 5)
        list_scroll.config(command = self.liste.yview)

        liste_species = []
        liste_species.append(" Rajouter une variété")
        liste_species.append(" Supprimer une variété")
        for i in varietes:
            liste_species.append(i)

        for i, element in enumerate(liste_species) :
            self.liste.insert(i, element)
            self.liste.bind('<Return>', self.choice)
            listspecies.set(liste_species)
            listspecies.get()
        self.liste.itemconfig(liste_species.index(" Rajouter une variété"),\
                              selectbackground = "green", selectforeground = "white",\
                              foreground = "green")
        self.liste.itemconfig(liste_species.index(" Supprimer une variété"),\
                              selectbackground = "red", selectforeground = "white",\
                              foreground = "red")

        # Création des entrées :

        self.date_weight = LabelFrame(self.widgets, bg = 'white')
        self.date_weight.grid(row = 2, column = 0, columnspan = 3, padx = 30, pady = 10)

        self.date = Label(self.date_weight, text = 'Date de récolte :',\
                    font = 'Times 16', bg = 'white')
        self.date.grid(row = 0, column = 0, sticky = 'e', padx = 5, pady = 5)
        
        self.entree_date = Entry(self.date_weight, width = 15, font = 'Times 16',\
                           bd = 2, bg = '#EFEFEF', relief = 'ridge', state = 'disabled',\
                           takefocus = 0)
        self.entree_date.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 5)

        self.weight = Label(self.date_weight, text = 'Poids (en Kg) :',\
                      font = 'Times 16', bg = 'white')
        self.weight.grid(row = 1, column = 0, sticky = 'e', padx = 5, pady = 5)
        
        self.entry_weight = Entry(self.date_weight, width = 15, font = 'Times 16',\
                            state = 'disabled', bd = 2, bg = '#EFEFEF', relief = 'ridge',\
                            takefocus = 0)
        self.entry_weight.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5) 

        self.total_weight = Label(self.date_weight, text = 'Total (en Kg) :',\
                            font = 'Times 16', bg = 'white')
        self.total_weight.grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 5)
        
        self.entry_weight_total = Entry(self.date_weight, width = 15, font = 'Times 16',\
                                  state = 'disabled', bd = 2, bg = '#EFEFEF',\
                                  relief = 'ridge', takefocus = 0)
        self.entry_weight_total.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5) 
        
        self.liste.bind('<Enter>', self.message_liste)
        
    def message_liste(self, event):
        "Fait apparaitre une fenêtre de dialogue une seule fois"
    
        if self.only_1 == 0:
            tkinter.messagebox.showinfo("Votre sélection",\
            'Choisissez une variété dans le menu et pressez la touche "Entrée".\n\
Si la liste est vide, enregistrez une variété avec l\'option "Rajouter une variété".', parent = self.main_window)
            self.only_1 += 1

    def choice(self, event = None):
        """Méthode qui sélectionne une variété ou qui ouvre une fenêtre 
           Toplevel pour ajouter ou supprimer une variété"""

        self.chosen = self.liste.curselection()

        if self.chosen == (0,):
            self.rajout = Toplevel(bg = 'green')
            self.rajout_label = Label(self.rajout, bg = 'green', fg = 'white', text = "Entrez le nom de la variété à rajouter.",\
                                      font = "Times 14 bold", pady = 5) 
            self.rajout_label.grid(row = 0, padx = 10)
            self.champ_rajout = Entry(self.rajout, width = 30, font = "Times 14")
            self.champ_rajout.grid(row = 1, padx = 10, pady = 10)
            self.champ_rajout.bind('<Return>', self.save_new_variety)

        elif self.chosen == (1,):
            self.suppression = Toplevel(bg = 'red')
            self.suppression_label = Label(self.suppression, bg = 'red', fg = 'white', text = "Entrez le nom de la variété à supprimer.",\
                                      font = "Times 14 bold", pady = 5) 
            self.suppression_label.grid(row = 0, padx = 10)
            self.champ_suppression = Entry(self.suppression, width = 30, font = "Times 14")
            self.champ_suppression.grid(row = 1, padx = 10, pady = 10)
            self.champ_suppression.bind('<Return>', self.suppress_variety)

        elif self.chosen != (0,) and self.chosen != (1,) : 
            self.editeur.delete(1.0, 'end')
            self.affichage()


    def affichage(self, event = None) :
        "Affichage des données de la variété sélectionnée"

        if self.just_one == 0:
            tkinter.messagebox.showinfo('Confirmation',\
            'La confirmation de chaque champ d\'entrée (date, poids) s\'exécute en pressant la touche "Entrée"',\
            parent = self.main_window)
            self.just_one += 1
        with open(self.file_varietes, 'r') as file_:
            readfile = file_.readlines()
        for i in range(0, len(readfile)) :
            if self.chosen == (i + 2,) :
                self.entree_date.focus_set()
                self.entree_date.delete(0, 15)
                self.entree_date.config(bg = 'white', fg = 'black')
                self.entry_weight_total.delete(0, 15)
                today = datetime.now()
                self.jour_actuel = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                self.entree_date.config(state = 'normal')
                file_variete = open(self.file_varietes + "_" + str(i + 1), 'a')
                file_variete.close()
                with open(self.file_varietes + "_" + str(i + 1), 'r') as file_variete:
                    readfile_variete = file_variete.readlines()
                total_weight_variete = open(self.file_varietes + "_" + str(i + 1) + '_PT', 'a')
                total_weight_variete.close()
                with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'r') as total_weight_variete:
                    readfile_total_weight = total_weight_variete.readline()
                    self.entry_weight_total.configure(state = 'normal')
                    self.entry_weight_total.insert(0, readfile_total_weight)
                list_edit = []
                for i2 in range (len(readfile_variete), 0, -2):
                    self.edit = Label(self.editeur, width = 55, justify = 'left', bg = '#EFEFEF',\
                                text = str(readfile_variete[i2-2]) + \
                                str(readfile_variete[i2-1]).strip(), highlightthickness = 2,\
                                highlightcolor = "red",  highlightbackground = self.read_color, \
                                font = "Times 14", anchor = 'w', padx = 10, pady = 10, takefocus = 1)
                    self.editeur.window_create('end', window=self.edit, padx=10, pady=10)
                    object_edit = Label_Bind(self.entry_weight_total, self.chosen, self.edit,\
                                  self.key, self.tuple_species, self.file_varietes, self.file_notes, self.type_, self.type_2)
                    list_edit.append(object_edit)
                for i3 in list_edit:
                    i3.label_bind()
                self.entree_date.insert(0, self.jour_actuel)
                self.entree_date.bind('<Return>', self.entree_poids)
                self.entry_weight.bind('<Button-1>', self.entree_poids)
                


    def entree_poids(self, event) :
        "Méthode qui déverouille le champ d'entrée du poids"
        
        self.editeur.delete(1.0, 'end')
        self.entry_weight.config(state='normal')
        self.tentative_date = self.entree_date.get()
        if len(self.tentative_date) < 7:
            self.signaleErreurDate()        
        else:
            try:
                verif2 = int(self.tentative_date[-4:len(self.tentative_date)])
            except:
                self.signaleErreurDate()
            else:
                self.entree_date.delete(0, 30)
                self.entree_date.insert(0, 'Enregistré')
                self.entry_weight.focus_set()
                while self.only_once < 1 :
                    self.entry_weight.configure(bg = 'green', fg='white')
                    self.entry_weight.insert(0, 'Exemple : 2.5')
                    self.widgets.after(1500, self.videEntreePoids)
                    self.only_once += 1
                self.entry_weight.bind('<Return>', self.date_poids_recolte)
                self.editeur.insert('end', "- " + self.tentative_date + "\n")
                self.entree_date.config(bg = "green", fg = "white")

    #---- Méthode ------------------------------------------------

    def date_poids_recolte(self, event):
        "Méthode qui enregistre la date et le poids récolté"
        
        tentative_poids = self.entry_weight.get()
        try:
            tentative_poids = str(round(Decimal(tentative_poids), 2))
        except:
            self.signaleErreurPoids()
        else:
            self.editeur.insert('end', '- ' + str(tentative_poids) + ' Kg\n')
            self.entry_weight.delete(0, 30)
            self.entry_weight.configure(bg = 'green', fg = 'white')
            self.entry_weight.insert(0, 'Enregistré')
            self.widgets.after(1000, self.videEntreePoids)
            self.entree_date.delete(0, 30)
            self.entree_date.config(bg = 'white', fg = 'black')
            self.entree_date.insert(0, self.jour_actuel)
            self.liste.focus_force()
            self.choice()
            with open(self.file_varietes, 'r') as file_:
                readfile = file_.readlines()
            for i in range(0, len(readfile)) :
                if self.chosen == (i + 2,) :
                    with open(self.file_varietes + "_" + str(i + 1), 'a') as file_variete:
                        file_variete.write("- Date de récolte: " + self.tentative_date + "\n")
                        file_variete.write('- Poids (en Kg): ' + str(tentative_poids) + '\n')
                    total_weight_variete = open(self.file_varietes + "_" + str(i + 1) + '_PT', 'a')
                    total_weight_variete.close()
                    with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'r') as total_weight_variete:
                        readfile_total_weight = total_weight_variete.readline()
                        if readfile_total_weight == '':
                            readfile_total_weight = 0
                        with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'w') as total_weight_variete:
                            total_weight_variete.write(str(Decimal(readfile_total_weight) + Decimal(tentative_poids)))
                        with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'r') as total_weight_variete:
                            readfile_total_weight = total_weight_variete.readline()
                            self.entry_weight_total.delete(0, 15)
                            self.entry_weight_total.configure(state = 'normal')
                            self.entry_weight_total.insert(0, readfile_total_weight)
                    with open(self.file_varietes + "_" + str(i + 1), 'r') as file_variete:
                        readfile_variete = file_variete.readlines() 
                    self.editeur.delete(1.0, 'end')
                    list_edit = []
                    for i2 in range (len(readfile_variete), 0, -2):
                        self.edit = Label(self.editeur, width = 55, justify = 'left', bg = '#EFEFEF', 
                                    text = str(readfile_variete[i2-2]) + str(readfile_variete[i2-1]).strip(),\
                                    highlightthickness = 2, highlightcolor = "red", highlightbackground = self.read_color,\
                                    font = "Times 14", anchor = 'w', padx = 10, pady = 10)
                        self.editeur.window_create('end', window=self.edit, padx=10, pady=10)
                        object_edit = Label_Bind(self.entry_weight_total, self.chosen, self.edit, self.key,\
                                      self.tuple_species, self.file_varietes, self.file_notes, self.type_, self.type_2)
                        list_edit.append(object_edit)
                    for i3 in list_edit:
                        i3.label_bind()


    def save_new_variety(self, event):
        "Enregistrement d'une nouvelle variété"
        
        new_variety = self.champ_rajout.get()
        self.rajout.destroy()
        with open(self.file_varietes, 'a') as file_:
            file_.write(" " + new_variety.capitalize() + "\n")
        with open(self.file_varietes, 'r') as file_ :
            readfile = file_.readlines()
        file_variete = open(self.file_varietes + "_" + str(len(readfile)), 'a')
        file_variete.close()
        total_weight_variete = open(self.file_varietes + "_" + str(len(readfile)) + '_PT', 'a')
        total_weight_variete.write('0')
        total_weight_variete.close()
        self.listbox_varietes()


    def suppress_variety(self, event): 
        "Suppression d'une variété"
        
        self.confirmation_suppression = tkinter.messagebox.askokcancel("Supprimer?", "Voulez-vous vraiment supprimer cette variété?\nCette opération est irréversible et détruira toutes les données enregistrées.")
        if self.confirmation_suppression == True:
            old_variety = self.champ_suppression.get().lower()
            self.suppression.destroy()
            with open(self.file_varietes, 'r') as file_:
                readfile = file_.readlines()
            for i in range(0, len(readfile)) :
                print(old_variety, readfile[i].strip())
                if old_variety == readfile[i].strip().lower() :
                    try:
                        os.remove(self.directory + "/" + self.file_varietes + "_" + str(i + 1))
                    except:
                        file_variete = open(self.file_varietes + "_" + str(i + 1), 'a')
                    try:
                       os.remove(self.directory + "/" + self.file_varietes + "_" + str(i + 1) + '_PT')
                    except:
                        total_weight_variete = open(self.file_varietes + "_" + str(i + 1) + '_PT', 'a')
            for i in readfile:
                if " " + old_variety.capitalize() + "\n" == i:
                    readfile.remove(i) 
            with open(self.file_varietes, 'w') as file_:
                for i in readfile:
                    file_.write(i) 
            self.listbox_varietes()


    def agrandir_remplacer(self):
        "Agrandir ou pivoter la photo?"
        
        image_resize = "/images/resize.png"
        image4 = Image.open(self.directory + image_resize)
        image4_size = 96, 96
        image4.thumbnail(image4_size)
        self.photo_resize = ImageTk.PhotoImage(image4)

        image_replace = "/images/default_image.png"
        image5 = Image.open(self.directory + image_replace)
        image5_size = 96, 96
        image5.thumbnail(image5_size)
        self.photo_rotate = ImageTk.PhotoImage(image5)
        
        self.choix = Toplevel(name = 'selected', bg  = 'white')
        self.label_agrandir_remplacer = Label(self.choix, bg = 'white', fg = 'black',\
                                       text = "Voulez-vous agrandir\nou remplacer la photo?",\
                                       font = ('Times', '14', 'bold'))
        self.label_agrandir_remplacer.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)
        self.agrandissement = Button(self.choix, image = self.photo_resize, bg = 'black', bd = 2,\
                              highlightthickness = 1, command = self.photo_agrandie)
        self.agrandissement.grid(row = 1, column = 0, sticky = 'w', padx = 10, pady = 10)
        self.replace_image = Button(self.choix, image = self.photo_rotate, bg = 'black', bd = 2,\
                             highlightthickness = 1, command = self.replace_photo)
        self.replace_image.grid(row = 1, column = 1, sticky = 'w', padx = 10, pady = 10)


    def photo_agrandie(self) :
        "Méthode permettant d'agrandir les photos"
        
        self.grande_photo = Toplevel(name = 'selected')
        image_open2 = Image.open(self.directory + self.image_species)
        if image_open2.size[0] > 768 and image_open2.size[1] > 768:
            image_species_size = 1024, 1024
            image_open2.thumbnail(image_species_size)
        self.great_picture = ImageTk.PhotoImage(image_open2)
        label_photo = Label(self.grande_photo, image = self.great_picture)
        label_photo.grid()


    def replace_photo(self):
        "Remplacement de photos"
        
        self.choose_picture = tkinter.filedialog.askopenfilename(title="Importer une image",\
                              filetypes=[('png files','.png'),('all files','.*')])
        try:
            shutil.copy(self.choose_picture, "images/images_{}".format(self.type_))
        except:
            pass
        else:
            image_to_remove = ''
            with open("images_legumes", 'r') as file_images:
                readfile_images = file_images.readlines()
                base_name = os.path.basename(self.choose_picture)
                for i, element in enumerate (readfile_images):
                    if readfile_images[i] == self.image_species + "\n" and i == self.key:
                        image_to_remove = self.image_species + "\n"
                        readfile_images[i] = "/images/images_{}/".format(self.type_) + base_name + "\n"
            if image_to_remove != "/images/default_image.png\n" and image_to_remove not in readfile_images:
                os.remove(self.directory + image_to_remove.strip())
            with open("images_{}".format(self.type_), 'w') as file_images:
                for i in readfile_images:
                    file_images.write(i)
            self.choix.destroy()
            self.tuple_species = list(self.tuple_species) 
            self.tuple_species[0] = "/images/images_{}/".format(self.type_) + base_name
            self.tuple_species = tuple(self.tuple_species)
            self.method_widgets(image_species = "/images/images_{}/".format(self.type_) + base_name)


    def save_notes(self):
        "Enregistrement des notes"
        
        new_notes = self.notes.get(2.0, 'end')
        with open(self.file_notes, 'w') as file_ :
            file_.write(new_notes)
            tkinter.messagebox.showinfo('Mise à jour',\
            'Votre bloc-notes a été mis à jour')


    def info_destroy_file(self):
        "Information sur la suppression d'une entrée"
        
        if self.chosen != () and self.chosen != (0,) and self.chosen != (1,):
            self.warning = tkinter.messagebox.showinfo('Supprimer une entrée',\
            "Cliquez sur l'entrée que vous souhaitez supprimer et confirmez la suppression.")
            

# METHODES DE GESTION DES ERREURS 

    def signaleErreurDate(self):
        "Format de date incorrecte"
        
        self.entree_date.configure(bg ='red', fg='white')
        self.entree_date.delete(0,15)
        self.entree_date.insert(0, 'Format invalide')
        self.widgets.after(1000, self.videEntreeDate) 
        
        
    def videEntreeDate(self):
        "Vide le champ d'entrée de la date"
        
        self.entree_date.configure(bg ='white', fg='black')
        self.entree_date.delete(0, 15)


    def signaleErreurPoids(self):
        "Format de poids incorrect"
        
        self.entry_weight.configure(bg ='red', fg='white')
        self.entry_weight.delete(0,15)
        self.entry_weight.insert(0, 'Format invalide')
        self.widgets.after(1000, self.videEntreePoids)


    def videEntreePoids(self):
        "Vide le champ d'entrée du poids"

        self.entry_weight.configure(bg ='white', fg='black')
        self.entry_weight.delete(0, 15)


    def videEntreeRajout(self):
        "Vide le champ d'entrée pour ajouter une variété"
        
        self.champ_rajout.configure(bg = 'white', fg = 'black')
        self.champ_rajout.delete(0, 45)
        self.champ_rajout.focus_set()


    def videEntreeSuppression(self):
        "Vide le champ d'entrée pour supprimer une espèce"

        self.champ_suppression.configure(bg = 'white', fg = 'black')
        self.champ_suppression.focus_set()
        self.champ_suppression.delete(0, 45)
        
class Label_Bind(Species):
    """Opérations sur les widgets Label qui instancient 
       les entrées d'une espèce avec la date et le poids de la récolte"""

    def __init__(self, entry_weight_total,chosen, edit, key, tuple_species, file_varietes, file_notes, type_, type_2):
        "Constructeur"
        
        Species.__init__(self, key, tuple_species, file_varietes, file_notes, type_, type_2)
        self.entry_weight_total = entry_weight_total
        self.chosen = chosen
        self.edit = edit

        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = "green"
        

    def label_bind(self):
        "binds"
    
        self.edit.bind('<Enter>', lambda event: self.select_label(self.edit))
        self.edit.bind('<Leave>', lambda event: self.deselect_label(self.edit))
        
        
    def select_label(self, edit):
        "La ligne de focus passe en rouge"
    
        self.edit = edit
        self.edit.configure(highlightbackground = "red")
        self.edit.bind('<Button-1>', lambda event: self.destroy_file(self.edit))
    
    
    def deselect_label(self, edit):
        "La ligne de focus repasse au vert"
    
        self.edit = edit
        self.edit.configure(highlightbackground = self.read_color)


    def destroy_file(self, edit):
        "Méthode de destruction de l'entrée sélectionnée"
        self.edit = edit
        self.edit.unbind('<Button-1>')
        warning = tkinter.messagebox.askquestion('Supprimer une entrée', "Voulez-vous vraiment supprimer cette entrée?")
        if warning == 'yes':
            recup_text = self.edit['text']
            poids_a_retrancher = Decimal(recup_text[recup_text.index(":", 35) + 2:])
            recup_text = recup_text.split('\n')
            with open(self.file_varietes, 'r') as file_:
                readfile = file_.readlines()
            for i in range(0, len(readfile)) :
                if self.chosen == (i + 2,) :
                    with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'r') as total_weight_variete:
                        readfile_total_weight = total_weight_variete.readline()
                    with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'w') as total_weight_variete:
                        total_weight_variete.write(str(Decimal(readfile_total_weight) - poids_a_retrancher))
                    with open(self.file_varietes + "_" + str(i + 1) + '_PT', 'r') as total_weight_variete:
                        readfile_total_weight = total_weight_variete.readline()
                        self.entry_weight_total.delete(0, 15)
                        self.entry_weight_total.configure(state = 'normal')
                        self.entry_weight_total.insert(0, readfile_total_weight)
                    with open(self.file_varietes + "_" + str(i + 1), 'r') as file_variete:
                        readfile_variete = file_variete.readlines() 
                    #for i2 in recup_text:
                     #   i2 = i2 + '\n'
                      #  print(i2)
                    for i2 in range(0, len(recup_text)):
                        recup_text[i2] = recup_text[i2] + '\n'
                        if i2 % 2 == 0 :
                            for i3 in range(0, len(readfile_variete)):
                                if i3 % 2 == 0 :
                                   if recup_text[i2] + recup_text[i2 + 1] == readfile_variete[i3] + readfile_variete[i3 + 1].strip():
                                       readfile_variete[i3:i3 + 2] = []
                                       break
                    with open(self.file_varietes + "_" + str(i + 1), 'w') as file_variete:
                        for x in readfile_variete:
                            file_variete.write(x)
            self.edit.destroy()