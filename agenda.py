
import os
import os.path
from tkinter import* 
from PIL import Image, ImageTk
import tkinter.messagebox
from calendar import monthcalendar 
from calendar import Calendar 
from time import localtime 
from datetime import time, datetime


class Agenda(object) :
    "Instanciation de l'agenda"
    
    dico = {}
    
    def __init__(self, d = localtime()[2], m = localtime()[1], y = localtime()[0]):
        "Méthode constructeur"
        
        self.directory = os.getcwd()
            
        self.d = d
        self.m = m
        self.y = y


    def pages(self, previous_page = None) :
        "Création des pages"
        
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = 'green'
        
        if previous_page != None : # Destruction de la page précédemment consultée 
            previous_page.destroy()
        self.page = Tk()
        self.page.title('Mon agenda')

        self.frame = Frame(self.page, bg = 'white')
        self.frame.grid()

        self.buttons = Frame(self.frame, bg = 'white')
        self.buttons.grid(row = 0, column = 0, sticky = 'w')

        subframe = Frame(self.frame, bg = 'white', relief = 'groove', bd = 1, padx = 170)
        subframe.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew')

        button_list = list()
        textes = ['Enregistrer', 'Valider', 'Effacer']
        for i, element in enumerate(textes):
            self.button = Button(self.buttons, text = element, bg = self.read_color, fg = 'white',\
                          activebackground = 'white', activeforeground = self.read_color)
            self.button.grid(row = 0, column = i)
            button_list.append(self.button)

        search_labelframe = LabelFrame(self.buttons, bd = 1, highlightthickness = 0,\
                                 bg = 'white')
        search_labelframe.grid(row = 0, column = 4)


        image_loupe = self.directory + "/images/loupe.png"
        image = Image.open(image_loupe)
        size = 32, 32 
        image.thumbnail(size)
        self.photo = ImageTk.PhotoImage(image, master = self.page)

        find = Actions()

        search_entry = Entry(search_labelframe, fg = self.read_color, font = 'Times 12 bold',\
                       border = 0, highlightthickness = 0)
        search_entry.grid(row = 0, column = 0)
        search_entry.insert(0, "Rechercher")
        search_entry.bind('<Button-1>', lambda event: self.delete(search_entry))
        search_entry.bind('<Return>', lambda event: find.search(search_entry))

        # Création du bouton "loupe" :
        
        search = Button(search_labelframe, image = self.photo, bd = 0, highlightthickness = 0,\
                 command = lambda : find.search(search_entry))
        search.grid(row = 0, column = 1)

        # Création du triangle de changement de date (vers le futur):
        
        next_day = Actions(int(self.d)+1, self.m, self.y)
        right_triangle = Button(subframe, bg = 'white', fg = self.read_color,\
                              text = u"\u25B6", bd = 0, highlightthickness = 0,\
                              padx = 0, pady = 0, activebackground = self.read_color,\
                              activeforeground = 'white')
        right_triangle.grid(row = 0, column = 2, padx = 10, sticky = 'e')
        right_triangle['command'] = lambda : next_day.next_day(self.page)

        if int(self.d) < 10 and self.m < 10 :
            date = Label(subframe, bg = 'white', fg = self.read_color,\
                        bd=0, font = 'Times 18 bold', text = '0' + str(self.d) +\
                        '/' + '0' + str(self.m) + '/' + str(self.y))
        elif int(self.d) < 10 :
            date = Label(subframe, bg = 'white', fg = self.read_color, bd = 0,\
                        font = 'Times 18 bold', text = '0' + str(self.d) +\
                        '/' + str(self.m) + '/' + str(self.y))
        elif self.m < 10 :
            date = Label(subframe, bg = 'white', fg = self.read_color, bd = 0,\
                        font = 'Times 18 bold', text = str(self.d) +\
                        '/' + '0' + str(self.m) + '/' + str(self.y))
        else :
            date = Label(subframe, bg = 'white', fg = self.read_color, bd = 0,\
                        font = 'Times 18 bold', text = str(self.d) +\
                        '/' + str(self.m) + '/' + str(self.y))
        date.grid(row = 0, column = 1, sticky = 'nsew')

        # Création du triangle de changement de date (vers le passé):
        
        previous_day = Actions(int(self.d)-1, self.m, self.y)
        left_triangle = Button(subframe, bg = 'white', fg = self.read_color,\
                             text = u"\u25C0", bd = 0, highlightthickness = 0,\
                             padx = 0, pady = 0, activebackground = self.read_color,\
                             activeforeground = 'white')
        left_triangle.grid(row = 0, column = 0, padx = 10, sticky = 'w')
        left_triangle['command'] = lambda : previous_day.previous_day(self.page)

        # Jour en cours. Remplacement des slashes par des tirets bas:
        
        current_date = date['text'].replace('/', '_')

        # Création des pages de l'agenda
        
        subframe2_list = list()
        hour_list = []
        for i in range(7,22):
            subframe2 = Frame(self.frame, bg = 'white')
            subframe2.grid(row = i-5, column = 0, sticky = 'nsew')
            subframe2_list.append(subframe2)
            if i < 10 : # Création des étiquettes affichant les heures de la journée.
                label = Label(subframe2, fg = 'white', bg = self.read_color, padx = 5, pady = 2,\
                        font = 'bold', text = '  ' + str(i) + u"\u2070\u2070")
            else :
                label = Label(subframe2, fg = 'white', bg = self.read_color, padx = 5, pady = 2,\
                        font = 'bold', text = str(i) + u"\u2070\u2070")
            label.grid(row = 0, column = 0, sticky = 'nsew')    
            
            # Création des entrées pour chaque heure de la journée :
            
            hour = Text(subframe2, bg = 'white', fg = 'black', font = 'Times 14',\
                   highlightthickness = 0, bd = 1, selectbackground = 'blue',\
                   selectforeground = 'white', wrap = 'word', width = 50, height = 1,\
                   padx = 10, pady = 2)
            hour.grid(row = 0, column = 1, sticky = 'nsew')
            hour_list.append(hour)

        # Affichage les différentes entrées de la page appelée.
        
        action_affichage = Actions(self.d, self.m, self.y, current_date, hour_list)
        action_affichage.entries(self.page) 
        save = Actions(self.d, self.m, self.y, current_date)
        validation = Actions(self.d, self.m, self.y, current_date)
        erase = Actions(self.d, self.m, self.y, current_date)
        button_list[0]['command'] = lambda : save.save(subframe2_list)
        button_list[1]['command'] = lambda : validation.validation(subframe2_list, self.page)
        button_list[2]['command'] = lambda : erase.erase(subframe2_list, self.page)
    
        # Message qui apparait sous la forme d'une fenêtre pop-up dans le cas où une entrée 
        #n'a pas été traitée ni validée. Le message contient la date et le texte de l'entrée :
        
        file_ = open('validated','a')
        file_.close()
        with open('validated','r') as file_:
            readfile2 = file_.readlines()
            readfile = []
            for i in range(0, len(readfile2)):
                readfile.append(readfile2[i].strip())
        filelist = open('entrylist', 'a')
        filelist.close()
        with open('entrylist', 'r') as filelist:
            readfilelist = filelist.readline()
        readfilelist = readfilelist.split(',')
        readfilelist = readfilelist[:-1]
        for i, x in enumerate(readfilelist):
            x = x.replace("entrees_agenda/", "")
            readfilelist[i] = x
        for x in readfilelist:
            if x not in Agenda.dico :
                Agenda.dico[x] = 0
                index = Agenda.dico[x]
            else:
                Agenda.dico[x] = 1
                index = Agenda.dico[x]
            x = x.split('-')
            for y, element in enumerate(x):
                x[y] = x[y].split('_')
            if x[0] == '':
                x[0] = []
            self.duration = datetime.now() - datetime(int(x[0][2]), int(x[0][1]), int(x[0][0]))
            x[0] = '_'.join(x[0])
            x[1] = ''.join(x[1])
            x = '-'.join(x)
            x = "entrees_agenda/" + x
            if self.duration.days > 1 and x not in readfile :
                while index < 1 :
                    with open(x, 'r') as file_:
                        readfile = file_.readline()
                    x = x.replace("_", "/")
                    index_tiret = x.index('-')
                    x = x[:index_tiret]
                    tkinter.messagebox.showwarning(x.replace\
                    ("entrees/agenda/", ""), x.replace("entrees/agenda/", "")\
                    + '\n\n' + readfile)
                    index += 1
                    Agenda.dico[x] = 1

        self.page.mainloop()
                                
                                
    def delete(self, search_entry):
        "Efface le champ d'entrée 'recherche'"
    
        if search_entry.get() == "Rechercher":
            search_entry.delete(0, 'end')


