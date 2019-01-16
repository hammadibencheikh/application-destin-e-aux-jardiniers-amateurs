

import os
from tkinter import*
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import shutil


class Phototheque(object) :
    """Classe instanciant l'application "Photothèque" """


    def __init__(self):
        "Méthode constructeur"

        self.directory = os.getcwd()


    def home(self):
        "Page d'accueil"
        
                
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = 'green'

        self.window = Tk()
        self.window.title('Photothèque')
        self._frame = Frame(self.window, bg = 'white')
        self._frame.pack(expand = True, fill = BOTH)
        self.first_frame = Frame(self._frame, bg = 'white')
        self.first_frame.pack(expand = True)
        self.main_frame = Frame(self.first_frame, bg='white', relief = 'ridge', bd = 2)
        self.main_frame.grid()

        self.home = LabelFrame(self.main_frame, text=' MA PHOTOTHÈQUE ', labelanchor='n',\
                    font='Times 40 italic', bg='white', relief='ridge', bd=3, padx=20, pady=20)
        self.home.grid(row = 0, padx = 300, pady = 60)

        # Image de la page principale

        self.home_image = "/images/default_image.png" 
        self.image_home = Image.open(self.directory + self.home_image)
        self.image_home_size = 512, 512
        self.image_home.thumbnail(self.image_home_size)
        self.home_photo = ImageTk.PhotoImage(self.image_home, master = self.window)
    
        self.titre = Button(self.home, image=self.home_photo, bg = self.read_color, relief = 'ridge',\
                     bd=2, padx = 40, cursor = 'hand2', command = self.folders) 
        self.titre.grid(padx = 100, sticky ='nsew') 
        
        
    def folders(self, back_to_folders = None):
        "Dossiers créés"

        self.image_folder = "/images/folder_icon.png" 
        self.folder_image = Image.open(self.directory + self.image_folder)
        self.folder_image_size = 128, 128
        self.folder_image.thumbnail(self.folder_image_size)
        self.photo_folder = ImageTk.PhotoImage(self.folder_image, master = self.window)

        # Si l'utilisateur revient sur la page des albums:

        if back_to_folders == True : 
            for self.child in self.main_frame.winfo_children():
                self.child.destroy()
            self.home = LabelFrame(self.main_frame, labelanchor='n', font='Times 40 italic',\
                        bg='white', relief='ridge', bd=3, padx=20, pady=20)
            self.home.grid(row = 0, padx = 300, pady = 60)

        for self.child in self.home.winfo_children():
            if self.child.winfo_class() == 'Button':
                self.child.destroy()
        self.home.config(text = ' Mes albums ')
        self.home.grid(padx = 200)

        self.can_dossiers_defil = Scrollbar(self.first_frame, bg = self.read_color, relief='ridge',\
                                  width = 18, orient = 'vertical', troughcolor = 'white',\
                                  activebackground = self.read_color)
        self.can_dossiers_defil.grid(row=0,column=1, rowspan = 2, sticky='ns')
        self.can_dossiers = Canvas(self.home, bg = 'white', highlightthickness = 0 ,\
                            scrollregion = (0,0,5000,5000),height = 500, width = 700, \
                            yscrollcommand = self.can_dossiers_defil.set)
        self.can_dossiers.grid(row = 0, column = 0)
        self.can_dossiers.grid_propagate(0)
        self.can_dossiers_defil.config(command=self.can_dossiers.yview)
        
        with open("dossiers_images", 'r') as file_ : 
            readfile = file_.readlines()

        # Variables de positionnement des images dans le canvas:

        self.a = 5      
        self.b = 10
        
        # Liste qui contient les images illustrant les boutons de chaque album créé:
        
        self.list_buttons_images = []
        
        # Liste qui contient les noms des albums créés:
        
        self.list_labels_images = []

        # image représentant un album vide (Bouton "Nouvel album"):

        self.empty_folder_image = "/images/empty_folder.png" 
        self.image_empty_folder = Image.open(self.directory + self.empty_folder_image)
        self.image_empty_folder_size = 100, 100
        self.image_empty_folder.thumbnail(self.image_empty_folder_size)
        self.empty_folder_photo = ImageTk.PhotoImage(self.image_empty_folder, master = self.window)

        # Image illustrant un dossier créé mais qui ne contient aucune image:

        self.new_folder_image = "/images/default_image.png" 
        self.image_new_folder = Image.open(self.directory + self.new_folder_image)
        self.new_folder_size = 128, 128
        self.image_new_folder.thumbnail(self.new_folder_size)
        self.new_folder_photo = ImageTk.PhotoImage(self.image_new_folder, master = self.window)
    
        # Parcours de la liste des albums créés:
    
        for i, element in enumerate(readfile): 
            # Ajout de chaque nom d'album
            self.list_labels_images.append(readfile[i].strip()) 
            # Création des cadres (Boutons + Labels)
            self.folder_and_label = LabelFrame(self.can_dossiers, bg = 'white', bd = 0) 
            # Placement des cadres dans le canvas
            self.can_dossiers.create_window(self.b, self.a, anchor = 'nw', window = self.folder_and_label)
            self.b += 140 # Incrémentation de la variable des colonnes
            if self.b > 680 :
                self.a += 185 # Incrémentation de la variable des lignes
                self.b = 10
            with open(readfile[i].strip(), 'r') as file_i: 
                read_file_i = file_i.readlines()

            if len(read_file_i) > 0 : 
                # Si l'album contient des images, la 1ère image illustre le bouton:
                self.image_read_file = Image.open(read_file_i[0][0:read_file_i[0].index('~#~')])
                self.image_read_file_size = 160, 160
                self.image_read_file.thumbnail(self.image_read_file_size)
                self.read_file_photo = ImageTk.PhotoImage(self.image_read_file, master = self.window)
                self.list_buttons_images.append(self.read_file_photo)
                self.folder = Button(self.folder_and_label, image = self.list_buttons_images[i],\
                              bg = 'white', height = 100, width = 100, bd = 2, highlightthickness = 1,\
                              command = lambda arg1 = readfile[i].strip(),\
                              arg2 = self.home : self.phototheque(arg1, home = arg2))
            elif len(read_file_i) == 0 : 
                # Si l'album ne contient pas d'images, l'image par défaut s'affiche:
                self.folder = Button(self.folder_and_label, image = self.new_folder_photo, bg = 'white',\
                              height = 100, width = 100, bd = 2, highlightthickness = 1,\
                              command = lambda arg1 = readfile[i].strip(),\
                              arg2 = self.home : self.phototheque(arg1, home = arg2))
            self.folder_label = Label(self.folder_and_label, bg = 'white', text = readfile[i].strip(),\
                                font = ('Times', '11', 'italic')) #Noms de l'album
            self.folder.grid(row = 0, column = 0)
            self.folder_label.grid(row = 1, column = 0)
            
            # Le clic droit sur le nom de l'album permet de renommer le dossier :
            
            self.folder_label.bind('<Button-3>', lambda event, arg1 = self.folder_and_label,\
            arg2 = self.folder_label['text']: self.rename(arg1, arg2))


        self.folder_and_label = LabelFrame(self.can_dossiers, bg = 'white', bd = 0)
        self.can_dossiers.create_window(self.b, self.a, anchor = 'nw', window = self.folder_and_label)
        
        # Appel de le fonction self.warning_empty_entry si le nom de l'album n'est pas renseigné:
        
        self.new_folder = Button(self.folder_and_label, image = self.empty_folder_photo, bg = 'white',\
                                  height = 100, width = 100, bd = 2, highlightthickness = 1,\
                                  command = self.warning_empty_entry)
        self.new_folder.grid(row = 0, column = 0)
        
        # Création du champ d'entrée pour renseigner le nom du nouvel album:
        
        self.new_folder_entry = Entry(self.folder_and_label, bg = 'white', width = 10,\
                                font = ('Times', '12', 'bold italic'))
        self.new_folder_entry.grid(row = 1, column = 0)
        self.new_folder_entry.insert(0, "  Nouveau")
        
        # Liaisons du widget : effacement du contenu du champ d'entrée, création du nouvel album
        
        self.new_folder_entry.bind('<Button-1>', lambda event: self.new_folder_entry.delete(0, 'end'))
        self.new_folder_entry.bind('<Return>', self.add_folder)


    def add_folder(self, event):
        "Création d'un nouvel album"
        
        self.new_label = self.new_folder_entry.get()

        with open("dossiers_images", 'r') as file_ :
            readfile = file_.readlines()
            if self.new_label + '\n' in readfile :
                # L'utilisateur doit donner un nom qui n'est pas déjà attribué :
                tkinter.messagebox.showwarning('Nouvel album', 'Cet album existe déjà.')
                self.new_folder_entry.delete(0, 'end')
            else : 
                with open("dossiers_images", 'a') as file_:
                    file_.write(self.new_folder_entry.get() + '\n')
                # Création du nouveau fichier images (vide pour l'instant)
                with open(self.new_folder_entry.get(), 'w') as new_file:
                    # Appel de la méthode photothèque qui ouvre le nouvel album:
                    self.phototheque(self.new_folder_entry.get(), home = self.home)
                    
                    
    def warning_empty_entry(self):
        """Le champ d'entrée est rouge pendant une seconde pour prévenir 
           l'utilisateur qu'il doit renseigner le nom de l'album qu'il souhaite créer."""
        
        self.new_folder_entry.config(bg = 'red', fg = 'white')
        self.new_folder_entry.after(1000, lambda : self.new_folder_entry.config(bg = 'white',\
        fg = 'black'))


    def rename(self, folder_and_label, current_label):
        "Méthode permettant de renommer un dossier"

        self.folder_and_label = folder_and_label
         # nom actuel de l'album à renommer:
        self.current_label = current_label
        # Boucle qui parcourt les albums existants :
        for i in range(0, len(self.can_dossiers.winfo_children())):
            for j in self.can_dossiers.winfo_children()[i].winfo_children():
                self.index_j = self.can_dossiers.winfo_children()[i].winfo_children().index(j)   
                # si le nom de l'album correspond à la variable self.current label:       
                if j.winfo_class() == 'Label' and j['text'] == self.current_label: 
                    j.destroy() # Destruction du nom et remplacement par un champ d'entrée:
                    self.entry_replacing_label = Entry(self.can_dossiers.winfo_children()[i],\
                                                 bg = 'white', width = 10)
                    self.entry_replacing_label.grid(row = 1, column = 0)
                    self.index_i(i) 
                    self.can_dossiers.after(4000, lambda : self.close_entry(self.folder_and_label,\
                    self.entry_replacing_label))
                    
                    
    def close_entry(self, folder_and_label, entry_replacing_label):
        """Ferme le champ d'entrée si l'utilisateur n'a toujours pas
           entré de nouveau nom après 4 secondes"""
           
        self.folder_and_label = folder_and_label
        self.entry_replacing_label = entry_replacing_label
        if self.entry_replacing_label.get() == '' :
            self.entry_replacing_label.destroy()
            self.back_folder_label = Label(self.folder_and_label, bg = 'white',\
                                     text = self.current_label,\
                                     font = ('Times', '12', 'italic'))
            self.back_folder_label.grid(row = 1, column = 0)
            self.back_folder_label.bind('<Button-3>', lambda event, arg1 = self.folder_and_label,\
            arg2 = self.current_label : self.rename(arg1, arg2))


    def index_i(self, i):
        "Liaison du widget Entry à la méthode new_text"

        self.i = i
        self.can_dossiers.winfo_children()[self.i].winfo_children()[1].bind('<Return>',\
        lambda event : self.new_text(self.i))
        

    def new_text(self, i):
        "Renommage du dossier"

        self.i = i # Incrémentation
        # Affectation de la nouvelle valeur récupérée dans le widget Entry:
        self.newlabel = self.can_dossiers.winfo_children()[self.i].winfo_children()[1].get()
        with open('dossiers_images', 'r') as file_ : 
            readfile = file_.readlines()
            # Suppression de la ligne contenant le nom actuel de l'album
            # pour éviter l'apparition du message de la ligne 233
            # qui n'a pas lieu d'apparaître s'il s'agit de l'album à renommer:
            readfile.remove(readfile[self.i])
        # Si le nouveau nom est déjà dans l'album : 
        if self.newlabel + '\n' in readfile : 
            tkinter.messagebox.showwarning('Nouvel album', 'Cet album existe déjà.')
            # Le widget Entry est vidé de son contenu : 
            self.can_dossiers.winfo_children()[self.i].winfo_children()[1].delete(0, 'end')
        else :
            # Destruction du widget Entry:
            self.can_dossiers.winfo_children()[self.i].winfo_children()[1].destroy()
            # Instanciation d'un widget Label avec le nouveau nom de l'album :
            self.new_folder_label = Label(self.can_dossiers.winfo_children()[self.i],\
                                    bg = 'white',\
                                    text = self.newlabel, font = ('Times', '12', 'italic'))
            self.new_folder_label.grid(row = 1, column = 0)
            # Liaison du widget Label avec la méthode self.rename
            # au cas ou l'utilisateur souhaite renommer une deuxième fois son album:
            self.new_folder_label.bind('<Button-3>', lambda event,\
            arg = self.newlabel : self.rename(arg))
            # Renommage de l'album dans le système d'exploitation:
            os.rename(self.current_label, self.newlabel)
            # Renommage de l'album dans le fichier "dossiers_images":
            with open('dossiers_images', 'r') as file_:
                readfile = file_.readlines()
                for i, element in enumerate (readfile) :
                    if readfile[i] == self.current_label + '\n':
                        readfile.remove(readfile[i])
                        readfile[i:i] = [self.newlabel+ '\n']
            # Effacement du fichier contenant l'ancien nom de l'album 
            # et réécriture avec le nouveau nom:
            with open('dossiers_images', 'w') as file_:
                for i, element  in enumerate (readfile) :
                    file_.write(readfile[i])


    def phototheque(self, import_photos, pictures = None, legende = None,\
        apercu_image = None, home = None) :
        "Ouverture de l'album après avoir cliqué sur le bouton"
        
        self.import_photos = import_photos
        self.pictures = pictures
        self.legende = legende
        self.apercu_image = apercu_image
        self.home = home
        self.back_to_folders = True
        
        for child in self.first_frame.winfo_children():
            if child.winfo_class() == 'Scrollbar':
                child.destroy()
        
        # Destruction des éventuels widgets avant d'afficher les images:
        
        if not self.home == None :
            self.home.destroy()
        if not self.legende == None and not self.apercu_image == None:
            self.legende.delete(0, 'end')
            self.apercu_image.destroy()
        if self.pictures != None:
            for self.child in self.pictures.winfo_children():
                self.child.destroy()
        else :
            self.pictures_defil = Scrollbar(self.main_frame, bg = self.read_color, relief='ridge', width = 18,\
                                  orient = 'vertical', troughcolor = 'white',\
                                  activebackground = self.read_color)
            self.pictures_defil.grid(row=0,column=1, rowspan = 2, sticky='ns')
            self.pictures = Canvas(self.main_frame, bg='white', height = 700,\
                            width = 1100, scrollregion = (0,0,10000,10000),\
                            highlightbackground = self.read_color,\
                            yscrollcommand = self.pictures_defil.set)
            self.pictures.grid(row=1, column=0, padx = 30, pady = 10)
            self.pictures.config(scrollregion=self.pictures.bbox('all'))
            self.pictures_defil.config(command=self.pictures.yview)

            # Images illustrant les boutons de la barre de tâches :
            
            self.upload_image = "/images/upload.png"
            self.image_upload = Image.open(self.directory + self.upload_image)
            self.image_upload_size = 70, 70
            self.image_upload.thumbnail(self.image_upload_size)
            self.photo_upload = ImageTk.PhotoImage(self.image_upload, master = self.window)

            self.image_corbeille = "/images/corbeille.png"
            self.corbeille_image = Image.open(self.directory + self.image_corbeille)
            self.corbeille_image_size = 64, 64
            self.corbeille_image.thumbnail(self.corbeille_image_size)
            self.photo_corbeille = ImageTk.PhotoImage(self.corbeille_image, master = self.window)
           
            self.image_folder = "/images/folder_icon.png"
            self.folder_image = Image.open(self.directory + self.image_folder)
            self.folder_image_size = 64, 64
            self.folder_image.thumbnail(self.folder_image_size)
            self.photo_folder = ImageTk.PhotoImage(self.folder_image, master = self.window)

            self.image_rotate = "/images/image_rotate.png"
            self.rotate_image = Image.open(self.directory + self.image_rotate)
            self.rotate_image_size = 64, 64
            self.rotate_image.thumbnail(self.rotate_image_size)
            self.photo_rotate = ImageTk.PhotoImage(self.rotate_image, master = self.window)
            

            # Création des boutons (téléversement, corbeille, albums):

            self.icons = LabelFrame(self.main_frame, bg = 'white', bd = 0)
            self.icons.grid(row = 0, sticky = 'w', pady = 20, padx = 20)
            self.import_picture = Button(self.icons,image = self.photo_upload, bd = 1,\
                                  highlightthickness = 1, command = self.importer)
            self.import_picture.grid(row = 0, sticky = 'w', padx = 5)
            self.delete_folder = Button(self.icons,image = self.photo_corbeille, bd = 2,\
                                 highlightthickness = 1, command = self.tout_supprimer)
            self.delete_folder.grid(row = 0, column = 1, sticky = 'w', padx = 5)
            self.open_folder = Button(self.icons,image = self.photo_folder, bd = 2,\
                               highlightthickness = 1,\
                               command = lambda arg = self.back_to_folders : self.folders(arg))
            self.open_folder.grid(row = 0, column = 2, sticky = 'w', padx = 5)
            self.legende = Entry(self.icons, width = 60, font = ('Times', '14', 'bold'),\
                           highlightbackground = self.read_color, disabledbackground = 'white',\
                           state = 'disabled')
            self.legende.grid(row = 0, column = 3, sticky = 'w', padx = 5)
        
        self.liste_photos = []
        self.a = 25
        self.b = 10
        self.c = 0
        
        # Ouverture du fichier contenant les images de l'album sélectionné:
        with open(self.import_photos, 'r') as file_ : 
            readfile = file_.readlines()
            # Compréhensions de liste [liste des images, liste des légendes]
            self.readfile2 = [readfile[i][0:readfile[i].index('~#~')]\
            for i, element in enumerate(readfile)]
            
            self.readfile3 = [readfile[i][(readfile[i].index('~#~') + 3):]\
            for i, element in enumerate(readfile)]
            
            for i, element in enumerate(self.readfile2):
                if self.b > 1070 : # Variables de positionnement des images
                    self.a += 350
                    self.b = 10
                self.liste_photos.append(readfile[i])
                self.image = Image.open(self.readfile2[i].strip())
                self.image2 = Image.open(self.readfile2[i].strip())
                self.photo = Boutons_photos(self.window, self.import_photos, self.main_frame,\
                             self.pictures, self.image, self.image2, self.readfile3[i], self.a,\
                             # Création des objets boutons-photos
                             self. b, self.c, self.liste_photos) 
                self.c+=1 # Variable d'indexation des photos
                self.photo.creation_bouton() 
                self.b += 270


    def importer(self):
        "Méthode permettant d'importer des photos"

        self.path = tkinter.filedialog.askopenfilename(title="Importer une image",\
                    filetypes=[('png files','.png'),('all files','.*')])
        self.path = shutil.copy(self.path, "images/images_phototheque")
        with open(self.import_photos, 'r') as file_:
            readfile = file_.readlines()
            readfile2 = ''.join(readfile)
            if self.path in readfile2:
                tkinter.messagebox.showwarning("Photo déjà importée", "Cette photo a déjà été importée.")
            else:
                self.apercu = Image.open(self.path)
                self.apercu_size = 128, 128
                self.apercu.thumbnail(self.apercu_size)
                self.apercu_photo = ImageTk.PhotoImage(self.apercu, master = self.window)
                self.legende.config(state = 'normal')
                self.legende.insert(0, "  Saisissez la légende de la photo à importer.")
                self.apercu_image = Label(self.icons, image = self.apercu_photo)
                self.apercu_image.grid(row = 0, column = 4, padx = 5)
                self.legende.bind('<Button-1>', lambda event : self.delete_legende())


    def delete_legende(self):
        "Vide le message qui s'affiche de le champ d'entrée des légendes"
        self.legende.delete(0, 'end')
        self.legende.config(bg = 'white', fg = 'black')
        self.legende.bind('<Return>', lambda event : self.get_legende())
        

    def get_legende(self):
        "Récupération de la légende entrée par l'utilisateur pour une image téléchargée"
        self.gotten_legend = self.legende.get()
        self.read_file2 = []
        with open(self.import_photos, 'r') as file_ :
            readfile = file_.readlines()
        for i in readfile : # Récupération de toutes les légendes
            i = i[i.index('~#~') + 3:].strip()
            self.read_file2.append(i)
        if self.gotten_legend in self.read_file2: # Messages d'avertissement
            tkinter.messagebox.showwarning('Légende',\
            'Il existe déjà une image intitulée "' + self.gotten_legend + '".')
        elif self.gotten_legend.isspace() == True or self.gotten_legend == '' or\
            self.gotten_legend.startswith("  Saisissez"):
            self.legende(0, 'end')
            tkinter.messagebox.showwarning('Légende',\
            'Saisissez une légende pour la photo importée.')
        else:
            with open(self.import_photos, 'r') as file_:
                readfile = file_.readlines()
                readfile.append(self.path + '~#~' + self.gotten_legend + '\n')
            with open(self.import_photos, 'w') as file_ :
                for i in readfile :
                    file_.write(i) 
            self.phototheque(self.import_photos, self.pictures, self.legende, self.apercu_image)
            

    def tout_supprimer(self):
        "Supprime l'album sélectionné"
        
        self.oui_non = tkinter.messagebox.askyesnocancel("supprimer l'album?",\
        'Souhaitez-vous vraiment supprimer cet album?\nCette opération est irréversible.')
        if self.oui_non == False or self.oui_non == None :
            pass
        elif self.oui_non == True :
            with open('dossiers_images', 'r') as self.folder :
                self.read_folder = self.folder.readlines()
            for i, element in enumerate(self.read_folder):
                if self.import_photos == self.read_folder[i].strip():
                      self.read_folder.remove(self.read_folder[i])
            with open('dossiers_images', 'w') as self.folder :
                for i, element in enumerate(self.read_folder):
                    self.folder.write(self.read_folder[i])
            os.remove(self.directory + '/' + self.import_photos)
            self.back_to_folders = True
            self.folders(self.back_to_folders)


