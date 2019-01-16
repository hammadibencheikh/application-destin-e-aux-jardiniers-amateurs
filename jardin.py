
from mon_jardin.accueil import Home
import os

dir_ = os.getcwd()
with open(dir_ + "/jardin.desktop", 'r') as file_:
    readfile = file_.readlines()
    for i in readfile:
        if i.startswith("Exec"):
            readfile[readfile.index(i)] = "Exec=./jardin.py\n"
        if i.startswith("Icon"):
            readfile[readfile.index(i)] = "Icon=" + dir_ + "/images/mon_jardin.png\n"
with open(dir_ + "/jardin.desktop", 'w') as file_:
    for i in readfile:
        file_.write(i)

home = Home()
home.home()