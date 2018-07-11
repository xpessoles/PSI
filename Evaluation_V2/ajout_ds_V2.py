#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

"""
Ajout des notes d'un DS à partir d'un fichier CSV.

"""
import sqlite3
import codecs
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter

file_csv = "Classeur1.csv"
file_bareme = "Bareme.csv"
bdd = "BDD_Evaluation.db"
num_ds = 1
annee = 2018


def lire_notes(file):
    """ Lire le fichier de notes sous la forme 
    IdEleve, Q1, Q2, Q3, ..., commentaire
    Retourne une liste de listes de la forme 
    [Id,[q1,q2,...],com]
    """
    
    fid = open(file,'r', encoding='utf-8-sig')
    
    # On récupère les notes
    data = fid.readlines()
    fid.close()
    notes = []
    for ligne in data :
        ligne = ligne.strip()
        ligne = ligne.split(";")
        id_eleve = ligne[0]
        commentaire = ligne[-1]
        ligne = ligne[1:-1]
        questions= [(i.replace(",",".")) for i in ligne]
        
        # typage des notes et des question non évaluées
        for i in range(len(questions)): 
        
            if questions[i]=="" or questions[i]=="n":
                questions[i] = "n"
            else :
                questions[i]=float(questions[i])
            
        eleve=[id_eleve,questions,commentaire]
        notes.append(eleve)
    
    return notes

def lire_bareme(file):
    """ Lire le fichier de barème"""
    
    # On récupère les infos du barème
    
    fid = open(file,'r', encoding='utf-8-sig')
    fid.readline() # La premiere ligne est inutile.
    bareme_q=fid.readline() # La seconde ligne contient le bareme par question
    total_q=fid.readline() # La troisième ligne donne le nombre de points alloués à la question
    data = fid.readlines()
    fid.close()
    nb_ques=0
    bareme = []
    
    for ligne in data :
        competence= []
        ligne = ligne.strip()
        ligne = ligne.split(";")
        # On supprime la première et la troisième colonne
        del ligne[2]
        del ligne[0]
        competence.append(ligne[0])
        for i in range(1,len(ligne)):
            if ligne[i]!="0":
                competence.append([i,float(ligne[i])])
        if len(competence)>1:
            bareme.append(competence)
            
        
        nb_ques=len(ligne)-1
    
    # BAREME comp : comp, poids DS
    bareme_comp=[]
    for ligne in bareme :
        comp = ligne[0]
        ligne = ligne[1:]
        q=0
        for l in ligne : 
           q=q+l[1]
        bareme_comp.append([comp,q])
      
        
    bareme_q = bareme_q.strip()
    bareme_q = bareme_q.split(";")
    bareme_q = bareme_q[3:]
    bareme_q = [float(x) for x in bareme_q]
    
    total_q = total_q.strip()
    total_q = total_q.split(";")
    total_q = total_q[3:]
    total_q = [float(x) for x in total_q]
    
    # Bareme final : 
    # [num_q, poids, nb_points [[comp1, %1],[comp2,%2]]...]
    bareme_final=[]
    for i in range(len(bareme_q)):
        bareme_final.append([i+1,bareme_q[i],total_q[i]])
    
    # Ajout des compétences par question
    for ligne in bareme:
        comp = ligne[0]
        quest = ligne[1:]
        cc = []
        for q in quest :
            num_q = q[0]-1 #Numérotation python
            poids = q[1]
            c = [comp,poids]
            cc.append(c)
        bareme_final[num_q].append(cc)
        
    #print(bareme_final)
    """    
    #On met les poids du bareme en %
    for i in range(len(bareme_final)) :
        poids = bareme_final[i][1]
        liste_comp=bareme_final[i][3:]
        for j in range(len(liste_comp)):
            bareme_final[i][j+3][1]=round(bareme_final[i][j+3][1]/poids,2)
    """
    
    #for b in bareme_final:
    #for b in bareme_comp:
    #    print(b)
    #print(bareme_final)
    return bareme_final,bareme_comp
    # Transposer une liste : 
    #list(map(list, zip(*baremeh)))


def calcul_note_eleve(notes_eleve,bareme,bareme_comp):
    id_eleve = notes_eleve[0]
    notes = notes_eleve[1]
    
    pts_eleve = 0
    total_pts = 0
    
    notes_comp = []
    
    for i in range(len(bareme)):
        comp = bareme[i][3]
        n = notes[i]
        poids = bareme[i][1]
        
        if n=='n':
            n=0
        note_q  = n/bareme[i][2]*poids
        pts_eleve += note_q
        total_pts += poids
        
        #print(comp)
        for c in comp :
            note_c = c[1]/poids
            notes_comp.append([c[0],round(note_c*note_q,0)])
    
    
    dico_comp_ini = dict(bareme_comp) 
    dico_comp = dict(bareme_comp) 
    
    #On vide le dictionnaire
    for clef in dico_comp :
        dico_comp[clef]=0
        
    #On remplit le dictionnaire
    for nc in notes_comp:
        clef = nc[0]
        val = nc[1]
        dico_comp[clef]=dico_comp[clef]+val
    
    # On met les valeurs du dico en pourcentage de réussite
    for clef in dico_comp:
        dico_comp[clef]=round(dico_comp[clef]/dico_comp_ini[clef],2)
    
    
    return [id_eleve,round(pts_eleve*20/total_pts,3),dico_comp]
    
promo = 2018
num_ds = 1

# Lecture du fichier de notes
notes_classe = lire_notes(file_csv)    
bareme,bareme_comp = lire_bareme(file_bareme)

"""
for notes_eleve in notes_classe : 
    calcul_note_eleve(notes_eleve,bareme,bareme)
"""
result_eleve = calcul_note_eleve(notes_classe[0],bareme,bareme_comp)

"""
[ideleve,note,rang,['comp',%]

"""





