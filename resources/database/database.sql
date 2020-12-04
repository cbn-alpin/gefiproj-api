/*===========================================*/
-- TABLES CREATION SCRIPT
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
DROP TABLE IF EXISTS historique CASCADE;

/*create data tables*/
CREATE TABLE IF NOT EXISTS role_acces
(
    id_ra   serial       NOT NULL, -- Identifiant du role.
    nom_ra  varchar(250) NOT NULL, -- Libellé du role
    code_ra serial       NOT NULL, -- Libellé du code role
    CONSTRAINT pk_ra PRIMARY KEY (id_ra)
);


CREATE TABLE IF NOT EXISTS utilisateur
(
    id_u        serial       NOT NULL,
    nom_u       varchar(250),
    prenom_u    varchar(250),
    initiales_u varchar(3)   NOT NULL UNIQUE,
    email_u     varchar(250) NOT NULL UNIQUE,
    password_u  varchar(250) NOT NULL,
    active_u    boolean DEFAULT TRUE,
    CONSTRAINT pk_u PRIMARY KEY (id_u)
);


CREATE TABLE IF NOT EXISTS role_utilisateur
(
    id_ra Int NOT NULL,
    id_u  Int NOT NULL,
    CONSTRAINT pk_id_role_utilisateur PRIMARY KEY (id_ra, id_u),
    CONSTRAINT fk_role_access FOREIGN KEY (id_ra) REFERENCES role_acces (id_ra),
    CONSTRAINT fk_utilisateur FOREIGN KEY (id_u) REFERENCES utilisateur (id_u)
);


CREATE TABLE IF NOT EXISTS financeur
(
    id_financeur                   serial       NOT NULL,
    nom_financeur                  varchar(250) NOT NULL UNIQUE,
    ref_arret_attributif_financeur varchar(250),
    CONSTRAINT pk_financeur PRIMARY KEY (id_financeur)
);


CREATE TABLE IF NOT EXISTS depense
(
    id_d      serial NOT NULL,
    annee_d   Int    NOT NULL UNIQUE,
    montant_d float  NOT NULL,
    CONSTRAINT pk_d PRIMARY KEY (id_d)
);


CREATE TABLE IF NOT EXISTS projet
(
    id_p     serial       NOT NULL,
    code_p   varchar(4)   NOT NULL UNIQUE,
    nom_p    varchar(250) NOT NULL UNIQUE,
    statut_p boolean DEFAULT FALSE,
    id_u     Int          NOT NULL,
    CONSTRAINT pk_p PRIMARY KEY (id_p),
    CONSTRAINT fk_p_responsable FOREIGN KEY (id_u) REFERENCES utilisateur (id_u)
);


CREATE TABLE IF NOT EXISTS financement
(
    id_f                serial       NOT NULL,
    id_p                Int          NOT NULL,
    id_financeur        Int          NOT NULL,
    montant_arrete_f    float        NOT NULL,
    date_arrete_f       date,
    date_limite_solde_f date,
    date_solde_f        date,
    statut_f            varchar(250) NOT NULL,
    commentaire_admin_f varchar(250),
    commentaire_resp_f  varchar(250),
    numero_titre_f      varchar(250),
    annee_titre_f       varchar(250),
    imputation_f        varchar(250),
    CONSTRAINT pk_f PRIMARY KEY (id_f),
    CONSTRAINT fk_f_p FOREIGN KEY (id_p) REFERENCES projet (id_p),
    CONSTRAINT fk_f_f FOREIGN KEY (id_financeur) REFERENCES financeur (id_financeur),
    CONSTRAINT ck_statut CHECK (statut_f IN ('ANTR', 'ATR', 'SOLDE'))
);


CREATE TABLE IF NOT EXISTS recette
(
    id_r      serial NOT NULL,
    id_f      Int    NOT NULL,
    montant_r float  NOT NULL,
    annee_r   Int    NOT NULL,
    CONSTRAINT pk_r PRIMARY KEY (id_r),
    CONSTRAINT fk_recette_financement FOREIGN KEY (id_f) REFERENCES financement (id_f)
);


CREATE TABLE IF NOT EXISTS montant_affecte
(
    id_ma      serial NOT NULL,
    montant_ma float  NOT NULL,
    annee_ma   Int    NOT NULL,
    id_r       Int    NOT NULL,
    CONSTRAINT pk_ma PRIMARY KEY (id_ma),
    CONSTRAINT fk_ma_recette FOREIGN KEY (id_r) REFERENCES recette (id_r)
);


CREATE TABLE IF NOT EXISTS historique
(
    id_h          serial NOT NULL,
    id_u          Int    NOT NULL,
    date_h        Date   NOT NULL,
    description_h varchar(250),
    id_p          Int    NOT NULL,
    CONSTRAINT pk_h PRIMARY KEY (id_h),
    CONSTRAINT fk_h_utilisateur FOREIGN KEY (id_u) REFERENCES utilisateur (id_u),
    CONSTRAINT fk_h_projet FOREIGN KEY (id_p) REFERENCES projet (id_p)
);
-- prevoir trigger sur le projet correspondant


/*drop index*/
DROP INDEX IF EXISTS ux_role_utilisateur;
DROP INDEX IF EXISTS ux_projet;
DROP INDEX IF EXISTS ux_financement;
DROP INDEX IF EXISTS ux_recette;
DROP INDEX IF EXISTS ux_montant_affecte;
DROP INDEX IF EXISTS ux_historique;


/*create index*/
CREATE UNIQUE INDEX ux_role_utilisateur ON role_utilisateur (id_ra, id_u);
CREATE INDEX ux_projet ON projet (id_u);
CREATE INDEX ux_financement ON financement (id_p, id_financeur);
CREATE INDEX ux_recette ON recette (id_f);
CREATE INDEX ux_montant_affecte ON montant_affecte (id_r);
CREATE INDEX ux_historique ON historique (id_u, id_p);


/*insert row*/
INSERT INTO role_acces (nom_ra)
VALUES ('administrateur');
INSERT INTO role_acces (nom_ra)
VALUES ('consultant');

