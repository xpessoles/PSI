#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

""" 
Ajout des élèves dans la BDD à partir d'un fichier csv de la forme :
nom, prenom, date de naissance, adresse mail
"""

import codecs
import sqlite3

file_csv = "Competences_PCSI_PSI.csv"
#bdd = "BDD_Evaluation.db"
bdd = "PSI_2020_2021.db"

def lire_fichier(file,bdd):
    fid = open(file,'r', encoding='utf-8-sig')

    # On vide la table
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    c.execute("DELETE FROM table_competences")
    conn.commit()
    conn.close()  
    
    
    for line in fid :
        conn = sqlite3.connect(bdd)
        c = conn.cursor()
        #print(line)
        line=line.strip()
        line = line.split(";")
        if len(line)==5 :
            classe,id,long,court,sem = line
        else :
            print(len(line),line)
        print(id)
        req = 'INSERT INTO table_competences (id_competence,nom_long,nom_court,semestre,classe) VALUES ("'+id+'","' +long+'","' +court+'",' +sem+', "'+classe+'" )'
        print(req)
        c.execute(req)
        conn.commit()
        conn.close()    
    
    fid.close()
    
lire_fichier(file_csv,bdd)