class Boutons_photos(Phototheque) :
    "Classe instanciant les 'boutons-photos' et les photos en taille originale"

    def __init__(self, window, import_photos, main_frame, pictures, image, image2,\
                photo_label,a, b, c, liste_photos) :
        "Méthode constructeur"
        
        Phototheque.__init__(self)
        self.window = window
        self.import_photos = import_photos
        self.main_frame = main_frame
        self.pictures = pictures
        self.image = image	
        self.image2 = image2
        self.photo_label = photo_label
        self.a = a
        self.b = b
        self.c = c
        self.c2 = None
        self.liste_photos = liste_photos
        self.dico = {}
             
    def creation_bouton(self) :
        "Méthode de création des 'boutons-photos'"
        
                
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = 'green'
        
        self.directory = os.getcwd()
        self.adresse_can2 = []
        
        self.size = 256, 256
        self.image.thumbnail(self.size)
        self.photo = ImageTk.PhotoImage(self.image, master = self.window)
        
        # Image de la croix (pour supprimer les images)
        self.cross_image = "/images/croix.png" 
        self.image_cross = Image.open(self.directory + self.cross_image)
        self.image_cross_size = 16, 16
        self.image_cross.thumbnail(self.image_cross_size)
        self.cross_photo = ImageTk.PhotoImage(self.image_cross, master = self.window)
        
        self.can2 = Canvas(self.pictures, bg='white', highlightthickness=0, bd = 0)
        self.pictures.create_window(self.b, self.a, anchor = 'nw', window = self.can2)
        # Création d'une liste de deux éléments avec self.c (pour l'indexation) 
        # et self.can2(pour la photo et le bouton de suppression)
        self.adresse_can2.append(self.c)
        self.adresse_can2.append(self.can2)
        self.mini_photo = Button(self.can2, bg='white', bd=0, image=self.photo,\
                          activebackground=self.read_color, cursor='hand2', command = self.agrandir_pivoter)
        self.mini_photo.grid(row=0, column = 0, sticky ='n')
        self.cross = Button(self.can2, image = self.cross_photo, highlightthickness = 0,\
                     bd = 0 , cursor='hand2', command = self.supprimer)
        self.cross.grid(row=0, column = 0, sticky = 'ne')
        self.label_photo = Label(self.can2, bg = 'white', text = self.photo_label,\
                           font = ('Times', '12', 'bold'), wraplength = 200, pady = 5)
        self.label_photo.grid(row = 1, sticky='n')
        # Liaison du label à la méthode rename:
        self.label_photo.bind('<Button-3>',\
        lambda event : self.rename_picture(self.label_photo['text'], self.can2))


    def rename_picture(self, current_label, can2):
        "Renommage des images"

        self.current_label = current_label
        self.can2 = can2
        for i in range(0, len(self.pictures.winfo_children())):
            for i2 in self.pictures.winfo_children()[i].winfo_children():
                self.index_i2 = self.pictures.winfo_children()[i].winfo_children().index(i2)
                if i2.winfo_class() == 'Label' and i2['text'] == self.current_label:
                    i2.destroy()
                    i2 = Entry(self.can2, bg = 'white', width = 10)
                    i2.grid(row = 1, column = 0)
                    self.pic_index_i(i)


    def pic_index_i(self, i):
        "Liaison du widget Entry à la méthode pic_new_text"

        self.i = i
        self.pictures.winfo_children()[self.i].winfo_children()[2].bind('<Return>',\
        lambda event : self.pic_new_text(self.i))


    def pic_new_text(self, i):
        "Renommage des images"
        
        self.i = i
        self.pic_newlabel = self.pictures.winfo_children()[self.i].winfo_children()[2].get()
        self.pictures.winfo_children()[self.i].winfo_children()[2].destroy()
        self.in_file = False
        self.new_picture_label = Label(self.pictures.winfo_children()[self.i],\
                                 bg = 'white', font = ('Times', '12', 'bold'))
        self.new_picture_label.grid(row = 1, column = 0)
        self.new_picture_label.bind('<Button-3>', lambda event, arg1 = self.current_label,\
        arg2 = self.can2 : self.rename_picture(arg1, arg2))
        
        with open(self.import_photos, 'r') as file_ :
            readfile = file_.readlines()
            self.read_file2 = []
        for i in readfile :
            i = i[i.index('~#~') + 3:].strip()
            self.read_file2.append(i)
        if self.pic_newlabel in self.read_file2:
            self.in_file = True
            tkinter.messagebox.showwarning('Légende',\
            'Il existe déjà une image intitulée "' + self.pic_newlabel + '".')
            self.pic_newlabel = self.current_label
            self.new_picture_label.config(text = self.current_label)
        if self.in_file == False :
            with open(self.import_photos, 'r') as file_:
                readfile = file_.readlines()
            for i, x in enumerate (readfile) :
                if readfile[i][readfile[i].index("~#~")+3:] == self.current_label:
                    # Remplacement de l'ancienne légende par la nouvelle:
                    readfile[i] = readfile[i].replace(self.current_label, self.pic_newlabel + '\n')
            with open(self.import_photos, 'w') as file_:
                for i in readfile :
                    file_.write(i)
            self.new_picture_label.config(text = self.pic_newlabel)
        self.phototheque(self.import_photos)
 
 
    def agrandir_pivoter(self):
        "Agrandir ou pivoter la photo?"
        
        self.image_resize = "/images/resize.png"
        self.image4 = Image.open(self.directory + self.image_resize)
        self.image4_size = 96, 96
        self.image4.thumbnail(self.image4_size)
        self.photo_resize = ImageTk.PhotoImage(self.image4)

        self.image_rotate = "/images/image_rotate.png"
        self.image5 = Image.open(self.directory + self.image_rotate)
        self.image5_size = 96, 96
        self.image5.thumbnail(self.image5_size) 
        self.photo_rotate = ImageTk.PhotoImage(self.image5)
        
        self.choix = Toplevel(name = 'selected', bg  = 'white')
        self.label_agrandir_pivoter = Label(self.choix, bg = 'white', fg = 'black',\
                                      text = "Voulez-vous agrandir\nou pivoter la photo?",\
                                      font = ('Times', '14', 'bold'))
        self.label_agrandir_pivoter.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)
        self.agrandissement = Button(self.choix, image = self.photo_resize, bg = 'black', bd = 2,\
                              highlightthickness = 1, command = self.photo_agrandie)
        self.agrandissement.grid(row = 1, column = 0, sticky = 'w', padx = 10, pady = 10)
        self.rotate_image = Button(self.choix, image = self.photo_rotate, bg = 'black', bd = 2,\
                            highlightthickness = 1, command = self.rotate)
        self.rotate_image.grid(row = 1, column = 1, sticky = 'w', padx = 10, pady = 10)


    def photo_agrandie(self) :
        "Méthode permettant d'agrandir les photos"

        self.grande_photo = Toplevel(name = 'selected')
        self.photo2 = ImageTk.PhotoImage(self.image2)
        if self.image2.size[0] > 768 and self.image2.size[1] > 768:
            self.image2_size = 1024, 1024
            self.image2.thumbnail(self.image2_size)
        self.photo2 = ImageTk.PhotoImage(self.image2)
        self.label_photo = Label(self.grande_photo, image = self.photo2)
        self.label_photo.grid()


    def rotate(self):
        "Pivote l'image"

        self.im2_rotate = self.image2.rotate(270, expand = True)
        with open(self.import_photos, 'r') as file_ :
            readfile = file_.readlines()
        self.filename = readfile[self.c][:readfile[self.c].index('~#~')]
        self.im2_rotate.save(self.filename)
        self.phototheque(self.import_photos, self.pictures)
        self.choix.destroy()

