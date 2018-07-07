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

file_csv = "ClasseurV2.csv"
bdd = "BDD_Evaluation.db"
num_ds = 1
annee = 2018

import os

def lire_notes(file):
    """ Lire le fichier de notes sous la forme 
    IdEleve, Q1, Q2, Q3, ..., commentaire"""
    
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


def remplir_bdd(num_ds,annee,competences,nb_questions, bareme, poids, notes,bdd):

    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    
    for eleve in notes : 
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
    bilan.reverse()
    #print(bilan)
    
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
    
def moyenne_classe(bilan_cl) :
    # Moyenne harmonisée et non harmonisée
    m = 0
    mh = 0
    for i in range(len(bilan_cl)):
        m = m+bilan_cl[i][6]        
        mh = mh+bilan_cl[i][7]
    m = m/len(bilan_cl)
    mh = mh/len(bilan_cl)
    return [m,mh]
    
def bilan_competences_ds(notes_el):
    # Rappel : pour une question, une note éleve est composée :
    # Id éleve[0], Numero question[1], poids(5)[2], bareme[3], note/5[4], commentaire[5], id_competence[6], comp longue[7], com courte[8].
    bilan_el=[] # Liste compsée d'une liste de  code comp, note eleve, note maxi
    # Recherche des compétences et incrémentation de la note et du barème. 
    for note in notes_el :
        comp = note[6]
        pts_el = note[4]*note[3]
        if type(pts_el)== str :
            pts_el = 0
        pts_total = note[2]*note[3]
        comp_lg = note[7]
        comp_courte = note[8]
        bilan_q = [comp,pts_el,pts_total,comp_lg,comp_courte]
        flag = True
        for i in range(len(bilan_el)):
            if comp == bilan_el[i][0] :
                bilan_el[i][1]+=pts_el
                bilan_el[i][2]+=pts_total
                flag = False
        if flag :
            bilan_el.append(bilan_q)

    
    return bilan_el
    
def creation_histogramme(bilan):
    # il faut que la derniere valeur de chaque élément du bilan soit la moyenne harmonisée
    histo = []
    for i in range(len(bilan)):
        histo.append(bilan[i][-1])
    histo.sort()
    
    plt.hist(histo, range = (0, 20), bins = 2, color = 'gray',edgecolor = 'black', histtype='bar', rwidth=0.8)
    #, color = 'yellow',edgecolor = 'red')
    
    plt.xlabel('Notes')
    plt.ylabel('Nombre')
    plt.title('Histogramme des notes')
    plt.savefig("histo.pdf")
    
    
    
    
def harmonisation(bilan,a=1,b=0):
    """
    Calcul de la moyenne de chaque éleve et harmonisation de
     la forme ax+b
    """
    for i in range(len(bilan)):
        note = 20* bilan[i][1]/bilan[i][2]
        note_h = a*note+b
        bilan[i].append(note)
        bilan[i].append(note_h)
    
    
    
    
