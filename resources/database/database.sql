-- Schema
CREATE SCHEMA IF NOT EXISTS taxon_concept AUTHORIZATION jpm;

-- Drop table

-- DROP TABLE taxon_concept.description;
-- DROP TABLE taxon_concept.description_media;

-- Tables

CREATE TABLE taxon_concept.description (
	id serial NOT NULL, -- Identifiant de la description.
    mnemonic varchar(250) NOT NULL, -- Libellé permettant d'identifier la description facilement dans la publication.
    "rank" varchar(50) NOT NULL, -- Rang du taxon décrit.
	raw_text text NOT NULL, -- Texte brute copié/collé de la publication.
    "order" varchar(5) NULL, -- Code/numéro d'ordre de la description dans la publication.
    sciname varchar(150) NULL, -- Nom scientifique complet avec auteurs, année et publication.
    relationships text NULL, -- Citations du taxon dans d'autres ouvrages.
    zoobank varchar(250) NULL, -- URL vers la référence dans Zoobank.
    type_locality text NULL, -- Localité du type.
    material_examined text NULL, -- Informations sur les spécimens examinés et la typification.
    diagnosis text NULL, -- Diagnose du taxon.
	"description" text NULL, -- Description brute d'origine issue de la taxon_concept.
    subtaxa text NULL, -- Description des sous-taxons éventuels.
    bionomics text NULL, -- Information sur la biologie du taxon.
    "distribution" text NULL, -- Répartition du taxon.
    etymology text NULL, -- Origine du nom donné (derivatio nominis).
    comments text NULL, -- Commentaire sur la description.
    meta_user_id int NOT NULL DEFAULT 0, -- Identifiant de l'utilisateur ayant fait la dernière modification sur l'enregistrement. Anonyme = 0.
    meta_date timestamp NOT NULL DEFAULT NOW(), -- Date et heure de dernière modification de l'enregistrement.
    meta_state char(1) NOT NULL -- Indique l'état de l'enregistrement à l'aide d'une lettre : C (créé), U (mise à jour), D (supprimé)
);


CREATE TABLE taxon_concept.description_media (
    id serial NOT NULL, -- Identifiant du media.
    description_id int NOT NULL, -- Identifiant de la description à laquelle ce media appartient.
    raw_text text NULL, -- Texte brute accompagnant le media.
    file_path varchar(250) NOT NULL, -- Chemin vers le fichier.
    file_hash varchar(32) NOT NULL -- Hash md5 du fichier.
);


-- Column comments
COMMENT ON COLUMN taxon_concept.description.id IS 'Identifiant de la fiche.';
COMMENT ON COLUMN taxon_concept.description.mnemonic IS 'Libellé permettant d''identifier la description facilement dans l''ouvrage.';
COMMENT ON COLUMN taxon_concept.description.rank IS 'Rang du taxon décrit.';
COMMENT ON COLUMN taxon_concept.description.raw_text IS 'Texte brute copié/collé de la publication.';
COMMENT ON COLUMN taxon_concept.description.order IS 'Code/numéro d''ordre de la description dans la publication';
COMMENT ON COLUMN taxon_concept.description.sciname IS 'Nom scientifique complet avec auteurs, année et publication.';
COMMENT ON COLUMN taxon_concept.description.relationships IS 'Citations du taxon dans d''autres ouvrages.';
COMMENT ON COLUMN taxon_concept.description.zoobank IS 'URL vers la référence dans Zoobank.';
COMMENT ON COLUMN taxon_concept.description.type_locality IS 'Localité du type.';
COMMENT ON COLUMN taxon_concept.description.material_examined IS 'Informations sur les spécimens examinés et la typification.';
COMMENT ON COLUMN taxon_concept.description.diagnosis IS 'Diagnose du taxon.';
COMMENT ON COLUMN taxon_concept.description.description IS 'Description brute d''origine issue de la taxon_concept.';
COMMENT ON COLUMN taxon_concept.description.subtaxa IS 'Description des sous-taxons éventuels';
COMMENT ON COLUMN taxon_concept.description.bionomics IS 'Information sur la biologie, écologie du taxon.';
COMMENT ON COLUMN taxon_concept.description.distribution IS 'Répartition du taxon.';
COMMENT ON COLUMN taxon_concept.description.etymology IS 'Origine du nom donné (derivatio nominis).';
COMMENT ON COLUMN taxon_concept.description.comments IS 'Commentaire sur la description.';
COMMENT ON COLUMN taxon_concept.description.meta_user_id IS 'Identifiant de l''utilisateur ayant fait la dernière modification sur l''enregistrement.';
COMMENT ON COLUMN taxon_concept.description.meta_date IS 'Date et heure de dernière modification de l''enregistrement.';
COMMENT ON COLUMN taxon_concept.description.meta_state IS 'Indique l''état de l''enregistrement à l''aide d''une lettre : A (ajouté), U (mise à jour), D (supprimé)';


COMMENT ON COLUMN taxon_concept.description_media.id IS 'Identifiant du media.';
COMMENT ON COLUMN taxon_concept.description_media.description_id IS 'Identifiant de la description à laquelle ce media appartient.';
COMMENT ON COLUMN taxon_concept.description_media.raw_text IS 'Texte brute accompagnant le media.';
COMMENT ON COLUMN taxon_concept.description_media.file_path IS 'Chemin vers le fichier.';
COMMENT ON COLUMN taxon_concept.description_media.file_hash IS 'Hash md5 du fichier.';


-- Primary keys
ALTER TABLE ONLY taxon_concept.description
    ADD CONSTRAINT pk_description PRIMARY KEY (id);

ALTER TABLE ONLY taxon_concept.description_media
    ADD CONSTRAINT pk_description_media PRIMARY KEY (id);


-- Foreign keys
ALTER TABLE ONLY taxon_concept.description_media
    ADD CONSTRAINT fk_dm_description FOREIGN KEY (description_id)
    REFERENCES taxon_concept.description (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;


-- Permissions
ALTER TABLE taxon_concept.description OWNER TO jpm;
GRANT ALL ON TABLE taxon_concept.description TO jpm;


ALTER TABLE taxon_concept.description_media OWNER TO jpm;
GRANT ALL ON TABLE taxon_concept.description_media TO jpm;
