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
    
    
    # Besoin du bareme question,comp
    quest_comp=[]
    for q in bareme_final:
        num = q[0]
        cp = q[3:]
        comp = []
        for c in cp :
            comp.append(c[0][0])
        quest_comp.append([num,comp])
    
    #for b in bareme_final:
    #for b in bareme_comp:
    #    print(b)
    #print(bareme_final)
    return bareme_final,bareme_comp,quest_comp
    # Transposer une liste : 
    #list(map(list, zip(*baremeh)))


def calcul_note_eleve(notes_eleve,bareme,bareme_comp):
    id_eleve = notes_eleve[0]
    notes = notes_eleve[1]
    comment = notes_eleve[2]
    
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
    
    
        
    return [int(id_eleve),round(pts_eleve*20/total_pts,3),notes,dico_comp,comment]
    
def stat_ds(bilan_ds,a,b):
    """
    Calcul de la moyenne, des rangs, de l'écart type.
    notes corrigées avec note = note_brute*a+b
    """
    id_note =[]
    notes_brutes = []
    # On récupère les id et les notes.
    for bilan_eleve in bilan_ds :
        id_note.append(bilan_eleve[0:2])
        notes_brutes.append(bilan_eleve[1])
        
    # On fait le classement
    for i in range(len(id_note)):
        id_note[i][0],id_note[i][1] = id_note[i][1],id_note[i][0] 
    
    id_note.sort()
    id_note.reverse()
    for i in range(len(id_note)):
        id_note[i]= [id_note[i][1],id_note[i][0],i+1]
        
    id_note.sort()
    
    # Fin du classement id_note contient [[id_el,note,class],...]
    
    
    moyenne_classe = sum(notes_brutes)/len(notes_brutes)
    # On ajoute le classement au bilan des DS
    for i in range(len(bilan_eleve)):
        if bilan_ds[i][0]==id_note[i][0]:
            bilan_ds[i].insert(2,id_note[i][2])
        else : 
            print("Les ID ne correspondent pas")
    
    # On modfie la note en appliquant le correctif
    for i in range(len(bilan_eleve)):
        bilan_ds[i][1]=a*bilan_ds[i][1]+b
    
    notes_eleves = [a*x+b for x in notes_brutes]
    # Bilan ds a été modifié en place. On n'est pas obligé de le retourner
    return moyenne_classe*a+b,notes_eleves
    
def creation_histogramme(bilan):
    # il faut que la derniere valeur de chaque élément du bilan soit la moyenne harmonisée
    bilan.sort()
    
    plt.hist(bilan, range = (0, 20), bins = 2, color = 'gray',edgecolor = 'black', histtype='bar', rwidth=0.8)
    #, color = 'yellow',edgecolor = 'red')
    
    plt.xlabel('Notes')
    plt.ylabel('Nombre')
    plt.title('Histogramme des notes')
    plt.savefig("histo.pdf")

    