def ecriture_notes_tex(notes,comp_el,bilan_el,moy):
    """
    Ecriture des notes  pour un seul élève.
    """
    el = notes[0][0]
    # On compte le nombre de lignes de notes :
    nb_ques = len(notes)
    nb_lignes = nb_ques//4+1

    #file_el = file+str(el)+".tex"
    file_el = "f1.tex"
    # fid = open(file_el,'w')
    fid = codecs.open(file_el, "w", "utf-8")
    
    
    
    # ===== EN TETE ELEVE ====
    
    fid.write("\\begin{minipage}[c]{.45\\linewidth} \n")
    
    fid.write("\\Large \\textbf{\\textsf{"+bilan_el[4].upper()+" "+bilan_el[5]+"}} \n \n")  
    
    fid.write(" \\normalsize Note harmonisée "+str(round(bilan_el[7],2))+"/20 \n \n")
    fid.write("Rang "+str(bilan_el[3])+"\n \n")
    fid.write("Note brute "+str(round(bilan_el[6],2))+"/20 \n \n")
    
    fid.write("Moyenne classe harmonisée "+str(round(moy[1],2))+"/20 \n \n")
    
    fid.write("Commentaires : \n")
    fid.write(notes[0][5]+" \n")
    fid.write("\\end{minipage}\\hfill \n")
    fid.write("\\begin{minipage}[c]{.45\\linewidth}  \n")
    fid.write("\\begin{center}\n")
    fid.write("\\includegraphics[width=.8\\linewidth]{../histo.pdf} \n")
    fid.write("\\end{center}\n")
    
    fid.write("\\end{minipage}\n")
    
    

    
    # ===== NOTES PAR QUESTIONS =====
    # On ajoute les notes par questions
    fid.write("\\footnotesize \n")
    fid.write("\\begin{center} \n")
    fid.write("\\begin{tabular}{|c|c|c|c||c|c|c|c||c|c|c|c||c|c|c|c|} \n")
    fid.write("\\hline \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} \\\ \n")
    fid.write("\\hline \n")
    fid.write("\\hline \n")
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
            ligne = ligne+" & "+str(notes[c4][1])+" & "+str(notes[c4][3])+" & "+str(notes[c4][6])+" & "+str(notes[c4][4])+" \\\ \\hline "
        else : 
            ligne = ligne+" & "+" & "+" & "+" & "+" \\\ \\hline \n"
        fid.write(ligne)
        fid.write('\n')
        
    #fid.write("\\hline \n")
    fid.write("\\end{tabular} \n")
    fid.write("\\end{center} \n")
    fid.write("\\normalsize \n \n")
    # ===== FIN NOTES PAR QUESTIONS =====
    
    # ===== NOTES PAR COMPETENCES =====
    fid.write("\\footnotesize \n")
    fid.write("\\begin{center} \n")
    fid.write("\\begin{tabular}{|p{.7\linewidth}|c|} \n")
    fid.write("\\hline \n")
    ch = "Compétences  & Taux \\\ \\hline \\hline \n"
    
    fid.write(ch)
    
    
    for i in range(len(comp_el)):
        code_comp = comp_el[i][0]
        nom_comp  = comp_el[i][3]
        taux =  comp_el[i][1]/comp_el[i][2]*100
        taux = int(taux)
        ligne = code_comp + " -- " + nom_comp + "&" + str(taux) + " \\% \\\ \\hline \n"
        fid.write(ligne)
    
    fid.write("\\end{tabular} \n")
    fid.write("\\end{center} \n")
    fid.write("\\normalsize \n \n")
    
    
    fid.close()    


def generation_bilan(notes,bilan_el,bilan_classe,moy):
    os.chdir("FicheDS")
    for i in range(len(notes)):
        ecriture_notes_tex(notes[i],bilan_el[i],bilan_classe[i],moy)
        os.system("pdflatex FicheDS.tex")
        ff = i
        if ff<10 :
            ff = str(0)+str(ff)
        fichier = ""+str(ff)+".pdf"
        shutil.copyfile("FicheDS.pdf",fichier)
    
    os.chdir("..")

def concatenation_pdf():
    os.chdir("FicheDS")
    liste_pdf = []
    liste = os.listdir()
    for f in liste : 
        if "pdf" in f :
            liste_pdf.append(f)
    liste_pdf=liste_pdf[0:-1]
    
    input_streams = []
    for input_file in liste_pdf:
        input_streams.append(open(input_file, 'rb'))
    writer = PdfFileWriter()
    for reader in map(PdfFileReader, input_streams):
        for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
    
    with open("BILAN.pdf", 'wb') as fileobj:
        writer.write(fileobj)
    
    

####     
promo = 2018
num_ds = 1

# Lecture du fichier de notes
notes_classe = lire_notes(file_csv)    

"""
# Remplissage de la BDD
remplir_bdd(num_ds,annee,competences,nb_questions, bareme, poids, notes,bdd)

# Bilan des notes par élves
notes = bilan_ds(num_ds,bdd,promo)

# Bilan des notes de la classe (classement etc...)
bilan_classe = stat_classe(notes)

# Bilan des élèves par compétences
bilan_ts_el = []
for i in range(len(notes)):
    bilan_el  = bilan_competences_ds(notes[i])
    bilan_ts_el.append(bilan_el)
    
# Harmonisation des notes
harmonisation(bilan_classe,a=1,b=0)

# Création de l'histogramme des notes
creation_histogramme(bilan_classe)

# Calcul de la moyenne classe
moy = moyenne_classe(bilan_classe)


# Génération des bilans individuels
generation_bilan(notes,bilan_ts_el,bilan_classe,moy)
"""

"""
# Concaténuation des bilans
concatenation_pdf()
"""

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