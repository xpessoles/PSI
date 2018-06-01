#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

"""
Ajout des notes d'un DS à partir d'un fichier CSV.

"""
import sqlite3

file_csv = ".csv"
bdd = "BDD_evaluation.db"
num_ds = 1
annee = 2018

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
    fid.close()
    notes = []
    for ligne in data : 
        print(ligne)
        ligne = ligne.split(";")
        commentaire = ligne[nb_questions+1]
        ligne = ligne[:nb_questions+1]
        ligne = [(i.replace(",",".")) for i in ligne]
        ligne.append(commentaire)
        print(ligne)
        notes.append(ligne)
    
    return nb_questions, bareme, poids, notes, competences

def remplir_bdd(competences,nb_questions, bareme, poids, notes,bdd):
    #conn = sqlite3.connect(bdd)
    #c = conn.cursor()
    for eleve in notes : 
        #print(eleve)
        data = ""
        for item in eleve : 
            data = data+str(item)+","
        data = data[:-1]
        req = 'INSERT INTO ds VALUES ('+data+')'
        #print(req)
        #c.execute(req)
    #conn.commit()

#REMPLISSAGE BDD A FAIRE
nb_questions, bareme, poids, notes, competences = lire_fichier("Classeur1.csv")    

remplir_bdd(competences,nb_questions, bareme, poids, notes,"bdd")

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