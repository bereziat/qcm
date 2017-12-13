# -*- coding: utf-8 -*-
import numpy as np
import qrcode



class Question:
    def __init__(self, question,choices, correct):
        self.question = question
        self.choices = choices
        self.correct = correct
from collections import namedtuple
q = [None] * 10
Question = namedtuple("Question", "question choices correct")
#q[0]= Question("What is 1 + 1",[1,2,3,4], {"b"})
#for i in range(40):
#   q[i] = Question("What is 1 + 1",[1,2,3,4], {2})
#print q[1].question
#print q[1].correct
#print len(q[1].choices)
q[0] = Question("Le premier reseau informatique est ne",["en 2000","en 1980","au debut des annees 60","aucune de ces reponses n'est correcte"],[3])
q[1] = Question("Quel est le cable utilise dans un reseau 10 Base T",["coaxial fin","paire torsadee","ondes hertziennes"],[2])
q[2] = Question("Dans un LAN Ethernet, le support",["n'est pas partage et les collisions n'existent pas.","est partage, les collisions existent et representent un phénomène anormal","est partage, les collisions existent et représentent un phenomene normal.","aucune de ces reponses n'est correcte"],[3])
q[3] = Question("Un reseau LAN peut relier Bruxelles et Londres :",["oui","non","parfois"],{2})
q[4] = Question("Un reseau LAN dépend d'un opérateur télécom pour fonctionner correctement :",["oui","non","parfois"],[3])
q[5] = Question("A chaque extremite d'un reseau 10 Base 2, il faut placer :",["une prise RJ45","un bouchon","une clé USB"],[2])
q[6] = Question("Avec une topologie physique en etoile, l'élément qui effectue une diffusion du signal s'appelle un :",["routeur","commutateur","concentrateur"],[3])
q[7] = Question("Dans une topologie physique en etoile, quel est l'élément qui permet d'envoyer une trame sur un port particulier :",["hub","commutateur","routeur"],[2])
q[8] = Question("Dans un reseau Ethernet, pendant l'émission d'une trame, un poste :",["reste inactif","continue l'écoute du signal","envoie une trame"],[2])
q[9] = Question("Une adresse IPv4 est composee de :",["6 octets","4 nombres compris entre 0 et 256","4 nombres compris entre 0 et 255"],[3])




# add a QRcode and size it
qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
        )
qr.add_data("1")
qr.make(fit=True)
img = qr.make_image()
img.save("copie1.png")

f = open("exemple.tex","w")
#package

f.write("\\documentclass[a4paper]{exam}\n")
f.write("\\usepackage[french]{babel}\n")
f.write("\\usepackage{tikz}\n\\usepackage{graphicx}\n\\usetikzlibrary{shadings}\n\\usepackage{amssymb}\n")

#head et foot
f.write("\\rhead{\\tikz{\draw[fill=black,line width=1pt]  circle(2ex);}}\n\lhead{\\tikz{\draw[fill=black,line width=1pt]  circle(2ex);}}\n")
f.write("\\rfoot{\\tikz{\draw[fill=black,line width=1pt]  circle(2ex);}}\n\lfoot{\\tikz{\draw[fill=black,line width=1pt]  circle(2ex);}}\n")
f.write("\\chead{ \\includegraphics[width=0.1\\textwidth,height=10mm]{copie1.png}}\n")
f.write("\\begin{document}\n")
f.write("numero d'etudiant\\newline\n")
for i in range(10):
    for j in range(6):
        f.write("\\tikz{\draw[fill=none,line width=1pt]  rectangle(2ex,2 ex);}\n")
    f.write("\\tikz{\draw[fill=none,line width=1pt]  rectangle(2ex,2 ex);} %d\\newline\n" %(i))
f.write("\\begin{tikzpicture}\n")
f.write("\\node[draw,text width=6cm] at (20,-20) {Nom et prenom\\vspace{5mm} };\n")
f.write("\end{tikzpicture}\\newline\n")
f.write("\\tikz{\draw (0,0) -- (15,0);}\\newline\n")

for i in range(10):
    f.write("\\textbf{Question %d} $\\blacklozenge$ %s\\newline\n"%(i+1,q[i].question))
    for j in range(len(q[i].choices)):
        f.write("\\tikz{\draw[fill=none,line width=1pt]  rectangle(2ex,2 ex);} ")
        f.write("%s\\newline"%(q[i].choices[j]))
    f.write("\\newline")
f.write("\end{document}\n")


f.close()



### brew install zbar
### sudo apt-get install zbar


import subprocess
def decoderQRcode(file):
    mycommand = subprocess.Popen(["zbarimg", file],stdout=subprocess.PIPE)
    (out, err) = mycommand.communicate()

    qr_code = None

    # out looks like "QR-code: Xuz213asdY" so you need
    # to remove first 8 characters plus whitespaces
    if len(out) > 8:
        qr_code = out[8:].strip()
    return int(qr_code)

print (decoderQRcode("copie1.png"))



import os

os.system("pdflatex exemple.tex")
os.system("convert exemple.pdf sujet.jpg")