#---------------------------------------------------------------------------------------------------------      
       
    def supprimer(self) :
        "Méthode permettant de supprimer des photos"
        self.oui_non = tkinter.messagebox.askyesnocancel('supprimer la photo?',\
                       'Souhaitez-vous vraiment supprimer cette photo?')

        if self.oui_non == False or self.oui_non == None :
            pass
        elif self.oui_non == True :
            self.d = 0 # Variable d'indexation 
            self.list_can2 = []	
            self.picture_path = []
            for can2 in self.pictures.winfo_children() :
                if can2 != self.mini_photo and can2 != self.cross :
                    self.list_can2.append(self.d)
                    self.d += 1
            for i in range(0, len(self.liste_photos)) :
                self.sous_liste = []
                # L'index et le chemin de chaque photo sont placés dans la sous-liste 
                #elle-même placée dans la liste self.picture_path.
                self.sous_liste.append(self.list_can2[i]) 
                self.sous_liste.append(self.liste_photos[i])
                self.picture_path.append(self.sous_liste)
            j = 0
            while j < len(self.picture_path):
                # On compare l'indice de la photo à supprimer avec les indices de la liste
                if  self.adresse_can2[0] == self.picture_path[j][0] :
                    # Si il y a concordance, on supprime l'indice et le chemin de la liste: 
                    self.picture_path.remove(self.picture_path[j])
                j+=1
            self.can2.destroy()
            with open(self.import_photos, 'w') as file_ :
                for i in range(0, len(self.picture_path)):
                    file_.write(self.picture_path[i][1])
            self.phototheque(self.import_photos, self.pictures)


# ============MAIN PROGRAMM ==================================================

if __name__ == "__main__":

    phototheque = Phototheque()
    phototheque.home()