class Actions(Agenda) :
    "Actions enregister, effacer, valider..."
    
    def __init__(self, d = localtime()[2], m = localtime()[1], y = localtime()[0],\
    current_date = [], hour_list = []) :
        "Constructeur"
        
        Agenda.__init__(self)
        self.d = d
        self.m = m
        self.y = y
        self.current_date = current_date
        self.hour_list = hour_list
        
        self.directory = os.getcwd()

        
        # Couleur:

        with open("file_color", 'r') as file_color:
            self.read_color = file_color.readline()
            if self.read_color == None:
                self.read_color = 'green'

    def previous_day(self, page) :
        "Conditions à remplir pour reculer d'un jour"
        
        if self.d < 1 :
            self.m -=1
            if self.m == 0 :
                self.m = 12
                self.y -= 1
            self.c = monthcalendar(self.y, self.m)
            self.d = max(max(self.c))
        self.pages(page)
        
    def next_day(self, page) :
        "Conditions à remplir pour avancer d'un jour"
        c = monthcalendar(self.y, self.m) 
        if self.d > max(max(c)):  
            self.d = '1'
            self.m += 1
            if self.m > 12 :
                self.m = 1
                self.y += 1
        self.pages(page)


    def save(self, subframe2_list):
        "Enregistrement des entrées"

        file_ = None
        for i in range(0, len(subframe2_list)) :
            for child in subframe2_list[i].winfo_children():
                if child.winfo_class() == "Text":
                    get_text = child.get(1.0, 'end')
                    filename = "entrees_agenda/" + str(self.current_date) + '-' + str(i)
                    if len(get_text) > 1 :
                        with open(filename, 'w') as file_:
                            file_.write(get_text)
                        with open('entrylist', 'r') as filelist:
                            readfilelist = filelist.readline()
                        readfilelist = readfilelist.strip() + filename + ','
                        readfilelist.replace('\n','')
                        with open('entrylist', 'w') as filelist:
                            filelist.write(readfilelist)
                        readfilelist = readfilelist.split(',')
                        readfilelist2 = []
                        for x in readfilelist :
                            if x not in readfilelist2 :
                                readfilelist2.append(x)
                            if x == '' :
                                del x
                        readfilelist2 = ",".join(readfilelist2)
                        with open('entrylist', 'w') as filelist:
                            filelist.write(readfilelist2)
                        filelist.close()
                    if child['bg'] == self.read_color and child['fg'] == 'white' :
                        self.green(i, filename)
        tkinter.messagebox.showinfo('Enregistrement', 'Les modifications ont été enregistrées')


    def entries(self, page) :
        "Affichage des entrées de la page consultée"
        
        with open('entrylist', 'r') as filelist:
            readfilelist = filelist.readline().split(',')
        for i, x in enumerate(readfilelist):
            readfilelist[i: i + 1] = [x.replace("entrees_agenda/", "").split('-')]
        readfilelist = readfilelist[:-1]
        for x in readfilelist:
            filename = "entrees_agenda/" + str(self.current_date) + '-' + x[1]
            if "entrees_agenda/" + '-'.join(x) == filename :
                with open(filename, 'r') as file_:
                    readfile = file_.readline()
                    self.hour_list[int(x[1])].delete(1.0, 'end')
                    readfile = readfile.strip()
                    self.hour_list[int(x[1])].insert('end', readfile)
        with open('validated', 'r') as validated:
            read_validated = validated.readlines()
        for i, x in enumerate(read_validated):
            read_validated[i:i + 1] = [x.replace("entres_agenda/", "")]
        read_validated_2 = []
        for x in read_validated :
            if x not in read_validated_2 :
                read_validated_2.append(x)
        with open('validated', 'w') as validated:
            for x in read_validated_2 :
                validated.write(x)
        for i, x in enumerate(read_validated_2):
            read_validated_2[i:i + 1] = [x.split('-')]
            if read_validated_2[i][0].replace("entrees_agenda/","") == self.current_date :
                self.hour_list[int(read_validated_2[i][1].strip())].config(bg = self.read_color, fg = 'white')
                

    def validation(self, subframe2_list, page):
        "Validation des entrées traitées (Rendez-vous honorés etc...)"
        
        try:
            validated_entry = page.focus_get()
        except:
            tkinter.messagebox.showwarning('Validation', 'Aucun contenu à valider')
        else:
            if validated_entry.winfo_class() == "Text" and\
            validated_entry.get(1.0, 'end').strip() != '':
                validated_entry.config(bg = self.read_color, fg = 'white')
                self.save(subframe2_list)
            else:
                tkinter.messagebox.showwarning('Validation', 'Aucun contenu à valider')
                        

    def green(self, i, filename) :
        "Stockage des pages validées dans un fichier"
        
        with open('validated', 'a') as validated:
            validated.write(filename + '\n')
        
         
    def erase(self, subframe2_list, page):
        "Effacement des entrées"
        
        get_entry = page.focus_get()
        confirm_erase = tkinter.messagebox.askquestion('Effacer?',\
                        'Voulez-vous vraiment supprimer cet événement?')
        if confirm_erase == 'yes':
            get_entry.delete(1.0, 'end')
            get_entry.config(bg='white', fg='black')
            filename = ''
            for i  in range(0, len(subframe2_list)) :
                for child in subframe2_list[i].winfo_children():
                    if child == get_entry:
                        filename = "entrees_agenda/" + str(self.current_date) + '-' + str(i)
            with open('validated', 'r') as validated:
                read_validated = validated.readlines()
            if filename + '\n' in read_validated :
                read_validated.remove(filename + '\n')
            with open('validated', 'w') as validated:
                for i in range(0, len(read_validated)):
                    validated.write(read_validated[i])
            with open('entrylist', 'r') as filelist:
                readfilelist = filelist.readline().split(',')
                if filename in readfilelist :
                    readfilelist.remove(filename)
                readfilelist = ','.join(readfilelist)
            with open('entrylist', 'w') as filelist:
                filelist.write(readfilelist)
            try:
                os.remove(self.directory + "/" + filename)
            except:
                tkinter.messagebox.showwarning("Aucun contenu", "Aucun contenu à effacer.")

    
    def search(self, search_entry):
        "Méthode qui cherche une chaîne de caractères dans les fichiers"

        search_string = search_entry.get().lower()
        if search_string == '':
            tkinter.messagebox.showwarning('Votre recherche', 'Entrez votre recherche.')
        else:
            listdir_ = os.listdir(self.directory + "/entrees_agenda/")
            list_all_files = list()
            for i in listdir_ :
                list_all_files.append(i)
            in_page = Toplevel(bg = 'white', padx=10, pady=10)
            in_page.title('Votre recherche')
            label = Label(in_page, bg = 'white', text = 'Les pages suivantes' + '\n' +\
                    'contiennent votre recherche', fg = 'black', font='Times 18 bold')
            label.grid(row=0, column = 0, columnspan = 4, pady = 10)
            i2 = 1 # variable d'incrémentation de la ligne dans le Toplevel 
            i3 = 0 # variable d'incrémentation de la colonne dans le Toplevel
            for i in list_all_files:
                with open("entrees_agenda/" + i, 'r') as file_:
                    readfile = file_.readline().lower()
                if readfile.find(search_string) != -1:
                    filename = os.path.splitext(i)
                    self.d = int(filename[0][:2])
                    self.m = int(filename[0][3:5])
                    self.y = int(filename[0][6:10])
                    
                    # Création du bouton ouvrant la page ou se trouve l'occurrence :
                    
                    button_page = Button(in_page, bg = self.read_color, fg = 'white',\
                                  text = filename[0][:10].replace('_','/'))
                    button_page.grid(row = i2, column = i3, sticky = 'w')
                    show_page = Agenda(self.d, self.m, self.y) 
                    show_page.pages
                    button_page.config(command = show_page.pages)
                    i3 += 1
                    if i3 % 4 == 0:
                        i2 += 1
                        i3 = 0
            if len(in_page.winfo_children()) == 1 :
                label.config(bg='red', fg='white', text='Aucun résultat', padx = 50)
                
#========= MAIN PROGRAMM ======================================================

if __name__ == "__main__":

    agenda = Agenda()
    agenda.pages()