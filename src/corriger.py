# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2

###donne de nos questions
class Question:
    def __init__(self, question,choices, correct):
        self.question = question
        self.choices = choices
        self.correct = correct
from collections import namedtuple
q = [None] * 10
Question = namedtuple("Question", "question choices correct")

q[0] = Question("Le premier reseau informatique est ne",["en 2000","en 1980","au debut des annees 60","aucune de ces reponses n'est correcte"],[3])
q[1] = Question("Quel est le cable utilise dans un reseau 10 Base T",["coaxial fin","paire torsadee","ondes hertziennes"],[2])
q[2] = Question("Dans un LAN Ethernet, le support",["n'est pas partage et les collisions n'existent pas.","est partage, les collisions existent et representent un phénomène anormal","est partage, les collisions existent et représentent un phenomene normal.","aucune de ces reponses n'est correcte"],[3])
q[3] = Question("Un réseau LAN peut relier Bruxelles et Londres :",["oui","non","parfois"],{2})
q[4] = Question("Un réseau LAN dépend d'un opérateur télécom pour fonctionner correctement :",["oui","non","parfois"],[3])
q[5] = Question("A chaque extremite d'un reseau 10 Base 2, il faut placer :",["une prise RJ45","un bouchon","une clé USB"],[2])
q[6] = Question("Avec une topologie physique en étoile, l'élément qui effectue une diffusion du signal s'appelle un :",["routeur","commutateur","concentrateur"],[3])
q[7] = Question("Dans une topologie physique en étoile, quel est l'élément qui permet d'envoyer une trame sur un port particulier :",["hub","commutateur","routeur"],[2])
q[8] = Question("Dans un réseau Ethernet, pendant l'émission d'une trame, un poste :",["reste inactif","continue l'écoute du signal","envoie une trame"],[2])
q[9] = Question("Une adresse IPv4 est composée de :",["6 octets","4 nombres compris entre 0 et 256","4 nombres compris entre 0 et 255"],[3])


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 100):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin,  cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        if len(cnt) == 4 and cv2.contourArea(cnt) > 50 and cv2.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
            if max_cos < 0.1:
                l1 = cnt[0] - cnt[1]
                #l2 = cnt[1] - cnt[2]
                if(abs(np.sqrt(np.dot(l1,l1))-13)< 3 ):

                    squares.append(cnt)
    return squares

def find_circles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 15,
                               param1=500,  # plus grand, le meilleur
                               param2=50,
                               minRadius=15,  # 15
                               maxRadius=20)  # 20
    circles = np.uint16(np.around(circles))
    return circles

img = cv2.imread('../images/scanner_jpg.jpg')
squares = find_squares(img)
circles = find_circles(img)
print( len(squares))
#print squares    # 95 squares total

#cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
#cv2.imshow('squares', img)
#k = cv2.waitKey(0)
#if k == 27:
#    cv2.destroyAllWindows()

img1 = cv2.imread('../images/scanner_jpg2.jpg')
squares1 = find_squares(img1)
circles1 = find_circles(img1)
print (len(squares1))
#cv2.drawContours( img1, squares1, -1, (0, 255, 0), 3 )
#cv2.imshow('squares1', img1)
#k = cv2.waitKey(0)
#if k == 27:
#    cv2.destroyAllWindows()


print (circles)
print (circles1)

def insertSort(a):
    liste = a
    for i in range(len(liste)-1):
        #print a,i
        for j in range(i+1,len(liste)):
            if liste[i]>liste[j]:
                temp = liste[i]
                liste[i] = liste[j]
                liste[j] = temp
    return liste
