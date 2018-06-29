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
    c.execute("DELETE FROM table_competences")
    conn.commit()
    conn.close()  
    
    id=1
    for line in fid :
        conn = sqlite3.connect(bdd)
        c = conn.cursor()
        #print(line)
        line=line.strip()
        line = line.split(";")
        if len(line)==4 :
            id,sem,long,court = line
        else : 
            id,sem,long= line
            court  = long
        req = 'INSERT INTO table_competences VALUES ("'+id+'","' +long+'","' +court+'",' +sem+')'
        #print(req)
        c.execute(req)
        conn.commit()
        conn.close()    
    
    fid.close()
    
lire_fichier(file_csv,bdd)