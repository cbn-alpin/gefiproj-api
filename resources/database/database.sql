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

/* **** BEGIN CREATE FUNCTION ******* */
-- Facilite la récupération des affectations.
DROP FUNCTION IF EXISTS affectations_sur(integer);

-- Retourne les affectations faite l'année en paramètre, à partir de la tables ‘affectation’ mais aussi de 'entree_sortie’.
-- @Param anneeAffectation : année des affectations. Si à 0, alors il n'y a pas de filtrage.
CREATE OR REPLACE FUNCTION affectations_sur(
	IN anneeAffectation integer DEFAULT 0)
    RETURNS table (
		id_ma integer, -- Identifiant du montant affecté (à 0 si la donnée vient de 'entree_sortie')
		id_r integer, -- Identifiant de la recette (à 0 si la donnée vient de 'entree_sortie')
		id_es integer, -- Identifiant de l'entrée/sortie (à 0 si la donnée vient de 'affectation')
		montant double precision,
		annee_recette integer,
		annee_affectation integer
	)
AS $$
DECLARE
BEGIN
	-- Liste des montants affectés sur l'année en paramètre
	RETURN
		QUERY
			SELECT
				ma.id_ma,
				r.id_r,
				0 id_es,
				montant_ma montant,
				annee_r annee_recette,
				annee_ma annee_affectation
			FROM montant_affecte ma NATURAL JOIN recette r
				WHERE ma.annee_ma = anneeAffectation OR anneeAffectation = 0
			UNION
				SELECT
					0 id_ma,
					0 id_r,
					es.id_es,
					montant_es montant,
					annee_recette_es annee_recette,
					annee_affectation_es annee_affectation
				FROM entree_sortie es
					WHERE annee_affectation_es = anneeAffectation OR anneeAffectation = 0;
END; $$
LANGUAGE 'plpgsql';

ALTER FUNCTION affectations_sur(integer)
    OWNER TO hello_flask;

GRANT EXECUTE ON FUNCTION affectations_sur(integer)
	TO hello_flask;

-- Utilisation : SELECT * FROM affectations_sur(2022);
-- Utilisation, sans filtrage : SELECT * FROM affectations_sur();

/* ----------------------------------------------------------------------------------------------- */


-- Données utiles pour le bilan financier (tableau 1).

DROP FUNCTION IF EXISTS bilan_financier(integer);
-- Retourne le bilan financier (tableau 1, en haut du bilan) sous forme d'une table
-- Attention : la 1ère ligne (avec annee_recette=0) correspond aux affectations de recettes qui précèdent l'année de référence. Utile pour les tableaux suivants.
-- @Param anneeRef : année de référence.
CREATE OR REPLACE FUNCTION bilan_financier(
	IN anneeRef integer)
    RETURNS table (
		annee_recette integer,
		montant_recette double precision,
		affectation_avant double precision,
		affectation_a double precision,
		affectation_a2 double precision,
		affectation_a3 double precision,
		affectation_a4 double precision,
		affectation_a5 double precision,
		affectation_apres double precision
	)
AS $$

BEGIN
	CREATE TEMP TABLE affectations(
		id_ma integer, -- Identifiant du montant affecté (à 0 si la donnée vient de 'entree_sortie')
		id_r integer, -- Identifiant de la recette (à 0 si la donnée vient de 'entree_sortie')
		id_es integer, -- Identifiant de l'entrée/sortie (à 0 si la donnée vient de 'affectation')
		montant double precision,
		annee_recette integer,
		annee_affectation integer
	) on commit drop;

	INSERT INTO affectations
		SELECT * FROM affectations_sur();

	-- Tableau 1 du bilan financier
	RETURN
		QUERY
			SELECT
				0 annee_recette,
				0 montant_recette,
				0 affectation_avant,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef AND aff.annee_recette < anneeRef) affectation_a,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+1 AND aff.annee_recette < anneeRef) affectation_a2,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+2 AND aff.annee_recette < anneeRef) affectation_a3,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+3 AND aff.annee_recette < anneeRef) affectation_a4,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+4 AND aff.annee_recette < anneeRef) affectation_a5,
				0 affectation_apres
			UNION
			SELECT
				annees.annee annee_recette,
				(SELECT COALESCE(sum(r.montant_r), 0) FROM recette r WHERE r.annee_r = annees.annee) montant_recette,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation < anneeRef AND aff.annee_recette = annees.annee) affectation_avant,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef AND aff.annee_recette = annees.annee) affectation_a,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+1 AND aff.annee_recette = annees.annee) affectation_a2,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+2 AND aff.annee_recette = annees.annee) affectation_a3,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+3 AND aff.annee_recette = annees.annee) affectation_a4,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+4 AND aff.annee_recette = annees.annee) affectation_a5,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation > anneeRef+4 AND aff.annee_recette = annees.annee) affectation_apres
			FROM
				(SELECT annee_r annee FROM recette GROUP BY annee_r ORDER BY annee_r) annees;
