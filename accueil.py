
import os 
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog 
import tkinter.colorchooser
from PIL import Image, ImageTk
import shutil
import collections 
from mon_jardin.calendrier import Calendrier
from mon_jardin.agenda import Agenda
from mon_jardin.module_notes import Notes
from mon_jardin.phototheque import Phototheque
from mon_jardin.species import Species

class Home(object):
    "Instanciation de la page d'accueil"

    os.chdir(os.getcwd() + "/mon_jardin")

    def __init__(self):
        """Méthode constructeur qui s'exécute automatiquement 
           lorsque un nouvel objet est créé par instanciation d'une classe."""


    def home(self) : 
        "Création de la page d'accueil"
        
        self.directory = os.getcwd()

        self.main_window = Tk()
        self.main_window.title('Mon jardin 3.0')
        self.main_window.config(bg='white')
        self.main_window.resizable(True, True)
                        
        self.home_image = "/images/mon_jardin.png"
        self.image = Image.open(self.directory + self.home_image)
        self.image_size = 512, 384
        self.image.thumbnail(self.image_size)
        self.photo = ImageTk.PhotoImage(self.image, master = self.main_window)
        
        self.main_frame = Frame(self.main_window, bg= 'white', relief = 'ridge', bd = 0, padx = 200, pady = 100) 
        self.main_frame.pack()
        self.homepage()
        
        self.main_window.mainloop()


    def homepage(self):
        "Création du bouton principal de la page d'accueil"
        
        for child in self.main_frame.winfo_children(): 
            child.destroy()
            
        # Couleur:

        file_color = open("file_color", "a")
        file_color.close()
        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == "":
                self.read_color = 'green'
                
        self.home_accueil = LabelFrame(self.main_frame, text = ' MON JARDIN ',\
                          labelanchor = 'n', font = 'Times 40 italic', bg = 'white',\
                          fg = self.read_color, relief = 'ridge', bd = 3, padx = 50, pady = 50)
        self.home_accueil.pack(expand = True, fill = BOTH)
        for child in self.home_accueil.winfo_children():
            child.destroy()
        self.titre=Button(self.home_accueil, image=self.photo, bg=self.read_color,\
                   relief='ridge', cursor = 'hand2', bd=3, command=self.buttons)
        self.titre.pack()


    def buttons(self):
        "Création des boutons de la page menu"
        
        self.titre.destroy()
        self.home_accueil.pack()
        self.buttons_frame = Frame(self.home_accueil, bg='white', padx=20)
        self.buttons_frame.pack()
        
        # Images illustrant les boutons:
        
        images = ["/images/home.png" ,
                  "/images/calendar.png" ,
                  "/images/legumes.png" ,
                  "/images/fruits.png",
                  "/images/post_it.png",
                  "/images/default_image.png"]
        
        type_ = ["legumes", "fruits"]
        type_2 = ["légumes", "fruits"]
        index_type = [2, 3]
        
        
        self.tabs_list=[]
        row_number=0
        column_number=0

        images_open = [Image.open(self.directory + i) for i in images]
        images_size = (172, 139)
        for i in images_open:
            i.thumbnail(images_size)
        self.photos = [ImageTk.PhotoImage(i, master = self.main_window) for i in images_open]

        # Création des boutons et des boutons-menu:
        
        for i, element in enumerate(images):
            tab = Menubutton(self.buttons_frame, bg = 'white', activebackground = 'white',\
                  relief = 'ridge', bd = 2, fg = 'white', font = 'Times 24 italic',\
                  cursor = 'hand2')
            if i == 4 or i == 5 :
                tab = Button(self.buttons_frame, bg = 'white', activebackground = 'white',\
                      font = 'Times 24 italic', cursor = 'hand2')
            tab.grid(row = row_number, column = column_number, padx = 30, pady = 30, sticky = 'ew')
            column_number += 1
            if column_number % 3 == 0:
                row_number += 1
                column_number = 0
            self.tabs_list.append(tab)
            
        for i, element in enumerate(self.tabs_list):
            self.tabs_list[i].configure(image = self.photos[i])
            
        # Création du menu du bouton d'accueil:
            
        home_basic_func = Menu(self.tabs_list[0], bg = 'white', fg = self.read_color,\
                          bd = 2, relief = 'ridge', font = 'Times 14 italic')
        home_basic_func.add_command(label = 'Page d\'accueil', underline = 0,\
                                             command = self.homepage)
        home_basic_func.add_command(label = 'personnaliser l\'apparence',\
                                          underline = 0, command = self.change_color)
        home_basic_func.add_command(label = 'Quitter', underline = 0,\
                                             command = self.main_frame.quit)
        self.tabs_list[0].configure(menu = home_basic_func)
        
        # Création du menu du bouton calendrier-agenda:
        
        agenda = Agenda()
        agenda_basic_func = Menu(self.tabs_list[1], bg = 'white', fg = self.read_color, bd = 2,\
                            relief = 'ridge', font = 'Times 14 italic')
        agenda_basic_func.add_command(label = 'Calendrier', underline = 0,\
                            command = self.ouvrir_calendrier)
        agenda_basic_func.add_command(label = 'Agenda', underline = 0,\
                            command = agenda.pages)
        self.tabs_list[1].configure(menu = agenda_basic_func)
        
        notes = Notes()
        self.tabs_list[4].configure(command = notes.notes)
        
        phototheque = Phototheque()
        self.tabs_list[5].configure(command = phototheque.home)
        
                        
        list_object_add = []
        for i in range(len(type_2)):
            object_add = Home()
            list_object_add.append(object_add.show_list(self.tabs_list[i + 2], type_[i], type_2[i], self.read_color, self.home_accueil))
            
            
    def ouvrir_calendrier(self):
        "Création de l'objet calendrier"
        
        calendrier = Calendrier()
        calendrier.calendrier()
        calendrier.buttons()
        calendrier.current_week()
         
         
    def show_list(self, tabs_list, type_, type_2, read_color, home_accueil) :
        "Méthode qui déroule la liste des espèces enregistrées dans le menu du bouton."
        
        self.tabs_list = tabs_list
        self.type_ = type_
        self.type_2 = type_2
        self.read_color = read_color
        self.home_accueil = home_accueil
        
        file_images = open("images_{}".format(self.type_), 'a')
        file_images.close()
        with open("images_{}".format(self.type_), 'r') as file_images:
            readfile_images = file_images.readlines()
        file_ = open("{}".format(self.type_), 'a') 
        file_.close() 
        with open("{}".format(self.type_), 'r') as file_:
            readfile = file_.readlines() 

        # Création d'un dictionnaire ordonné.
        self.dico = {} # stocke le nom de l'espèce et l'image associée
        self.dico = collections.OrderedDict(self.dico) 
        for i, element in enumerate(readfile):
            self.dico[i] = (readfile_images[i].strip(), readfile[i].strip())

        # Création du menu déroulant:

        self.list = [] # stocke les objets créant les pages des espèces
        
        basic_func = Menu(self.tabs_list, bg = 'white', fg = self.read_color,\
        bd = 2, relief = 'ridge', font = 'Times 14 italic')
        
        basic_func.add_command(label = 'Rajouter un {}'.format(self.type_2[:-1]),\
        underline = 0, command = lambda: self.add(self.tabs_list, self.type_, self.type_2,\
        self.read_color, self.home_accueil))
        
        basic_func.add_command(label = 'Supprimer un {}'.format(self.type_2[:-1]),\
        underline = 0, command = lambda: self.remove_species(self.tabs_list, self.type_,\
        self.type_2, self.read_color, self.home_accueil))
        
        for i, element in enumerate(self.dico):
            species = Species(i, self.dico[i],\
            "varietes_" + self.dico[i][1].lower(),\
            "notes_" + self.dico[i][1].lower(), self.type_, self.type_2)
            
            self.list.append(species.species)
            
            basic_func.add_command(label = self.dico[i][1], underline = 0, command = self.list[i])
        
        self.tabs_list.configure(menu = basic_func)


    def add(self, tabs_list, type_, type_2, read_color, home_accueil):
        """Méthode qui ouvre une fenêtre de dialogue pour rajouter 
           une nouvelle espèce dans le menu déroulant."""
        
        self.rajout = Toplevel(bg = 'green')
        self.rajout.title("Rajouter un {}".format(type_2[:-1]))
        
        self.rajout_label = Label(self.rajout, bg = 'green', fg = 'white',\
        text = "Veuillez entrer le nom du nouveau {}".format(type_2[:-1]),\
        font = "Times 14 bold", pady = 5) 
        
        self.rajout_label.grid(row = 0, padx = 10)
        
        self.champ_rajout = Entry(self.rajout, width = 30, font = "Times 14")
        self.champ_rajout.grid(row = 1, padx = 10, pady = 10)
        
        self.champ_rajout.bind('<Return>', lambda event: self.save_new(tabs_list, type_, type_2,\
        read_color, home_accueil))


    def save_new(self, tabs_list, type_, type_2, read_color, home_accueil):
        """Méthode qui enregistre une nouvelle espèce 
           dans le menu déroulant et qui créé
           la page associée."""
           
        # Récupération du nom de la nouvelle espèce et ajout d'une majuscule au début du nom:
        
        new = self.champ_rajout.get().capitalize() 
        
        self.rajout.iconify()
        with open("{}".format(self.type_), 'r') as file_:
            readfile_ = file_.readlines()
        if new + "\n" in readfile_:
            tkinter.messagebox.showwarning("Déjà enregistré!",\
            "Ce {} est déjà enregistré.".format(self.type_2[:-1]))
        else:
            with open("{}".format(self.type_), 'a') as file_:
                file_.write(new + "\n")
            new_file_ = open("varietes_" + self.champ_rajout.get().lower(), 'a')
            new_file_.close()
            new_file_notes_ = open("notes_" + self.champ_rajout.get().lower(), 'a')
            new_file_notes_.close()
            with open('images_{}'.format(self.type_), 'a') as file_images :
                file_images.write("/images/default_image.png\n")
            self.show_list(tabs_list, type_, type_2, read_color, home_accueil) 
            import_picture = tkinter.messagebox.askquestion("Importer une image",\
            "Le nouveau {} vient d'être rajouté. Souhaitez-vous importer une image pour illustrer la page """.format(self.type_2[:-1]) + new + "?", icon = "question")
            
            if import_picture == "yes":
                choose_picture = tkinter.filedialog.askopenfilename(title = "Importer une image",\
                filetypes=[('png files','.png'),('all files','.*')])
                
                base_name = os.path.basename(choose_picture)
                shutil.copy(choose_picture, "images/images_{}".format(self.type_))
                
                with open("images_{}".format(self.type_), 'r') as file_images:
                    readfile_images = file_images.readlines()
                    readfile_images = readfile_images[:-1]
                    readfile_images.append('/images/images_{}/'.format(self.type_) + base_name + '\n')
                with open("images_{}".format(self.type_), 'w') as file_images : 
                    for i, element in enumerate(readfile_images):
                        file_images.write(readfile_images[i])
                tkinter.messagebox.showinfo("image rajoutée", "L'image a été rajoutée", parent = home_accueil)
        self.show_list(tabs_list, type_, type_2, read_color, home_accueil)
        self.list[len(self.list) - 1]()
        

    def remove_species(self, tabs_list, type_, type_2, read_color, home_accueil):
        """Méthode qui ouvre une fenêtre de dialogue pour supprimer 
           une espèce du menu déroulant."""
        
        self.remove = Toplevel(bg = 'red')
        self.remove.title("Supprimer un {}".format(self.type_2[:-1]))
        self.remove_label = Label(self.remove, bg = 'red', fg = 'white', text = "Entrez le nom du {} à supprimer".format(self.type_2[:-1]),\
                            font = "Times 14 bold", pady = 5) 
        self.remove_label.grid(row = 0, padx = 10)
        self.champ_remove = Entry(self.remove, width = 30, font = "Times 14")
        self.champ_remove.grid(row = 1, padx = 10, pady = 10)
        self.champ_remove.bind('<Return>', lambda event : self.to_remove(tabs_list, type_, type_2, read_color, home_accueil))


    def to_remove(self, tabs_list, type_, type_2, read_color, home_accueil):
        "Méthode qui supprime une espèce."
        
        self.directory = os.getcwd()
        
        to_be_removed = self.champ_remove.get()
        self.remove.iconify()
        removed = ''
        remove_confirmation = False
        with open("{}".format(self.type_), 'r') as file_:
            readfile = file_.readlines()
            if to_be_removed.capitalize() + '\n' not in readfile:
                tkinter.messagebox.showinfo("{} absent".format(self.type_2), "Ce {} n'est pas répertorié".format(self.type_2[:-1]))
            else:
                remove_confirmation = tkinter.messagebox.askokcancel("Supprimer ce {}?".format(self.type_2[:-1]),\
"Voulez-vous vraiment supprimer ce {}?\nCette opération est irréversible et\
 détruira toutes les données enregistrées.".format(self.type_2[:-1]))
        if remove_confirmation:
            with open("{}".format(self.type_), 'r') as file_:
                readfile = file_.readlines()
            for i, element in enumerate (readfile):
                if to_be_removed.lower() == readfile[i].lower().strip():
                    readfile.remove(readfile[i])
                    with open("{}".format(self.type_), 'w') as file_:
                        for i2, element in enumerate(readfile):
                            file_.write(readfile[i2])
                with open("images_{}".format(self.type_), 'r') as file_images:
                    readfile_images = file_images.readlines() 
                    if readfile_images[i] != "/images/default_image.png\n":
                        removed = readfile_images[i]
                    readfile_images.remove(readfile_images[i])
            if removed != '' and removed not in readfile_images: 
                os.remove(self.directory + removed.strip())
            with open("images_{}".format(self.type_), 'w') as file_images:
                for i, element in enumerate(readfile_images):
                    file_images.write(readfile_images[i]) 
            for i in os.listdir(self.directory):
                if i.startswith("varietes_" + to_be_removed.lower()):
                    os.remove(i)
            if self.directory + "/notes_" + to_be_removed.lower():
                os.remove(self.directory + "/notes_" + to_be_removed.lower())
            self.champ_remove.delete(0, 30) 
            self.show_list(tabs_list, type_, type_2, read_color, home_accueil) 

         
    def change_color(self):
        "Modification de l'apparence"
        
        new_color = tkinter.colorchooser.askcolor("green", parent = self.main_window)
        with open("file_color", 'w') as file_color:
            if new_color[1] != None:
                file_color.write(new_color[1])
            elif new_color[1] == None:
                file_color.write("green")
        with open ("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            self.homepage()
            self.buttons()
            tkinter.messagebox.showinfo("Modification prise en compte",\
            "La modification a été appliquée", parent = self.main_window)
            

# ============MAIN PROGRAMM ================================================== :

if __name__ == "__main__": 

    home = Home() 
    home.home() 