
import os 
from tkinter import*
import tkinter.messagebox
from PIL import Image, ImageTk
from time import localtime 


class Notes(object):
    "Instanciation d'une note"
    info_iterator = 0
    show_notes_iterator = 80
 
    def __init__(self):
        "constructeur"

        self.y = localtime()[0]
        self.m = localtime()[1]
        self.d = localtime()[2]
        self.numb_note = ''


    def notes(self, previous_note = None):
        "Création de la note"

        self.previous_note = previous_note
        if self.previous_note != None: # Destruction d'une éventuelle note précédente.
           self.previous_note.destroy()
       
        self.rep = os.getcwd() # Retourne le répertoire courant
       
        self.note = Tk()
        self.note.title("Ordinotes")
        self.note_frame = Frame(self.note, bg = 'yellow')
        self.note_frame.grid()
               
        self.menu_image = "/images/menu_icon.png" # Image de la page principale
        self.image = Image.open(self.rep + self.menu_image)
        self.image_size = 32, 32
        self.image.thumbnail(self.image_size) # Redimensionnement de l'image
        self.photo = ImageTk.PhotoImage(self.image, master = self.note)
       
        self.date_objet = LabelFrame(self.note_frame, bg = "yellow", bd = 0, highlightthickness = 0 ) # Barre contenant le menu, la date et le champ d'entrée de l'objet.
        self.date_objet.grid(row = 0, column = 0, sticky = 'nsew', pady = 10)
           
        self.menu_button = Menubutton(self.date_objet, image=self.photo) # Menu avec différentes commandes
        self.menu_button.grid(row= 0, column = 0, padx = 5)
        self.menu_func=Menu(self.menu_button, bg='black', fg='white', bd=2, relief='ridge', font= 'Times 14')
        self.menu_func.add_command(label='Nouveau', underline = 0, command = lambda arg = self.note : self.notes(arg))
        self.menu_func.add_command(label='Ouvrir', underline = 0, command = lambda arg = self.note : self.show(arg))
        self.menu_func.add_command(label='Enregistrer', underline = 0, command = lambda arg = self.note : self.save(arg))
        self.menu_func.add_command(label='Quitter', underline = 0, command = self.note.quit)
        self.menu_button.configure(menu = self.menu_func)
       
        self.entry_date = Entry(self.date_objet, bg="yellow", font='Times 14 bold', width = 10, bd = 0, highlightthickness = 0) # Date de la note
        self.entry_date.grid(row = 0, column = 1, padx = 10)
       
        if self.d < 10 and self.m < 10 : # Formatage de la date : rajout d'un zéro lorsque le jour et/ou le mois sont inférieurs à 10.
            self.entry_date.insert(0, '0' + str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        elif self.d < 10 :
            self.entry_date.insert(0, '0' + str(self.d) + '/' + str(self.m) + '/' + str(self.y))
        elif self.m < 10 :
            self.entry_date.insert(0, str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        else :
            self.entry_date.insert(0, str(self.d) + '/' + str(self.m) + '/' + str(self.y))
       
        self.label_objet = Label(self.date_objet, text = "Objet : ", bg = "yellow", font = 'Times 14 bold', padx = 5)
        self.label_objet.grid(row =0, column = 2)
        self.entry_objet = Entry(self.date_objet, bg="white", font='Times 14', width = 33, bd = 1, disabledbackground = 'white', disabledforeground = 'black')
        self.entry_objet.grid(row = 0, column = 3)
        self.entry_objet.focus_set() # Le focus est dirigé vers le champ d'entrée de l'objet.
        self.entry_objet.bind('<Return>', self.focus_editor)
       
        self.editor = Text(self.note_frame, bg = "yellow", state = "disabled", font='Times 14',  width = 60, height = 10, bd = 0, highlightthickness = 0, padx = 20, pady = 20)
        self.editor.grid(row = 1, column = 0, pady = 5)
       
        if Notes.info_iterator < 1 :
            self.warning_editor = tkinter.messagebox.showinfo('Objet', 'BIENVENUE DANS ORDINOTES.\n\nVeuillez renseigner le champ "Objet" et presser la touche "Entrée" avant de rédiger votre note.')    
           
        Notes.info_iterator += 1 # Incrémentation de la variable pour afficher le message précédent une seule fois.
        self.note.mainloop() # Déclenchement du réceptionnaire d'événements
 
#----------------------------------------------------------------------------
 
    def focus_editor(self, event):
        "Autorise l'écriture de la note après avoir renseigné l'objet"
        if self.entry_objet.get() != '' and not self.entry_objet.get().isspace():
            self.editor.config(state='normal')
            self.editor.focus_set()
       
#----------------------------------------------------------------------------
   
    def save(self, note) :
        "Enregistrement de la note"
        self.note = note
        for child in self.note.winfo_children() :
            if child.winfo_class() == 'Toplevel' :
                child.iconify()       
        #self.note.after(100, lambda arg = self.note : self.destroy_widget(arg)) # Destruction de la note.
        self.note_number = open('note_number', 'a')
        self.note_number.close()
        with open('note_number', 'r') as self.note_number: # Attribution d'un n° à chaque note suivi d'une itération.
            self.iterateur = self.note_number.readline()
            if self.iterateur == "":
                self.iterateur = "0"
            self.iterateur = int(self.iterateur) + 1

        with open('note_number', 'w') as self.note_number:
            self.note_number.write(str(self.iterateur))
        self.get_entry_date = self.entry_date.get().replace('/', '_') # Variable qui stocke la date du jour et quiremplace les ':' par des '_'.
        self.get_editor = self.editor.get(1.0, 'end')
        self.get_entry_objet = self.entry_objet.get()
        if self.numb_note != '' : # Variable liée à la méthode self.change()
            with open(self.get_entry_date  + 'a' + self.numb_note + 'bnote', 'w') as self.file :
                self.file.write(self.get_entry_objet + '\n\n')
                self.file.write(self.get_editor)
            with open(self.get_entry_date  + 'a' + self.numb_note + 'bnote', 'r') as self.file :
                self.show_notes(self.get_entry_date  + 'a' + self.numb_note + 'bnote', self.note)
            self.numb_note = ''
        else :      
            with open(self.get_entry_date  + 'a' + str(self.iterateur) + 'bnote', 'w') as self.file :
                self.file.write(self.get_entry_objet + '\n\n')
                self.file.write(self.get_editor)
            #with open(self.get_entry_date  + 'a' + str(self.iterateur) + 'bnote', 'r') as self.file :
             #   self.show_notes(self.get_entry_date  + 'a' + str(self.iterateur) + 'bnote', self.note)
        self.editor['state'] = 'disabled' # Verrouillage de l'éditeur de texte (interdit en écriture)
 
#----------------------------------------------------------------------------
         
    def show(self, note):
        "Récapitulatif des notes rédigées qui apparaissent sous forme de boutons)"
        self.listdir = os.listdir(self.rep) # Liste de tous les fichiers contenus dans la chaîne de caractères passée en argument
        self.list_all_files = list()
        self.note = note
        for i, element in enumerate (self.listdir):
            self.string = os.path.splitext(self.listdir[i])[0]
            if self.string.endswith('note'):
                self.list_all_files.append(self.listdir[i]) # Liste de toutes les notes.
        print(self.listdir)
   
        self.summary = Toplevel(self.note, bg = 'white', padx=10, pady=10)
        self.summary.title('Vos notes')
        self.summary.lift(self.note)
        # self.note.after(3000, lambda arg = self.summary : self.destroy_widget(arg)) # Icônification de la fenêtre Toplevel
        self.label = Label(self.summary, bg = 'white', text = 'Votre bloc-notes contient ' + str(len(self.list_all_files)) + ' note.', fg = 'black', font='Times 18 bold')
        if len(self.list_all_files) > 1 :
            self.label['text'] = 'Votre bloc-notes contient ' + str(len(self.list_all_files)) + ' notes.'
        elif len(self.list_all_files) == 0 :
            self.label['text'] = 'Votre bloc-notes est vide.'
        self.label.grid(row=0, column = 0, columnspan = 4, pady = 10)
        self.i2 = 1 # variable d'incrémentation de la ligne dans le Toplevel
        self.i3 = 0 # variable d'incrémentation de la colonne dans le Toplevel
        for i in range(0, len(self.list_all_files)): # Création des boutons
            self.button_note = Button(self.summary, bg='black', fg='white', font = 'Times 14 bold',\
            text=self.list_all_files[i][0:10].replace('_','/') + '\n' + 'Note n°' + str(self.list_all_files.index(self.list_all_files[i]) + 1))
            self.button_note.grid(row=self.i2, column = self.i3, sticky = 'w')
            self.show_note = Notes() # Création de l'objet self.show_note
            self.show_note.show_notes # Appel de la méthode show_notes de la classe Agenda
            # Liaison du bouton à la méthode show_notes :
            self.button_note.config(command = lambda arg1 = self.list_all_files[i], arg2 = self.note, arg3 = self.summary : self.show_note.show_notes(arg1, arg2, arg3))
            self.i3 += 1 # Incrémentation de la colonne
            if self.i3 % 4 == 0:
                self.i2 += 1 # Incrémentation de la ligne lorsque le modulo 4 de la colonne est égal à 0.
                self.i3 = 0  # Réinitialisation de la colonne à 0 lorsqu'une nouvelle ligne commence.
 
#----------------------------------------------------------------------------
           
    def show_notes(self, note_file, previous_note = None, summary = None):
        "Affiche une note déjà écrite"
 
        self.rep = os.getcwd() # Retourne le répertoire courant
        self.note_file = note_file
        self.previous_note = previous_note
        
        for child in self.previous_note.winfo_children() :
            if child.winfo_class() == 'Toplevel' :
                child.withdraw()
        
        self.note = Tk()
        self.note.title("Ordinotes")
        self.note.geometry('580x340+' + str(Notes.show_notes_iterator) + '+' + str(Notes.show_notes_iterator)) # Apparition de la note dans le coin supérieur gauche.
        Notes.show_notes_iterator += 100 # Décalage de 100 par 100 pour la prochaine note qui sera affichée.
        self.note_frame = Frame(self.note, bg = 'yellow')
        self.note_frame.grid()
               
        self.menu_image = "/images/menu_icon.png" # Image de la page principale
        self.image = Image.open(self.rep + self.menu_image)
        self.image_size = 32, 32
        self.image.thumbnail(self.image_size) # Redimensionnement de l'image
        self.photo = self._photo = ImageTk.PhotoImage(self.image, master = self.note)
       
        self.date_objet = LabelFrame(self.note_frame, bg = "yellow", bd = 0, highlightthickness = 0 ) # Barre contenant le menu, la date et le champ d'entrée de l'objet.
        self.date_objet.grid(row = 0, column = 0, sticky = 'nsew', pady = 10)
       
       
        self.menu_button = Menubutton(self.date_objet, image=self.photo) # Menu avec différentes commandes
        self.menu_button.image = self.photo # On conserve la référence de l'image.
        self.menu_button.grid(row= 0, column = 0, padx = 5)
        self.menu_func=Menu(self.menu_button, bg='black', fg='white', bd=2, relief='ridge', font= 'Times 14')
        self.menu_func.add_command(label='Nouveau', underline = 0, command = lambda arg = self.note : self.notes(arg))
        self.menu_func.add_command(label='Ouvrir', underline = 0, command = self.show(self.note))
        self.menu_func.add_command(label='Enregistrer', underline = 0, command = lambda arg = self.note : self.save(arg))
        self.menu_func.add_command(label='Modifier', underline = 0, command = lambda arg = self.note_file : self.change(arg))
        self.menu_func.add_command(label='Supprimer', underline = 0, command = lambda arg1 = self.note_file, arg2 = self.note : self.remove(arg1, arg2))
        self.menu_func.add_command(label='Tout supprimer', underline = 0, command = lambda arg1 = self.note_file, arg2 = self.note : self.remove_all(arg1, arg2))
        self.menu_func.add_command(label='Quitter', underline = 0, command = self.note.quit)
        self.menu_button.configure(menu = self.menu_func)
       
        self.entry_date = Entry(self.date_objet, bg="yellow", font='Times 14 bold', width = 10, bd = 0, highlightthickness = 0) # Date de la note
        self.entry_date.grid(row = 0, column = 1, padx = 10)
       
        if self.d < 10 and self.m < 10 : # Formatage de la date : rajout d'un zéro lorsque le jour et/ou le mois sont inférieurs à 10.
            self.entry_date.insert(0, '0' + str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        elif self.d < 10 :
            self.entry_date.insert(0, '0' + str(self.d) + '/' + str(self.m) + '/' + str(self.y))
        elif self.m < 10 :
            self.entry_date.insert(0, str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        else :
            self.entry_date.insert(0, str(self.d) + '/' + str(self.m) + '/' + str(self.y))
       
        self.label_objet = Label(self.date_objet, text = "Objet : ", bg = "yellow", font = 'Times 14 bold', padx = 5)
        self.label_objet.grid(row =0, column = 2)
        self.entry_objet = Entry(self.date_objet, bg="white", font='Times 14', width = 33, bd = 1, disabledbackground = 'white', disabledforeground = 'black')
        self.entry_objet.grid(row = 0, column = 3)
        self.entry_objet.focus_set() # Le focus est dirigé vers le champ d'entrée de l'objet.
        self.entry_objet.bind('<Return>', self.focus_editor)
       
        self.editor = Text(self.note_frame, bg = "yellow", font='Times 14',  width = 60, height = 10, bd = 0, highlightthickness = 0, padx = 20, pady = 20)
        self.editor.grid(row = 1, column = 0, pady = 5)
       
        self.file = open(self.note_file, 'r')
        self.readfile = self.file.readlines()
        self.file.close()
        self.entry_objet.insert(0, self.readfile[0].strip())
        self.readfile[2:] = [self.readfile[2:][i].strip() for i, element in enumerate(self.readfile[2:])]
        i2 = 1.0
        for i, element in enumerate(self.readfile[2:]):
            self.editor.insert(i2, self.readfile[2:][i] + '\n')
            i2 += 1
        self.editor['state'] = 'disabled'
        self.entry_objet['state'] = 'disabled'
       
#----------------------------------------------------------------------------
       
    def change(self, note_file):
        "Modification d'une note"
        self.note_file = note_file
        self.numb_note = self.note_file[self.note_file.index('a')+1:self.note_file.index('b')] # Variable qui stocke le n° de la note à modifier.
        self.editor['state'] = 'normal' # Déverrouillage de ces deux widgets : écriture autorisée.
        self.entry_objet['state'] = 'normal'      
       
#----------------------------------------------------------------------------
 
    def remove(self, note_file, note) :
        "Suppression d'une note"
        self.note_file = note_file
        self.note = note
        os.remove(self.rep + '/' + self.note_file)
        self.notes(self.note)
        
        
    def remove_all(self, note_file, note) :
        "Suppression de toutes les notes"
        self.listdir = os.listdir(self.rep) # Liste de tous les fichiers contenus dans la chaîne de caractères passée en argument
        self.list_all_files = list()
        self.note = note
        for i, element in enumerate (self.listdir):
            self.string = os.path.splitext(self.listdir[i])[0]
            if self.string.endswith('note'):
                os.remove(self.rep + '/' + self.string)
        
    def destroy_widget(self, widget):
        "Icônification des Toplevel ou destruction des autres fenêtres"
        self.widget = widget
        if self.widget.winfo_class() == 'Toplevel' :
            self.widget.iconify()  
        else :
            self.widget.destroy()
#============================================================================
 
# PROGRAMME PRINCIPAL:
 
"""Instruction qui sert à déterminer si le module est lancé
  en tant que programme autonome (auquel cas les instructions qui suivent doivent être exécutées),
  ou au contraire utilisé comme une bibliothèque de classe importée ailleurs.
  Dans ce cas, cette partie de code est sans effet."""
     
if __name__ == "__main__":
 
    note = Notes() # Création de l'objet note par instanciation de la classe Notes.
    note.notes() # Appel de la méthode notes.