END; $$
LANGUAGE 'plpgsql';

ALTER FUNCTION bilan_financier(integer)
    OWNER TO hello_flask;

GRANT EXECUTE ON FUNCTION bilan_financier(integer)
	TO hello_flask;

-- Utilisation :
SELECT * FROM bilan_financier(2016) ORDER BY annee_recette;

/* ----------------------------------------------------------------------------------------------- */

-- Données utiles pour le suivi des financements

DROP FUNCTION IF EXISTS suivi_financement(integer, integer, integer);
-- Retourne le suivi des financements sous forme d'une table
-- @Param versionFt : version (1 ou 2) du suivi.
-- @Param anneeRef : année de référence pour la v1 et année min pour la v2.
-- @Param anneeMax : année max pour la v2. Non utilisé pour la v1.
CREATE OR REPLACE FUNCTION suivi_financement(
	IN versionFt integer,
	IN anneeRef integer,
	IN anneeMax integer DEFAULT 0)
    RETURNS table (
		id_p integer, -- Identifiant du projet
		code_p integer,
		nom_p varchar,
		id_u integer, -- Identifiant du responsable
		initiales_u varchar,
		id_f integer, -- Identifiant du financement
		date_arrete_f date,
		date_limite_solde_f date,
		montant_arrete_f double precision,
		commentaire_admin_f varchar,
		imputation_f varchar,
		numero_titre_f varchar,
		statut_f varchar,
		id_financeur integer, -- Identifiant du financeur
		nom_financeur varchar,
		recette_avant double precision,
		recette_a double precision,
		recette_a2 double precision,
		recette_a3 double precision,
		recette_a4 double precision,
		recette_a5 double precision,
		recette_apres double precision
	)
AS $$
DECLARE
	codeAnneeMin integer;
	codeAnneeMax integer;
BEGIN
	CREATE TEMP TABLE temp_id(
		id_f integer
	) on commit drop;

	-- Sélection des financements à analyser
	IF versionFt = 1 THEN -- Version 1 basée sur les statuts des financements
		BEGIN
			RAISE INFO 'Version 1 - année %', anneeRef;

			INSERT INTO temp_id(id_f)
				SELECT f.id_f FROM financement f
					WHERE f.statut_f IN ('ANTR', 'ATR')
						OR (f.statut_f = 'SOLDE'
						AND f.date_solde_f IS NOT NULL
						AND extract(year from COALESCE(f.date_solde_f, DATE '1900-01-01')) >= anneeRef);
		END;
		ELSE -- Version 2 basée sur une période, pour les projets
			BEGIN
				codeAnneeMin := (anneeRef % 100) * 1000;
				codeAnneeMax := (COALESCE(anneeMax, anneeRef) % 100) * 1000;
				RAISE INFO 'Version 2 - min: %, max: %', codeAnneeMin, codeAnneeMax;

				INSERT INTO temp_id(id_f)
					SELECT f.id_f FROM projet p NATURAL JOIN financement f
						WHERE p.code_p >= codeAnneeMin
							AND p.code_p <= codeAnneeMax;
			END;
	END IF;

	-- Tableau du suivi des financements
	RETURN
		QUERY SELECT
			p.id_p,
			p.code_p,
			p.nom_p,
			u.id_u,
			u.initiales_u,
			f.id_f,
			f.date_arrete_f,
			f.date_limite_solde_f,
			f.montant_arrete_f,
			f.commentaire_admin_f,
			f.imputation_f,
			f.numero_titre_f,
			f.statut_f,
			feur.id_financeur,
			feur.nom_financeur,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r < anneeRef) recette_avant,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r = anneeRef) recette_a,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r = anneeRef+1) recette_a2,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r = anneeRef+2) recette_a3,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r = anneeRef+3) recette_a4,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r = anneeRef+4) recette_a5,
			(SELECT COALESCE(SUM(montant_r), 0) FROM recette r WHERE r.id_f = f.id_f AND r.annee_r > anneeRef+4) recette_apres
		FROM
			projet p
			NATURAL JOIN utilisateur u
			INNER JOIN financement f ON f.id_p = p.id_p
			LEFT JOIN financeur feur ON feur.id_financeur = f.id_financeur
		WHERE
			f.id_f IN (SELECT ti.id_f FROM temp_id ti);
END; $$
LANGUAGE 'plpgsql';

ALTER FUNCTION suivi_financement(integer, integer, integer)
    OWNER TO hello_flask;

GRANT EXECUTE ON FUNCTION suivi_financement(integer, integer, integer)
	TO hello_flask;

-- Utilisation v1 : SELECT * FROM suivi_financement(1, 2019) ORDER BY id_p, id_f;
-- Utilisation v2 : SELECT * FROM suivi_financement(2, 2019, 2021) ORDER BY id_p, id_f;