def circles_ordre(circles):
    liste = []
    circles_ordre = circles * 0
    print (circles)
    for i in range(len(circles[0])):
        liste.append(circles[0][i][0]+circles[0][i][1])
    #print liste
    liste_ordre = insertSort(liste)
    liste = []
    for i in range(len(circles[0])):
        liste.append(circles[0][i][0]+circles[0][i][1])
    print (liste)
    print (liste_ordre)
    for i in range(len(circles[0])):
        for j in range(len(circles[0])):
            if liste_ordre[i] == liste[j]:

                circles_ordre[0][i] = circles[0][j]
    return circles_ordre



circles = circles_ordre(circles)
circles1 = circles_ordre(circles1)

print (circles)
print (circles1)


#recalage

pts1 = np.float32([[circles[0][0][0],circles[0][0][1]],[circles[0][1][0],circles[0][1][1]],
                  [circles[0][2][0],circles[0][2][1]],[circles[0][3][0],circles[0][3][1]]])

pts2 = np.float32([[circles1[0][0][0],circles1[0][0][1]],[circles1[0][1][0],circles1[0][1][1]],
                  [circles1[0][2][0],circles1[0][2][1]],[circles1[0][3][0],circles1[0][3][1]]])

M = cv2.getPerspectiveTransform(pts2,pts1)
dst = cv2.warpPerspective(img1,M,(1240,1754))


squares1 = find_squares(dst)
print (len(squares1))
#print squares1

squares_choix = squares[0:25]
squares_numero = squares[25:]
#print len(squares_choix)
#print len(squares_numero)
#print squares_choix
#print squares_numero[0:7]
#methode mise en ordre bubble
def mise_ordre_squares(squares):
    squares_ordre =[]
    for num in range(10):
        squares_temp = squares[num*7:num*7+7]
        for passnum in range(len(squares_temp) - 1, 0, -1):
            # print alist,passnum
            for i in range(passnum):
                if squares_temp[i][0][0] > squares_temp[i + 1][0][0]:
                    temp = squares_temp[i]
                    squares_temp[i] = squares_temp[i + 1]
                    squares_temp[i + 1] = temp
        squares_ordre += squares_temp
    return squares_ordre

squares_numero = mise_ordre_squares(squares_numero)






# afficher les carres detecte
'''
cv2.drawContours( dst, squares, -1, (0, 255, 0), 3 )
cv2.imwrite( "resultat3.jpg", dst );
cv2.imshow('squares', dst)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
'''


print('###')
#print squares_choix[0][0]
#print img.shape
#print img[squares_choix[0][0][1],squares_choix[0][0][0]]

print('resultat')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)


def correlation_coefficient(patch1, patch2):
    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product
'''
#test de les moyennes et correlation
for i in range(25):
    compte = 0
    print('case %d'%(i))
    print('difference entre la moyenne')
    print np.mean(img[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]]) - np.mean(dst[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]])
    print('correlation_coefficent')
    cor = correlation_coefficient(img[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]],dst[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]])
    print cor
    #print  np.corrcoef(img[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]],dst[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]])[0,1]

    (m,n) = img[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]].shape
    for a in range(m):
        for b in range(n):
            if(img[a][b] == dst[a][b]):
                compte += 1
    print compte
'''

#print('###')
#print squares[1]
#print squares1[0]

difference_moyenne = []
for i in range(25):
    difference_moyenne.append(np.mean(img[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]]) - np.mean(dst[squares_choix[i][0][1]:squares_choix[i][1][1],squares_choix[i][0][0]:squares_choix[i][2][0]]))
print (difference_moyenne)
def decoder(difference_moyenne,seuil):
    for i in range(len(difference_moyenne)):
        if difference_moyenne[i] > seuil:
            difference_moyenne[i] = 1
        else:
            difference_moyenne[i] = 0
    return difference_moyenne
reponse_correcte = [1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0]
reponse =  decoder(difference_moyenne,20)

def resultat(reponse,reponse_correcte):
    compte = 0
    for i in range(len(reponse)):
        if(reponse[i] == reponse_correcte[i] == 1):
            compte +=1
    return compte

print ("note final %d/8"%(resultat(reponse,reponse_correcte)))




