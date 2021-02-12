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
		montant double precision, -- Montant de l'affectation
		annee_recette integer,
		annee_affectation integer
	)    
AS $$
DECLARE
BEGIN
	-- Liste des montants affectés sur l'année en paramètre
	RETURN 
		QUERY 
			SELECT -- Affectations depuis les projets
				ma.id_ma,
				r.id_r,
				0 id_es,
				montant_ma montant,
				annee_r annee_recette,
				annee_ma annee_affectation
			FROM montant_affecte ma NATURAL JOIN recette r -- Laisser 'NATURAL JOIN' pour ne pas inclure les recettes non affectées
				WHERE ma.annee_ma = anneeAffectation OR anneeAffectation = 0
			UNION 
				SELECT -- Affectations des entrées-sorties
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

/*ALTER FUNCTION affectations_sur(integer)
    OWNER TO hello_flask;
	
GRANT EXECUTE ON FUNCTION affectations_sur(integer) 
	TO hello_flask;*/
	
-- Utilisation : SELECT * FROM affectations_sur(2022);
-- Utilisation, sans filtrage : SELECT * FROM affectations_sur();