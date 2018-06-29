#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

""" 
Ajout des élèves dans la BDD à partir d'un fichier csv de la forme :
nom, prenom, date de naissance, adresse mail
"""


import sqlite3

file_csv = "Competences_PSI.csv"
bdd = "BDD_Evaluation.db"

def lire_fichier(file,bdd):
    fid = open(file,'r')
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    id=1
    for line in fid :
        print(line)
        line=line.strip()
        line = line.split(";")
        id,sem,long,court = line
        req = 'INSERT INTO table_competences ("'+id+'","' +long+'","' +court+'","' +sem+'")'
        print(req)
        c.execute(req)
        
    fid.close()
    conn.commit()
    conn.close()    

lire_fichier(file_csv,bdd)