/*===========================================*/
-- TABLES CREATION SCRIPT
-- v3, modifié le 29/01/2020 Pour ajouter la table entree_sortie, des index et des index unique.
/*===========================================*/

/*===========================================*/
-- NOTE :
-- prevoir trigger sur le projet correspondant

-- Statut projet - False : non soldé | True : soldé

-- ANTR : actif non totalement rattaché
-- ATR : actif totalement rattaché
-- SOLDE : soldé
/*===========================================*/


/*clean database*/
DROP TABLE IF EXISTS role_acces CASCADE;
DROP TABLE IF EXISTS utilisateur CASCADE;
DROP TABLE IF EXISTS role_utilisateur CASCADE;
DROP TABLE IF EXISTS financeur CASCADE;
DROP TABLE IF EXISTS depense CASCADE;
DROP TABLE IF EXISTS projet CASCADE;
DROP TABLE IF EXISTS financement CASCADE;
DROP TABLE IF EXISTS recette CASCADE;
DROP TABLE IF EXISTS montant_affecte CASCADE;
DROP TABLE IF EXISTS entree_sortie CASCADE;
DROP TABLE IF EXISTS historique CASCADE;

/*create data tables*/
CREATE TABLE IF NOT EXISTS role_acces (
    id_ra serial NOT NULL, -- Identifiant du role.
    nom_ra varchar(250) NOT NULL, -- Libellé du role
    code_ra Int NOT NULL, -- Libellé du code role
    CONSTRAINT pk_ra PRIMARY KEY (id_ra)    
);


CREATE TABLE IF NOT EXISTS utilisateur (
    id_u serial NOT NULL,
    nom_u varchar(250),
    prenom_u varchar(250),
    initiales_u varchar(3) NOT NULL UNIQUE,
    email_u varchar(250) NOT NULL UNIQUE,
    password_u varchar(250) NOT NULL,
    active_u boolean DEFAULT TRUE,
    CONSTRAINT pk_u PRIMARY KEY (id_u)
);


CREATE TABLE IF NOT EXISTS role_utilisateur (
    id_ra Int NOT NULL,
    id_u Int NOT NULL,
    CONSTRAINT pk_id_role_utilisateur PRIMARY KEY (id_ra, id_u),
    CONSTRAINT pk_role FOREIGN KEY (id_ra) REFERENCES role_acces(id_ra),
    CONSTRAINT pk_utilisateur FOREIGN KEY (id_u) REFERENCES utilisateur(id_u)
);


CREATE TABLE IF NOT EXISTS financeur (
    id_financeur serial NOT NULL,
    nom_financeur varchar(250) NOT NULL UNIQUE,
    ref_arret_attributif_financeur varchar(250),
    CONSTRAINT pk_financeur PRIMARY KEY (id_financeur)
);


CREATE TABLE IF NOT EXISTS depense (
    id_d serial NOT NULL,
    annee_d Int NOT NULL UNIQUE,
    montant_d float NOT NULL,
    CONSTRAINT pk_d PRIMARY KEY (id_d)
);


CREATE TABLE IF NOT EXISTS entree_sortie (
    id_es serial NOT NULL,
    annee_recette_es Int NOT NULL,
	annee_affectation_es Int NOT NULL,
    montant_es float NOT NULL,
    CONSTRAINT pk_es PRIMARY KEY (id_es)
);


CREATE TABLE IF NOT EXISTS projet(
    id_p serial NOT NULL,
    code_p varchar(4) NOT NULL UNIQUE,
    nom_p varchar(250) NOT NULL UNIQUE,
    statut_p boolean DEFAULT FALSE,
    id_u Int NOT NULL,
    CONSTRAINT pk_p PRIMARY KEY (id_p),
    CONSTRAINT fk_p_responsable FOREIGN KEY (id_u) REFERENCES utilisateur(id_u)
);


CREATE TABLE IF NOT EXISTS financement (
    id_f serial NOT NULL,
    id_p Int NOT NULL,
    id_financeur Int NOT NULL,
    montant_arrete_f float NOT NULL,
    date_arrete_f date ,
    date_limite_solde_f date,
    statut_f varchar(250) NOT NULL,
    date_solde_f date NOT NULL,
    commentaire_admin_f varchar(250),
    commentaire_resp_f varchar(250),
    numero_titre_f varchar(250),
    annee_titre_f varchar(250),
    imputation_f varchar(250),
    CONSTRAINT pk_f PRIMARY KEY (id_f),
    CONSTRAINT fk_f_p FOREIGN KEY (id_p) REFERENCES projet(id_p),
    CONSTRAINT fk_f_f FOREIGN KEY (id_financeur) REFERENCES financeur(id_financeur),
    CONSTRAINT ck_statut CHECK (statut_f IN ('ANTR', 'ATR', 'SOLDE'))
);