def ecriture_notes_tex(bilan_eleve,moyenne_classe,bareme,quest_comp,promo,file_bdd):
    """
    Ecriture des notes  pour un seul élève.
    """
    
    id_el = bilan_eleve[0]
    note_eleve = bilan_eleve[1]
    rang_eleve = bilan_eleve[2]
    notes = bilan_eleve[3]
    # On compte le nombre de lignes de notes :
    nb_ques = len(notes)
    nb_lignes = nb_ques//4+1
    
    # On cherche le nom et le prénom
    conn = sqlite3.connect(bdd)
    c = conn.cursor()
    req = "SELECT nom,prenom FROM eleves WHERE id_eleve="+str(id_el)
    c.execute(req)
    tab = c.fetchall()
    conn.commit()
    conn.close()
    print(tab)
    nom,prenom = tab[0][0],tab[0][1]
    
    

    #file_el = file+str(el)+".tex"
    file_el = "f1.tex"
    # fid = open(file_el,'w')
    fid = codecs.open(file_el, "w", "utf-8")
    
    
    
    
    # ===== EN TETE ELEVE ====
    
    fid.write("\\begin{minipage}[c]{.45\\linewidth} \n")
    
    fid.write("\\Large \\textbf{\\textsf{"+nom.upper()+" "+prenom+"}} \n \n")  
    
    fid.write(" \\normalsize Note harmonisée "+str(round(note_eleve,2))+"/20 \n \n")
    fid.write("Rang "+str(rang_eleve)+"\n \n")
    #fid.write("Note brute "+str(round(bilan_el[1],2))+"/20 \n \n")
    
    fid.write("Moyenne classe harmonisée "+str(round(moyenne_classe,2))+"/20 \n \n")
    
    fid.write("Commentaires : \n")
    fid.write(bilan_eleve[5]+" \n")
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
    fid.write("\\begin{tabular}{|c|c|m{1cm}|c||c|c|m{1cm}|c||c|c|m{1cm}|c||c|c|m{1cm}|c|} \n")
    fid.write("\\hline \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} & \\textbf{Qu} & \\textbf{Coef} & \\textbf{Comp} & \\textbf{/5} \\\ \n")
    fid.write("\\hline \n")
    fid.write("\\hline \n")
    for i in range (0,nb_lignes):
        c1 = i
        c2 = nb_lignes+i
        c3 = 2*nb_lignes+i
        c4 = 3*nb_lignes+i
        ligne = ""
        
        cp1 = quest_comp[c1][1]
        comp1 = cp1[0]
        if len(cp1)>1:
            for c in cp1[1:]:
                comp1+=", "+c
        
        cp2 = quest_comp[c2][1]
        comp2 = cp2[0]
        if len(cp2)>1:
            for c in cp2[1:]:
                comp2+=", "+c
                
        cp3 = quest_comp[c3][1]
        comp3 = cp3[0]
        if len(cp3)>1:
            for c in cp3[1:]:
                comp3+=", "+c
        
        
        ligne = ligne+str(c1+1)+" & "+str(bareme[c1][1])+" & "+comp1+" & "+str(notes[c1])
        ligne = ligne+" & "+str(c2+1)+" & "+str(bareme[c2][1])+" & "+comp2+" & "+str(notes[c2])
        ligne = ligne+" & "+str(c3+1)+" & "+str(bareme[c3][1])+" & "+comp3+" & "+str(notes[c3])
        
        
        if c4 < nb_ques :
            cp4 = quest_comp[c4][1]
            comp4 = cp4[0]
            if len(cp4)>1:
                for c in cp4[1:]:
                    comp4+=", "+c
        
            ligne = ligne+" & "+str(c4+1)+" & "+str(bareme[c4][1])+" & "+comp4+" & "+str(notes[c4])+" \\\ \\hline "
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
    
    
    dico = bilan_eleve[4]
    
    for clef in dico :
        id_comp = clef
        taux = dico[clef]*100
        # On cherche le nom court de la competence
        conn = sqlite3.connect(bdd)
        c = conn.cursor()
        req = "SELECT nom_court FROM table_competences WHERE id_competence='"+str(id_comp)+"'"
        
        c.execute(req)
        tab = c.fetchall()
        conn.commit()
        conn.close()
        nom_court = tab[0][0]
        
        ligne = id_comp + " -- " + nom_court + "&" + str(taux) + " \\% \\\ \\hline \n"
        fid.write(ligne)    
        

    
    fid.write("\\end{tabular} \n")
    fid.write("\\end{center} \n")
    fid.write("\\normalsize \n \n")
    
    
    fid.close()   
    
    
promo = 2018
num_ds = 1

# Lecture du fichier de notes
notes_classe = lire_notes(file_csv)    
# Lecture du bareme
bareme,bareme_comp,quest_comp = lire_bareme(file_bareme)

bilan_ds=[]
# PAR DS un bilan [id,note/20, notes_q, dico_comp,commentaire]
for notes_eleve in notes_classe : 
    result_eleve = calcul_note_eleve(notes_eleve,bareme,bareme_comp)
    bilan_ds.append(result_eleve)

moyenne_classe,notes_eleves = stat_ds(bilan_ds,1,1)

# Création de l'histogramme
creation_histogramme(notes_eleves)

# Ecriture des fichiers élèves
bilan_eleve = bilan_ds[0]
ecriture_notes_tex(bilan_eleve,moyenne_classe,bareme,quest_comp,promo,bdd)
    