#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

"""
Ajout des notes d'un DS à partir d'un fichier CSV.

"""
import sqlite3

file_csv = "Classeur1.csv"
bdd = "BDD_Evaluation.db"
num_ds = 1
annee = 2018

import os

def lire_fichier(file):
    fid = open(file,'r', encoding='utf-8-sig')
    
    # Premiere ligne numéro de questions
    ligne = fid.readline()
    ligne = ligne.split(";")
    nb_questions = int(ligne[0])
    
    # Seconde ligne : bareme
    ligne = fid.readline()
    ligne = ligne.split(";")
    ligne = ligne[1:nb_questions+1]
    bareme = [float(i.replace(",",".")) for i in ligne]
    
    # Troisième ligne : poids 
    ligne = fid.readline()
    ligne = ligne.split(";")
    ligne = ligne[1:nb_questions+1]
    poids = [float(i.replace(",",".")) for i in ligne]
    
    
    # Quatrième ligne poids/20 de la question ; on saute. 
    ligne = fid.readline()
    
    # Cinquième ligne compétences
    ligne = fid.readline()
    ligne = ligne.split(";")
    competences = ligne[1:nb_questions+1]
    
    
    # Ensuite, on récupère les notes
    data = fid.readlines()
    #print(data)
    fid.close()
    notes = []
    for ligne in data : 
        #print(ligne)
        ligne = ligne.split(";")
        commentaire = ligne[nb_questions+1]
        ligne = ligne[:nb_questions+1]
        ligne = [(i.replace(",",".")) for i in ligne]
        ligne.append(commentaire)
        notes.append(ligne)
    
    return nb_questions, bareme, poids, notes, competences

def remplir_bdd(num_ds,annee,competences,nb_questions, bareme, poids, notes,bdd):
    #print(os.getcwd())
    #print(os.listdir())
    #bdd="BDD_Evaluation.db"
   
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    
    for eleve in notes : 
        #print(eleve)
        data = ""
        id_eleve = int(eleve[0])
        print("EleveID", id_eleve)
        
        for i in range (1,nb_questions+1):
            data = str(id_eleve)+','+str(num_ds)+','
            data = data + str(annee)+','
            data = data + str(nb_questions)+','
            data = data + str(i)+','
            data = data + str(poids[i-1])+','
            data = data + str(bareme[i-1])+',"'
            data = data + str(eleve[i])+'","'
            data = data + str(competences[i-1])+'","'
            data = data + str(eleve[nb_questions+1])+'"'
            req = 'INSERT INTO ds VALUES ('+data+')'
            #print(req)
            
            
            c.execute(req)
    conn.commit()
    conn.close()

def bilan_ds(num_ds):
    # On récupère pour chaque eleve : num_question, poids, bareme, note, id_competence
        
    


nb_questions, bareme, poids, notes, competences = lire_fichier("file_csv")    
remplir_bdd(num_ds,annee,competences,nb_questions, bareme, poids, notes,bdd)
bilan_ds(num_ds)


"""
(
	`id_eleve`	INTEGER,
	`num_ds`	INTEGER,
	`annee`	INTEGER,
	`nb_questions`	INTEGER,
	`num_question`	INTEGER,
	`poids`	INTEGER,
	`bareme`	INTEGER,
	`note`	INTEGER,
	`id_competence`	INTEGER,
	`commentaire`	INTEGER
);
"""

"""
conn = sqlite3.connect('example.db')
You can also supply the special name :memory: to create a database in RAM.

Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL commands:

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
"""