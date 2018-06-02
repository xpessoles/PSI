#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Xavier Pessoles"

"""
Ajout des notes d'un DS à partir d'un fichier CSV.

"""
import sqlite3

bdd = "BDD.db"
conn = sqlite3.connect(bdd)
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS `table_competences` (
	`id_competence`	TEXT NOT NULL,
	`nom_long`	TEXT,
	`nom_court`	TEXT,
	PRIMARY KEY(`id_competence`)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS `eleves` (
	`id_eleve`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`nom`	TEXT NOT NULL,
	`prenom`	TEXT NOT NULL,
	`naissance`	TEXT,
	`lycee_bac`	TEXT,
	`annee_integration`	NUMERIC,
	`ecole_integree`	TEXT,
	`job`	TEXT,
	`mail`	TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS `eleve_competences` (
	`id_eleve`	INTEGER NOT NULL,
	`id_competence`	TEXT NOT NULL,
	`id_ds`	INTEGER NOT NULL,
	`reussite`	INTEGER NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS `ds` (
	`id_eleve`	INTEGER,
	`num_ds`	INTEGER,
	`annee`	INTEGER,
	`nb_questions`	INTEGER,
	`num_question`	INTEGER,
	`poids`	INTEGER,
	`bareme`	INTEGER,
	`note`	TEXT,
	`id_competence`	INTEGER,
	`commentaire`	TEXT
)''')


conn.commit()
conn.close()



