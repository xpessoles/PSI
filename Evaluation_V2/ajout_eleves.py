#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

""" 
Ajout des élèves dans la BDD à partir d'un fichier csv de la forme :
nom, prenom, date de naissance, adresse mail
"""


import sqlite3

file_csv = "Eleve.csv"
bdd = "BDD_Evaluation.db"
def lire_fichier(file,bdd):
    fid = open(file,'r', encoding='utf-8-sig')
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    id=1
    for line in fid :
        line=line.strip()
        line = line.split(";")
        nom,prenom,date,lycee_bac,annee,ecole,job,mail = line
        req = 'INSERT INTO eleves VALUES ('+str(id)+',"'+nom+'","' +prenom+'","' +date+'","' +lycee_bac+'","' +annee+'","' +ecole+'","' +job+'","' +mail+'")'
        id=id+1
        c.execute(req)
        
        
    conn.commit()
    conn.close()    

lire_fichier(file_csv,bdd)