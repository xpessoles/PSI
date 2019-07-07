BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `table_competences` (
	`id_competence`	TEXT NOT NULL,
	`nom_long`	TEXT,
	`nom_court`	TEXT,
	`semestre`	INTEGER,
	`classe`	INTEGER,
	PRIMARY KEY(`id_competence`)
);
CREATE TABLE IF NOT EXISTS `eleves` (
	`id_eleve`	INTEGER NOT NULL,
	`nom`	TEXT NOT NULL,
	`prenom`	TEXT NOT NULL,
	`naissance`	TEXT,
	`lycee_bac`	TEXT,
	`promo`	NUMERIC,
	`ecole_integree`	TEXT,
	`job`	TEXT,
	`mail`	TEXT
);
CREATE TABLE IF NOT EXISTS `eleve_competences` (
	`id_eleve`	INTEGER NOT NULL,
	`id_competence`	TEXT NOT NULL,
	`DS`	INTEGER,
	`reussite`	INTEGER NOT NULL,
	`promo`	INTEGER,
	PRIMARY KEY(`id_eleve`,`promo`)
);
CREATE TABLE IF NOT EXISTS `ds` (
	`id_eleve`	INTEGER,
	`promo`	INTEGER,
	`ds`	INTEGER,
	`note`	REAL,
	PRIMARY KEY(`promo`,`ds`,`id_eleve`)
);
COMMIT;
