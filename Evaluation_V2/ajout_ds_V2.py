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
    
    for ligne in bareme:
        comp = ligne[0]
        quest = ligne[1:]
        for q in quest :
            num_q = q[0]-1 #Numérotation python
            poids = q[1]
            c = [comp,poids]
            bareme_final[num_q].append(c)
    """    
    #On met les poids du bareme en %
    for i in range(len(bareme_final)) :
        poids = bareme_final[i][1]
        liste_comp=bareme_final[i][3:]
        for j in range(len(liste_comp)):
            bareme_final[i][j+3][1]=round(bareme_final[i][j+3][1]/poids,2)
    """
    
    for b in bareme_final :
        print(b)
    #print(bareme_final)
    return bareme_final
    # Transposer une liste : 
    #list(map(list, zip(*baremeh)))




promo = 2018
num_ds = 1

# Lecture du fichier de notes
notes_classe = lire_notes(file_csv)    
bareme = lire_bareme(file_bareme)

# Calcul des notes par élève et par compétence.







