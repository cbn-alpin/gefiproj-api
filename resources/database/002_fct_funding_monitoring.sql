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
				codeAnneeMax := ((COALESCE(anneeMax, anneeRef) % 100)+1) * 1000;
				RAISE INFO 'Version 2 - min: %, max: %', codeAnneeMin, codeAnneeMax;
				
				INSERT INTO temp_id(id_f)
					SELECT f.id_f FROM projet p NATURAL JOIN financement f
						WHERE p.code_p >= codeAnneeMin
							AND p.code_p < codeAnneeMax;
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
			f.id_f IN (SELECT ti.id_f FROM temp_id ti)
		ORDER BY UPPER(p.nom_p), UPPER(feur.nom_financeur);
END; $$ 
LANGUAGE 'plpgsql';

/*ALTER FUNCTION suivi_financement(integer, integer, integer)
    OWNER TO hello_flask;
	
GRANT EXECUTE ON FUNCTION suivi_financement(integer, integer, integer) 
	TO hello_flask;*/
	
-- Utilisation v1 : SELECT * FROM suivi_financement(1, 2019) ORDER BY id_p, id_f;
-- Utilisation v2 : SELECT * FROM suivi_financement(2, 2018, 2019) ORDER BY id_p, id_f;