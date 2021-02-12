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
		affectation_avant double precision, -- < Année de référence
		affectation_a double precision, -- Année de référence
		affectation_a2 double precision, -- Année de référence + 1
		affectation_a3 double precision, -- Année de référence + 2
		affectation_a4 double precision, -- Année de référence + 3
		affectation_a5 double precision, -- Année de référence + 4
		affectation_a6 double precision, -- Année de référence + 5
		affectation_apres double precision -- > Année de référence + 5
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
			SELECT -- Ligne pour les tableaux suivants, cellule ligne "Montant affecté de n vers .." / colonne "Avant .."
				0 annee_recette, -- Non utilisé
				0 montant_recette, -- Non utilisé
				0 affectation_avant, -- Non utilisé
							 
				 -- Année de référence, puis année + 1, etc.
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef AND aff.annee_recette < anneeRef) affectation_a,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+1 AND aff.annee_recette < anneeRef) affectation_a2,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+2 AND aff.annee_recette < anneeRef) affectation_a3,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+3 AND aff.annee_recette < anneeRef) affectation_a4,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+4 AND aff.annee_recette < anneeRef) affectation_a5,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+5 AND aff.annee_recette < anneeRef) affectation_a6,
				
				0 affectation_apres -- Non utilisé
			UNION
			SELECT
				annees.annee annee_recette,
				-- Recettes = somme des recettes affectées des projets + sommes des montants affectés en entrées-sorties :
				(SELECT COALESCE(sum(r.montant_r), 0) FROM recette r WHERE r.annee_r = annees.annee AND r.id_r IN (SELECT ma.id_r FROM montant_affecte ma)) + (SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.id_r IS NULL AND aff.annee_recette = annees.annee) montant_recette,
				
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation < anneeRef AND aff.annee_recette = annees.annee) affectation_avant,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef AND aff.annee_recette = annees.annee) affectation_a,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+1 AND aff.annee_recette = annees.annee) affectation_a2,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+2 AND aff.annee_recette = annees.annee) affectation_a3,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+3 AND aff.annee_recette = annees.annee) affectation_a4,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+4 AND aff.annee_recette = annees.annee) affectation_a5,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation = anneeRef+5 AND aff.annee_recette = annees.annee) affectation_a6,
				(SELECT COALESCE(sum(aff.montant), 0) FROM affectations aff WHERE aff.annee_affectation > anneeRef+5 AND aff.annee_recette = annees.annee) affectation_apres
			FROM
				(SELECT DISTINCT aff2.annee_recette annee FROM affectations aff2 ORDER BY annee) annees
			WHERE annees.annee >= anneeRef;
END; $$ 
LANGUAGE 'plpgsql';

/*ALTER FUNCTION bilan_financier(integer)
    OWNER TO hello_flask;
	
GRANT EXECUTE ON FUNCTION bilan_financier(integer) 
	TO hello_flask;*/
	
-- Utilisation : SELECT * FROM bilan_financier(2016) ORDER BY annee_recette;
-- Vérif : SELECT SUM(da.montant_recette), SUM(da.affectation_avant)+SUM(da.affectation_a)+SUM(da.affectation_a2)+SUM(da.affectation_a3)+SUM(da.affectation_a4)+SUM(da.affectation_a5)+SUM(da.affectation_apres) FROM (SELECT * FROM bilan_financier(2016) WHERE annee_recette>0  ORDER BY annee_recette) da;
