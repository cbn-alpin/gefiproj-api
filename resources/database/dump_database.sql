-- -------------------------------------------------------------
-- TablePlus 3.12.2(358)
--
-- https://tableplus.com/
--
-- Database: dbprod
-- Generation Time: 2021-02-07 19:54:59.1860
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS depense_id_d_seq;

-- Table Definition
CREATE TABLE "public"."depense"
(
    "id_d"      int4   NOT NULL DEFAULT nextval('depense_id_d_seq'::regclass),
    "annee_d"   int4   NOT NULL,
    "montant_d" float8 NOT NULL,
    PRIMARY KEY ("id_d")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS entree_sortie_id_es_seq;

-- Table Definition
CREATE TABLE "public"."entree_sortie"
(
    "id_es"                int4   NOT NULL DEFAULT nextval('entree_sortie_id_es_seq'::regclass),
    "annee_recette_es"     int4   NOT NULL,
    "annee_affectation_es" int4   NOT NULL,
    "montant_es"           float8 NOT NULL,
    PRIMARY KEY ("id_es")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS financement_id_f_seq;

-- Table Definition
CREATE TABLE "public"."financement"
(
    "id_f"                int4         NOT NULL DEFAULT nextval('financement_id_f_seq'::regclass),
    "id_p"                int4         NOT NULL,
    "id_financeur"        int4         NOT NULL,
    "montant_arrete_f"    float8       NOT NULL,
    "date_arrete_f"       date,
    "date_limite_solde_f" date,
    "statut_f"            varchar(250) NOT NULL CHECK ((statut_f)::text = ANY
                                                       ((ARRAY ['ANTR'::character varying, 'ATR'::character varying, 'SOLDE'::character varying])::text[])),
    "date_solde_f"        date,
    "commentaire_admin_f" varchar(250),
    "commentaire_resp_f"  varchar(250),
    "numero_titre_f"      varchar(250),
    "annee_titre_f"       varchar(250),
    "imputation_f"        varchar(250),
    PRIMARY KEY ("id_f")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS financeur_id_financeur_seq;

-- Table Definition
CREATE TABLE "public"."financeur"
(
    "id_financeur"                   int4         NOT NULL DEFAULT nextval('financeur_id_financeur_seq'::regclass),
    "nom_financeur"                  varchar(250) NOT NULL,
    "ref_arret_attributif_financeur" varchar(250),
    PRIMARY KEY ("id_financeur")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS historique_id_h_seq;

-- Table Definition
CREATE TABLE "public"."historique"
(
    "id_h"          int4 NOT NULL DEFAULT nextval('historique_id_h_seq'::regclass),
    "id_u"          int4 NOT NULL,
    "date_h"        date NOT NULL,
    "description_h" varchar(250),
    "id_p"          int4 NOT NULL,
    PRIMARY KEY ("id_h")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS montant_affecte_id_ma_seq;

-- Table Definition
CREATE TABLE "public"."montant_affecte"
(
    "id_ma"      int4   NOT NULL DEFAULT nextval('montant_affecte_id_ma_seq'::regclass),
    "montant_ma" float8 NOT NULL,
    "annee_ma"   int4   NOT NULL,
    "id_r"       int4   NOT NULL,
    PRIMARY KEY ("id_ma")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS projet_id_p_seq;

-- Table Definition
CREATE TABLE "public"."projet"
(
    "id_p"     int4         NOT NULL DEFAULT nextval('projet_id_p_seq'::regclass),
    "code_p"   int4         NOT NULL,
    "nom_p"    varchar(250) NOT NULL,
    "statut_p" bool                  DEFAULT false,
    "id_u"     int4         NOT NULL,
    PRIMARY KEY ("id_p")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS recette_id_r_seq;

-- Table Definition
CREATE TABLE "public"."recette"
(
    "id_r"      int4   NOT NULL DEFAULT nextval('recette_id_r_seq'::regclass),
    "id_f"      int4   NOT NULL,
    "montant_r" float8 NOT NULL,
    "annee_r"   int4   NOT NULL,
    PRIMARY KEY ("id_r")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS recette_comptable_id_rc_seq;

-- Table Definition
CREATE TABLE "public"."recette_comptable"
(
    "id_rc"      int4   NOT NULL DEFAULT nextval('recette_comptable_id_rc_seq'::regclass),
    "montant_rc" float8 NOT NULL,
    "annee_rc"   int4   NOT NULL,
    PRIMARY KEY ("id_rc")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS revoked_tokens_id_seq;

-- Table Definition
CREATE TABLE "public"."revoked_tokens"
(
    "id"  int4 NOT NULL DEFAULT nextval('revoked_tokens_id_seq'::regclass),
    "jti" varchar(120),
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS role_acces_id_ra_seq;

-- Table Definition
CREATE TABLE "public"."role_acces"
(
    "id_ra"   int4         NOT NULL DEFAULT nextval('role_acces_id_ra_seq'::regclass),
    "nom_ra"  varchar(250) NOT NULL,
    "code_ra" int4         NOT NULL,
    PRIMARY KEY ("id_ra")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."role_utilisateur"
(
    "id_ra" int4 NOT NULL,
    "id_u"  int4 NOT NULL,
    PRIMARY KEY ("id_ra", "id_u")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS utilisateur_id_u_seq;

-- Table Definition
CREATE TABLE "public"."utilisateur"
(
    "id_u"        int4         NOT NULL DEFAULT nextval('utilisateur_id_u_seq'::regclass),
    "nom_u"       varchar(250),
    "prenom_u"    varchar(250),
    "initiales_u" varchar(3)   NOT NULL,
    "email_u"     varchar(250) NOT NULL,
    "password_u"  varchar(250) NOT NULL,
    "active_u"    bool                  DEFAULT true,
    PRIMARY KEY ("id_u")
);

INSERT INTO "public"."depense" ("id_d", "annee_d", "montant_d")
VALUES ('1', '2021', '4589');

INSERT INTO "public"."entree_sortie" ("id_es", "annee_recette_es", "annee_affectation_es", "montant_es")
VALUES ('1', '2021', '2021', '456'),
       ('2', '2021', '2022', '458');

INSERT INTO "public"."financement" ("id_f", "id_p", "id_financeur", "montant_arrete_f", "date_arrete_f",
                                    "date_limite_solde_f", "statut_f", "date_solde_f", "commentaire_admin_f",
                                    "commentaire_resp_f", "numero_titre_f", "annee_titre_f", "imputation_f")
VALUES ('1', '4', '1', '65329.95', '2017-05-02', '2020-09-24', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('2', '5', '1', '16506', '2019-04-29', '2020-03-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('3', '5', '1', '101001.5', '2019-04-02', '2022-09-30', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('4', '5', '1', '23187', '2020-05-25', '2021-03-30', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('5', '5', '1', '20907', NULL, NULL, 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('6', '6', '1', '11436.37', '2019-03-19', '2020-03-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('7', '6', '1', '58631.11', '2019-06-18', '2022-06-30', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('8', '6', '1', '10139', '2020-05-25', '2021-03-30', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('9', '6', '1', '12372.9', NULL, NULL, 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('10', '7', '1', '7000', '2018-02-14', '2019-02-13', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('11', '8', '1', '40000', '2019-03-11', '2022-12-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('12', '8', '1', '40000', '2019-11-18', '2022-12-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('13', '8', '1', '40000', '2019-11-14', '2022-12-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('14', '8', '1', '120000', '2019-08-08', '2022-06-30', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('15', '9', '1', '22170', '2020-01-28', '2022-04-15', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('16', '9', '1', '17149', '2020-04-27', '2022-08-14', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('17', '9', '1', '17149', NULL, NULL, 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('18', '9', '1', '95270', '2020-02-24', '2022-10-31', 'ATR', NULL, 'Données de tests !', '', '', '', ''),
       ('19', '10', '1', '50000', NULL, NULL, 'ANTR', NULL, '', '', '', '', '');

INSERT INTO "public"."financeur" ("id_financeur", "nom_financeur", "ref_arret_attributif_financeur")
VALUES ('1', 'CBNA', ''),
       ('2', 'MIAGE', 'Pour tests !');

INSERT INTO "public"."montant_affecte" ("id_ma", "montant_ma", "annee_ma", "id_r")
VALUES ('1', '1572', '2016', '1'),
       ('2', '5436.33', '2017', '1'),
       ('3', '19604.67', '2017', '2'),
       ('4', '12500.28', '2018', '2'),
       ('5', '483.72', '2018', '3'),
       ('6', '10628', '2019', '3'),
       ('7', '15104.95', '2020', '3'),
       ('8', '4951.8', '2019', '4'),
       ('9', '11554.2', '2019', '5'),
       ('10', '29390.77', '2019', '6'),
       ('11', '38646.5', '2020', '7'),
       ('12', '32964.23', '2021', '8'),
       ('13', '11593.5', '2020', '9'),
       ('14', '11593.5', '2020', '10'),
       ('15', '6272.1', '2021', '11'),
       ('16', '14634.9', '2021', '12'),
       ('17', '5232.51', '2019', '13'),
       ('18', '6203.86', '2019', '14'),
       ('19', '19060.61', '2019', '15'),
       ('20', '17641.5', '2020', '16'),
       ('21', '21929', '2021', '17'),
       ('22', '5069.5', '2020', '18'),
       ('23', '5069.5', '2020', '19'),
       ('24', '3711.87', '2021', '20'),
       ('25', '8661.02', '2021', '21'),
       ('26', '7000', '2018', '22'),
       ('27', '12000', '2019', '23'),
       ('28', '28000', '2019', '24'),
       ('29', '12000', '2020', '25'),
       ('30', '28000', '2020', '26'),
       ('31', '12000', '2021', '27'),
       ('32', '28000', '2021', '28'),
       ('33', '40000', '2019', '29'),
       ('34', '40000', '2020', '30'),
       ('35', '40000', '2021', '31'),
       ('36', '10258', '2020', '32'),
       ('37', '827', '2021', '32'),
       ('38', '9653', '2021', '33'),
       ('39', '1432', '2022', '33'),
       ('40', '3429.8', '2020', '34'),
       ('41', '12440.2', '2020', '35'),
       ('42', '1279', '2021', '35'),
       ('43', '3429.8', '2021', '36'),
       ('44', '11504', '2021', '37'),
       ('45', '2215.2', '2022', '37'),
       ('46', '44086', '2020', '38'),
       ('47', '45036', '2021', '39'),
       ('48', '6148', '2022', '40');

INSERT INTO "public"."projet" ("id_p", "code_p", "nom_p", "statut_p", "id_u")
VALUES ('4', '16025', 'Alcotra Resthalp', 'f', '4'),
       ('5', '18003', 'SCALP', 'f', '4'),
       ('6', '18004', 'ROCVEG', 'f', '4'),
       ('7', '18022', 'SILENE', 'f', '4'),
       ('8', '18059', 'Infloreb', 'f', '4'),
       ('9', '19017', 'Floreclim', 'f', '4'),
       ('10', '23000', 'test', 't', '5');

INSERT INTO "public"."recette" ("id_r", "id_f", "montant_r", "annee_r")
VALUES ('1', '1', '7008.33', '2017'),
       ('2', '1', '32104.95', '2019'),
       ('3', '1', '26216.67', '2020'),
       ('4', '2', '4951.8', '2019'),
       ('5', '2', '11554.2', '2020'),
       ('6', '3', '29390.77', '2020'),
       ('7', '3', '38646.5', '2021'),
       ('8', '3', '32964.23', '2022'),
       ('9', '4', '11593.5', '2020'),
       ('10', '4', '11593.5', '2021'),
       ('11', '5', '6272.1', '2021'),
       ('12', '5', '14634.9', '2022'),
       ('13', '6', '5232.51', '2019'),
       ('14', '6', '6203.86', '2020'),
       ('15', '7', '19060.61', '2020'),
       ('16', '7', '17641.5', '2021'),
       ('17', '7', '21929', '2022'),
       ('18', '8', '5069.5', '2020'),
       ('19', '8', '5069.5', '2021'),
       ('20', '9', '3711.87', '2021'),
       ('21', '9', '8661.02', '2022'),
       ('22', '10', '7000', '2018'),
       ('23', '11', '12000', '2019'),
       ('24', '11', '28000', '2020'),
       ('25', '12', '12000', '2019'),
       ('26', '12', '28000', '2021'),
       ('27', '13', '12000', '2019'),
       ('28', '13', '28000', '2022'),
       ('29', '14', '40000', '2020'),
       ('30', '14', '40000', '2021'),
       ('31', '14', '40000', '2022'),
       ('32', '15', '11085', '2020'),
       ('33', '15', '11085', '2022'),
       ('34', '16', '3429.8', '2020'),
       ('35', '16', '13719.2', '2021'),
       ('36', '17', '3429.8', '2021'),
       ('37', '17', '13719.2', '2022'),
       ('38', '18', '44086', '2021'),
       ('39', '18', '45036', '2022'),
       ('40', '18', '6148', '2023'),
       ('41', '19', '10000', '2023');

INSERT INTO "public"."recette_comptable" ("id_rc", "montant_rc", "annee_rc")
VALUES ('1', '4589', '2021');

INSERT INTO "public"."revoked_tokens" ("id", "jti")
VALUES ('1', '00b9efa3-14cb-4c9c-9fab-06f183ee370e'),
       ('2', '747d3907-6b18-40b2-861b-9bd70bb9558a'),
       ('3', 'ae58e01a-90f4-4b96-9516-e19a9ce5b902'),
       ('4', '47de7945-ca34-4d18-b945-e38a610e15d8'),
       ('5', '498605ac-6036-4c1a-8f64-4f5e98f5478e'),
       ('6', 'b357b595-cb5e-4c11-afe7-8f8ceff733eb'),
       ('7', '1cd1aed8-9d25-4e56-ac34-04ffe8cd1eec'),
       ('8', 'dfc45194-7275-40a6-80e0-7233a42837f3'),
       ('9', '9e261a27-466a-454a-90da-9755da31c9e9'),
       ('10', '699f8440-ab39-4d2d-bb4c-eef173612438'),
       ('11', '7f8d1f4f-582a-4d8a-9d48-1f424dfbdb94'),
       ('12', '6fb94052-51f9-45ed-ba3c-84ecfb9a1556'),
       ('13', 'f7344d8c-064b-4b23-b066-b92a58a25a16'),
       ('14', '50f160d8-9b3d-4ed6-9a82-18de627b8364'),
       ('15', '0c9c5fe2-ab0a-49ca-b6a5-d25dcda8c8c3'),
       ('16', 'a4f07062-74f5-4b2b-9a16-62b781a09d7d');

INSERT INTO "public"."role_acces" ("id_ra", "nom_ra", "code_ra")
VALUES ('1', 'administrateur', '2'),
       ('2', 'consultant', '1');

INSERT INTO "public"."role_utilisateur" ("id_ra", "id_u")
VALUES ('1', '4'),
       ('1', '24'),
       ('1', '25'),
       ('1', '42'),
       ('2', '1'),
       ('2', '2'),
       ('2', '3'),
       ('2', '4'),
       ('2', '5'),
       ('2', '6'),
       ('2', '7'),
       ('2', '8'),
       ('2', '9'),
       ('2', '10'),
       ('2', '11'),
       ('2', '12'),
       ('2', '13'),
       ('2', '14'),
       ('2', '15'),
       ('2', '16'),
       ('2', '17'),
       ('2', '18'),
       ('2', '19'),
       ('2', '20'),
       ('2', '21'),
       ('2', '22'),
       ('2', '23'),
       ('2', '24'),
       ('2', '25'),
       ('2', '26'),
       ('2', '27'),
       ('2', '28'),
       ('2', '29'),
       ('2', '30'),
       ('2', '31'),
       ('2', '32'),
       ('2', '33'),
       ('2', '34'),
       ('2', '35'),
       ('2', '36'),
       ('2', '37'),
       ('2', '38'),
       ('2', '39'),
       ('2', '40'),
       ('2', '41');

INSERT INTO "public"."utilisateur" ("id_u", "nom_u", "prenom_u", "initiales_u", "email_u", "password_u", "active_u")
VALUES ('1', 'LECLERE', 'Alisson', 'al', 'a.leclere@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('2', 'MERHAN', 'Baptiste', 'bm', 'b.merhan@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('3', 'BERTRAND', 'Bernard', 'bb', 'b.bertrand@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('4', 'LIENARD', 'Bertrand', 'bl', 'b.lienard@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('5', 'LAMBEY', 'Brigitte', 'bla', 'b.lambey@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('6', 'WINTER', 'Candice', 'cw', 'c.winter@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('7', 'PAULIN', 'David', 'dp', 'd.paulin@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('8', 'RATAJCZAK', 'Emilie', 'er', 'e.ratajczak@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('9', 'BLAIN', 'Emmanuelle', 'eb', 'e.blain@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('10', 'MARQUIS', 'Frédéric', 'fm', 'f.marquis@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('11', 'PACHE', 'Gilles', 'gp', 'g.pache@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('12', 'BOITE', 'Générale', 'gb', 'cbna@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('13', 'VILLARET', 'Jean-Charles', 'jcv', 'jc.villaret@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('14', 'GENIS', 'Jean-Michel', 'jmg', 'jm.genis@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('15', 'MILCENT', 'Jean-Pascal', 'jpm', 'jp.milcent@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('16', 'VAN ES', 'Jérémie', 'jve', 'j.van-es@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('17', 'MARIS', 'Louise', 'lm', 'l.maris@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('18', 'GARRAUD', 'Luc', 'lg', 'l.garraud@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('19', 'BONNET', 'Lucie', 'lb', 'l.bonnet@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('20', 'VAHE', 'Lucile', 'lv', 'l.vahe@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('21', 'LAPEBIE', 'Ludivine', 'll', 'l.lapebie@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('22', 'ALGLAVE', 'Lydie', 'la', 'l.alglave@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('23', 'BIZARD', 'Léa', 'lbd', 'l.bizard@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('24', 'ISENMANN', 'Marc', 'mi', 'm.isenmann@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('25', 'GILLIOT', 'Marianne', 'mg', 'm.gilliot@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('26', 'MARIE', 'Marie-Hélène', 'mhm', 'mh.marie@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('27', 'SPAETH', 'Martin', 'ms', 'm.spaeth@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('28', 'MICHOULIER', 'Mathieu', 'mm', 'm.michoulier@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('29', 'MOLINATTI', 'Myriam', 'mmi', 'm.molinatti@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('30', 'FORT', 'Noémie', 'nf', 'n.fort@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('31', 'KRISTO', 'Ornella', 'ok', 'o.kristo@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('32', 'administratif', 'partage', 'pa', 'partage@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('33', 'SEGURA', 'Paul', 'ps', 'p.segura@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('34', 'DEBAY', 'Pauline', 'pdy', 'p.debay@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('35', 'VALLEE', 'Sophie', 'sv', 's.vallee@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('36', 'BISSUEL', 'Sophie', 'sb', 's.bissuel@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('37', 'HUC', 'Stéphanie', 'sh', 's.huc@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('38', 'ABDULHAK', 'Sylvain', 'sa', 's.abdulhak@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('39', 'LEGLAND', 'Thomas', 'tl', 't.legland@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('40', 'FINIELS', 'Véronique', 'vf', 'v.finiels@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('41', 'BONNET', 'Véronique', 'vb', 'v.bonnet@cbn-alpin.fr',
        '$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', 't'),
       ('42', 'Azp', 'Manu', 'azp', 'tempor.05@gmail.com',
        '$pbkdf2-sha256$29000$LGXs3ZszBsC4l5IypnQOwQ$RMTcb0.Ltaj1JoN/r0O7q.gWGqF0XXKZF8Bfmw.8Hdo', 't');

CREATE OR REPLACE FUNCTION public.affectations_sur(anneeaffectation integer DEFAULT 0)
    RETURNS TABLE
            (
                id_ma             integer,
                id_r              integer,
                id_es             integer,
                montant           double precision,
                annee_recette     integer,
                annee_affectation integer
            )
    LANGUAGE plpgsql
AS
$function$
DECLARE
BEGIN
    -- Liste des montants affectés sur l'année en paramètre
    RETURN
        QUERY
        SELECT ma.id_ma,
               r.id_r,
               0          id_es,
               montant_ma montant,
               annee_r    annee_recette,
               annee_ma   annee_affectation
        FROM montant_affecte ma
                 NATURAL JOIN recette r
        WHERE ma.annee_ma = anneeAffectation
           OR anneeAffectation = 0
        UNION
        SELECT 0                    id_ma,
               0                    id_r,
               es.id_es,
               montant_es           montant,
               annee_recette_es     annee_recette,
               annee_affectation_es annee_affectation
        FROM entree_sortie es
        WHERE annee_affectation_es = anneeAffectation
           OR anneeAffectation = 0;
END;
$function$;
CREATE OR REPLACE FUNCTION public.bilan_financier(anneeref integer)
    RETURNS TABLE
            (
                annee_recette     integer,
                montant_recette   double precision,
                affectation_avant double precision,
                affectation_a     double precision,
                affectation_a2    double precision,
                affectation_a3    double precision,
                affectation_a4    double precision,
                affectation_a5    double precision,
                affectation_apres double precision
            )
    LANGUAGE plpgsql
AS
$function$

BEGIN
    CREATE TEMP TABLE affectations
    (
        id_ma             integer, -- Identifiant du montant affecté (à 0 si la donnée vient de 'entree_sortie')
        id_r              integer, -- Identifiant de la recette (à 0 si la donnée vient de 'entree_sortie')
        id_es             integer, -- Identifiant de l'entrée/sortie (à 0 si la donnée vient de 'affectation')
        montant           double precision,
        annee_recette     integer,
        annee_affectation integer
    ) on commit drop;

    INSERT INTO affectations
    SELECT *
    FROM affectations_sur();

    -- Tableau 1 du bilan financier
    RETURN
        QUERY
        SELECT 0                                    annee_recette,
               0                                    montant_recette,
               0                                    affectation_avant,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef
                  AND aff.annee_recette < anneeRef) affectation_a,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 1
                  AND aff.annee_recette < anneeRef) affectation_a2,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 2
                  AND aff.annee_recette < anneeRef) affectation_a3,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 3
                  AND aff.annee_recette < anneeRef) affectation_a4,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 4
                  AND aff.annee_recette < anneeRef) affectation_a5,
               0                                    affectation_apres
        UNION
        SELECT annees.annee                                                                         annee_recette,
               (SELECT COALESCE(sum(r.montant_r), 0) FROM recette r WHERE r.annee_r = annees.annee) montant_recette,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation < anneeRef
                  AND aff.annee_recette = annees.annee)                                             affectation_avant,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef
                  AND aff.annee_recette = annees.annee)                                             affectation_a,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 1
                  AND aff.annee_recette = annees.annee)                                             affectation_a2,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 2
                  AND aff.annee_recette = annees.annee)                                             affectation_a3,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 3
                  AND aff.annee_recette = annees.annee)                                             affectation_a4,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation = anneeRef + 4
                  AND aff.annee_recette = annees.annee)                                             affectation_a5,
               (SELECT COALESCE(sum(aff.montant), 0)
                FROM affectations aff
                WHERE aff.annee_affectation > anneeRef + 4
                  AND aff.annee_recette = annees.annee)                                             affectation_apres
        FROM (SELECT annee_r annee FROM recette GROUP BY annee_r ORDER BY annee_r) annees;
END;
$function$;
CREATE OR REPLACE FUNCTION public.check_financement_montant()
    RETURNS trigger
    LANGUAGE plpgsql
AS
$function$
BEGIN
    IF NEW.montant_arrete_f < (SELECT COALESCE(SUM(r.montant_r), 0) FROM recette r WHERE r.id_f = NEW.id_f) THEN
        RAISE EXCEPTION 'Le montant d''un financement ne peut pas être inférieur au montants de ses recettes';
    END IF;

    RETURN NEW;
END;
$function$;
CREATE OR REPLACE FUNCTION public.check_montantaffecte_montant()
    RETURNS trigger
    LANGUAGE plpgsql
AS
$function$
BEGIN
    IF (SELECT r.montant_r FROM recette r WHERE r.id_r = NEW.id_r) < NEW.montant_ma +
                                                                     (SELECT COALESCE(SUM(ma.montant_ma), 0)
                                                                      FROM montant_affecte ma
                                                                      WHERE ma.id_r = NEW.id_r
                                                                        AND ma.id_ma != NEW.id_ma) THEN
        RAISE EXCEPTION 'Le montant d''une recette ne peut pas être inférieur au montants de ses affectations';
    END IF;

    RETURN NEW;
END;
$function$;
CREATE OR REPLACE FUNCTION public.check_recette_montant()
    RETURNS trigger
    LANGUAGE plpgsql
AS
$function$
BEGIN
    IF NEW.montant_r < (SELECT COALESCE(SUM(ma.montant_ma), 0) FROM montant_affecte ma WHERE ma.id_r = NEW.id_r) THEN
        RAISE EXCEPTION 'Le montant d''une recette ne peut pas être inférieur au montants de ses affectations';
    END IF;

    RETURN NEW;
END;
$function$;
CREATE OR REPLACE FUNCTION public.check_recette_somme_montant()
    RETURNS trigger
    LANGUAGE plpgsql
AS
$function$
BEGIN
    IF (SELECT f.montant_arrete_f FROM financement f WHERE f.id_f = NEW.id_f) < NEW.montant_r +
                                                                                (SELECT COALESCE(SUM(r.montant_r), 0)
                                                                                 FROM recette r
                                                                                 WHERE r.id_f = NEW.id_f
                                                                                   AND r.id_r != NEW.id_r) THEN
        RAISE EXCEPTION 'Le montant d''un financement ne peut pas être inférieur au montants de ses recettes';
    END IF;

    RETURN NEW;
END;
$function$;
CREATE OR REPLACE FUNCTION public.suivi_financement(versionft integer, anneeref integer, anneemax integer DEFAULT 0)
    RETURNS TABLE
            (
                id_p                integer,
                code_p              integer,
                nom_p               character varying,
                id_u                integer,
                initiales_u         character varying,
                id_f                integer,
                date_arrete_f       date,
                date_limite_solde_f date,
                montant_arrete_f    double precision,
                commentaire_admin_f character varying,
                imputation_f        character varying,
                numero_titre_f      character varying,
                statut_f            character varying,
                id_financeur        integer,
                nom_financeur       character varying,
                recette_avant       double precision,
                recette_a           double precision,
                recette_a2          double precision,
                recette_a3          double precision,
                recette_a4          double precision,
                recette_a5          double precision,
                recette_apres       double precision
            )
    LANGUAGE plpgsql
AS
$function$
DECLARE
    codeAnneeMin integer;
    codeAnneeMax integer;
BEGIN
    CREATE TEMP TABLE temp_id
    (
        id_f integer
    ) on commit drop;

    -- Sélection des financements à analyser
    IF versionFt = 1 THEN -- Version 1 basée sur les statuts des financements
        BEGIN
            RAISE INFO 'Version 1 - année %', anneeRef;

            INSERT INTO temp_id(id_f)
            SELECT f.id_f
            FROM financement f
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
            SELECT f.id_f
            FROM projet p
                     NATURAL JOIN financement f
            WHERE p.code_p >= codeAnneeMin
              AND p.code_p <= codeAnneeMax;
        END;
    END IF;

    -- Tableau du suivi des financements
    RETURN
        QUERY SELECT p.id_p,
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
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r < anneeRef)     recette_avant,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r = anneeRef)     recette_a,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r = anneeRef + 1) recette_a2,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r = anneeRef + 2) recette_a3,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r = anneeRef + 3) recette_a4,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r = anneeRef + 4) recette_a5,
                     (SELECT COALESCE(SUM(montant_r), 0)
                      FROM recette r
                      WHERE r.id_f = f.id_f AND r.annee_r > anneeRef + 4) recette_apres
              FROM projet p
                       NATURAL JOIN utilisateur u
                       INNER JOIN financement f ON f.id_p = p.id_p
                       LEFT JOIN financeur feur ON feur.id_financeur = f.id_financeur
              WHERE f.id_f IN (SELECT ti.id_f FROM temp_id ti);
END;
$function$;
ALTER TABLE "public"."financement"
    ADD FOREIGN KEY ("id_p") REFERENCES "public"."projet" ("id_p");
ALTER TABLE "public"."financement"
    ADD FOREIGN KEY ("id_financeur") REFERENCES "public"."financeur" ("id_financeur");
ALTER TABLE "public"."historique"
    ADD FOREIGN KEY ("id_u") REFERENCES "public"."utilisateur" ("id_u");
ALTER TABLE "public"."montant_affecte"
    ADD FOREIGN KEY ("id_r") REFERENCES "public"."recette" ("id_r");
ALTER TABLE "public"."projet"
    ADD FOREIGN KEY ("id_u") REFERENCES "public"."utilisateur" ("id_u");
ALTER TABLE "public"."role_utilisateur"
    ADD FOREIGN KEY ("id_u") REFERENCES "public"."utilisateur" ("id_u");
ALTER TABLE "public"."role_utilisateur"
    ADD FOREIGN KEY ("id_ra") REFERENCES "public"."role_acces" ("id_ra");