CREATE TABLE IF NOT EXISTS recette (
    id_r serial NOT NULL,
    id_f Int NOT NULL,
    montant_r float NOT NULL,
    annee_r Int NOT NULL,
    CONSTRAINT pk_r PRIMARY KEY (id_r),
    CONSTRAINT fk_recette_financement FOREIGN KEY (id_f) REFERENCES financement(id_f)
);


CREATE TABLE IF NOT EXISTS montant_affecte (
    id_ma serial NOT NULL,
    montant_ma float NOT NULL,
    annee_ma Int NOT NULL,
    id_r Int NOT NULL,
    CONSTRAINT pk_ma PRIMARY KEY (id_ma),
    CONSTRAINT fk_ma_recette FOREIGN KEY (id_r) REFERENCES recette(id_r)
);


CREATE TABLE IF NOT EXISTS recette_comptable
(
    id_rc serial NOT NULL,
    montant_rc float NOT NULL,
    annee_rc Int NOT NULL UNIQUE,
    CONSTRAINT pk_rc PRIMARY KEY (id_rc)
);


CREATE TABLE IF NOT EXISTS historique (
    id_h serial NOT NULL,
    id_u Int NOT NULL,
    date_h Date NOT NULL,
    description_h varchar(250),
    id_p Int NOT NULL,
    CONSTRAINT pk_h PRIMARY KEY (id_h),
    CONSTRAINT fk_h_utilisateur FOREIGN KEY (id_u) REFERENCES utilisateur(id_u),
    CONSTRAINT fk_h_projet FOREIGN KEY (id_p) REFERENCES projet(id_p)
);
-- prevoir trigger sur le projet correspondant


/*drop index*/
DROP INDEX IF EXISTS ux_depense_annee;
DROP INDEX IF EXISTS ux_recettecomptable_annee;
DROP INDEX IF EXISTS ux_entreesortie_annees;
DROP INDEX IF EXISTS x_entreesortie_anneeaffectation;
DROP INDEX IF EXISTS x_financement_projet_financeur;
DROP INDEX IF EXISTS x_financement_statut;
DROP INDEX IF EXISTS ux_financeur_nom;
DROP INDEX IF EXISTS x_historique_utilisateur_projet;
DROP INDEX IF EXISTS x_montantaffecte_recette;
DROP INDEX IF EXISTS ux_montantaffecte_recette_annee;
DROP INDEX IF EXISTS ux_projet_nom;
DROP INDEX IF EXISTS ux_projet_code;
DROP INDEX IF EXISTS x_projet_utilisateur;
DROP INDEX IF EXISTS x_projet_statut;
DROP INDEX IF EXISTS ux_recette_financement_annee;
DROP INDEX IF EXISTS x_recette_financement;
DROP INDEX IF EXISTS ux_roleacces_nom;
DROP INDEX IF EXISTS ux_role_utilisateur;
DROP INDEX IF EXISTS ux_utilisateur_initiales;
DROP INDEX IF EXISTS ux_utilisateur_email;


/*create index*/
CREATE UNIQUE INDEX ux_depense_annee ON depense(annee_d);
CREATE UNIQUE INDEX ux_recettecomptable_annee ON recette_comptable(annee_rc);
CREATE UNIQUE INDEX ux_entreesortie_annees ON entree_sortie(annee_recette_es, annee_affectation_es);
CREATE INDEX x_entreesortie_anneeaffectation ON entree_sortie(annee_affectation_es);
CREATE INDEX x_financement_projet_financeur ON financement(id_p, id_financeur); -- Unique ?
CREATE INDEX x_financement_statut ON financement(statut_f);
CREATE UNIQUE INDEX ux_financeur_nom ON financeur(nom_financeur);
CREATE INDEX x_historique_utilisateur_projet ON historique(id_u, id_p);
CREATE INDEX x_montantaffecte_recette ON montant_affecte(id_r);
CREATE UNIQUE INDEX ux_montantaffecte_recette_annee ON montant_affecte(id_r, annee_ma);
CREATE UNIQUE INDEX ux_projet_nom ON projet(nom_p);
CREATE UNIQUE INDEX ux_projet_code ON projet(code_p);
CREATE INDEX x_projet_utilisateur ON projet(id_u);
CREATE INDEX x_projet_statut ON projet(statut_p);
CREATE UNIQUE INDEX ux_recette_financement_annee ON recette(id_f, annee_r);
CREATE INDEX x_recette_financement ON recette(id_f);
CREATE UNIQUE INDEX ux_roleacces_nom ON role_acces(nom_ra);
CREATE UNIQUE INDEX ux_role_utilisateur ON role_utilisateur(id_ra, id_u);
CREATE UNIQUE INDEX ux_utilisateur_initiales ON utilisateur(initiales_u);
CREATE UNIQUE INDEX ux_utilisateur_email ON utilisateur(email_u);


/*insert row*/
INSERT INTO role_acces (nom_ra, code_ra) VALUES ('administrateur', 2);
INSERT INTO role_acces (nom_ra, code_ra) VALUES ('consultant', 1);
