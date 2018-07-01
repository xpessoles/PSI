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
            print(req)
            
            
            c.execute(req)
    conn.commit()
    conn.close()

def bilan_ds(num_ds,bdd,promo):
    # On récupère le num de chaque élève
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    req = "SELECT id_eleve FROM eleves WHERE annee_integration="+str(promo)
    c.execute(req)
    tab = c.fetchall()
    id_eleves=[tab[i][0] for i in range(len(tab))]
    conn.commit()
    conn.close()
    
    res=[]
    for id in id_eleves :
        # On récupère pour chaque eleve : num_question, poids, bareme, note, id_competence
        conn = sqlite3.connect(bdd)
        c = conn.cursor()
        req = "SELECT num_question, poids, bareme, note, commentaire, id_competence FROM ds WHERE id_eleve="+str(id)+" AND num_ds="+str(num_ds)
        c.execute(req)
        tab = c.fetchall()
        conn.commit()
        conn.close()
        res.append(tab)
        
    notes = []
    
    i=0 
    #On convertit les tuples en liste et on ajoute les id eleves.
    for el in res :
        eleve = []
        for qq in el :
            questions = []
            questions.append(id_eleves[i])
            for q in qq :
                questions.append(q)
                # On ajoute la compétence courte et longue.
            conn = sqlite3.connect(bdd)
            c = conn.cursor()
            code_comp = questions[-1]
            req = 'SELECT nom_long,nom_court FROM table_competences WHERE id_competence="'+code_comp+'"'
            #print(req)
            c.execute(req)
            res = c.fetchall()
            conn.commit()
            conn.close()
            questions.append(res[0][0])    
            questions.append(res[0][1])
                
            eleve.append(questions)
        notes.append(eleve)
        i+=1
    
        
        """
        # On calcule la note :
        note_gl = 0
        note_el = 0 
        for q in tab :
            
            note_gl += q[1]*q[2]
            note = q[3]
            if q[3]=="n" or q[3]=="":
                note = 0
            #print(note_el,type(q[2]),type(note),note)
            note_el = note_el+ q[2]*note
        notes.append([id,note_el,note_gl,note_el*20/note_gl])
        """

    
    
    return notes


def stat_classe(notes):
    """ Calcul de la note et du rang de chaque eleve"""
    bilan = []
    for eleve in notes :
        id = eleve[0][0]
        note_gl = 0
        note_el = 0
        for note in eleve :
            note_gl += note[2]*note[3]
            n = note[4]
            if note[4]=="n" or note[4]=="":
                n = 0
            #print(note_el,type(q[2]),type(note),note)
            note_el = note_el+ note[3]*n
        bilan.append([note_el,id,note_gl])
        
    bilan.sort()
    i=1
    # On ajoute le classement
    for b in bilan:
        b.append(i)
        i+=1
    
    #On retrie dans l'ordre des identifiants
    for b in bilan:
        b[0],b[1]=b[1],b[0]
    bilan.sort()
    
    # On rajoute le nom et le prénom
    for b in bilan : 
        id = b[0]
        conn = sqlite3.connect(bdd)
        c = conn.cursor()
        req = 'SELECT nom,prenom FROM eleves WHERE id_eleve="'+str(id)+'"'
        #print(req)
        c.execute(req)
        res = c.fetchall()
        conn.commit()
        conn.close()
        b.append(res[0][0])
        b.append(res[0][1])


    return bilan
    
    
promo = 2018
num_ds = 1

def ecriture_notes_tex(notes,bilan,file):
    el = notes[0][0]
    # On compte le nombre de lignes de notes :
    nb_ques = len(notes)
    nb_lignes = nb_ques//4+1

    file_el = file+str(el)+".tex"
    fid = open(file_el,'w')
    
    
    # ===== NOTES PAR QUESTIONS =====
    # On ajoute les notes par questions
    fid.write("\\footnotesize \n")
    fid.write("\\begin{center} \n")
    fid.write("\\begin{tabular}{|c|c|c|c||c|c|c|c||c|c|c|c||c|c|c|c|} \n")
    for i in range (0,nb_lignes):
        c1 = i
        c2 = nb_lignes+i
        c3 = 2*nb_lignes+i
        c4 = 3*nb_lignes+i
        ligne = ""
        
        # 1 : num, 3 : note, 6 : comp, 4 : note/5
        ligne = ligne+str(notes[c1][1])+" & "+str(notes[c1][3])+" & "+str(notes[c1][6])+" & "+str(notes[c1][4])
        ligne = ligne+" & "+str(notes[c2][1])+" & "+str(notes[c2][3])+" & "+str(notes[c2][6])+" & "+str(notes[c2][4])
        ligne = ligne+" & "+str(notes[c3][1])+" & "+str(notes[c3][3])+" & "+str(notes[c3][6])+" & "+str(notes[c3][4])
        if c4 < nb_ques :
            ligne = ligne+" & "+str(notes[c4][1])+" & "+str(notes[c4][3])+" & "+str(notes[c4][6])+" & "+str(notes[c4][4])+" \\\ "
        else : 
            ligne = ligne+" & "+" & "+" & "+" & "+" \\\ "
        fid.write(ligne)
        fid.write('\n')
    
    fid.write("\\end{tabular} \n")
    fid.write("\\end{center} \n")
    fid.write("\\normalsize \n")
    # ===== FIN NOTES PAR QUESTIONS =====
    
    # ===== NOTES PAR COMPETECNES =====
    
    
    
    
    
    fid.close()    
            
"""
    1    10    19    28
    2    11    20    29
    3    12    21    30
    4    13    22    31
    5    14    23    32
    6    15    24    33
    7    16    25
    8    17    26
    9    18    27
"""    
    
    
#nb_questions, bareme, poids, notes, competences = lire_fichier(file_csv)    
#remplir_bdd(num_ds,annee,competences,nb_questions, bareme, poids, notes,bdd)
file  = "f"
notes = bilan_ds(1,bdd,promo)
bilan = stat_classe(notes)
ecriture_notes_tex(notes[0],bilan,file)




"""
(
	`id_eleve`	INTEGER,tt
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