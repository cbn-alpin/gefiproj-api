INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, active_u)
VALUES (
        1,
        'monnom',
        'super',
        'ms',
        'testmaill@mail.ml',
        '$pbkdf2-sha256$29000$QKhVqtX6v1eqlXLOmVOqNQ$H8Cix.p0L.53d8xxZGiOzo/THNXjbAQTC1Nt6ymNpaU', -- gefiproj
        true
);
INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, active_u)
VALUES (
        4,
        'monnom',
        'super',
        'msu',
        'testimaill@mail.ml',
        '$pbkdf2-sha256$29000$QKhVqtX6v1eqlXLOmVOqNQ$H8Cix.p0L.53d8xxZGiOzo/THNXjbAQTC1Nt6ymNpaU', -- gefiproj
        true
);

INSERT INTO public.financeur (id_financeur, nom_financeur, ref_arret_attributif_financeur)
VALUES (1, 'MIAGE', null);

INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (1, 'COCO', 'projet test 1', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (2, 'COC2', 'CBNA', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (4, 'CO34', 'CBNA Test', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (5, 'CO35', 'CBNA 2', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (6, 'test', 'test project', false, 1);

INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (3, 1, 1, 44344, null, null, 'ANTR', '2010-05-01', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (5, 1, 1, 44344, null, null, 'ANTR', '2010-05-01', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (17, 2, 1, 0, '2018-06-29', null, 'ANTR', '2018-06-29', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (18, 2, 1, 10, '2018-06-29', null, 'ANTR', '2018-06-29', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (19, 2, 1, 40, '2018-06-29', null, 'ANTR', '2018-06-29', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (22, 2, 1, 40, '2018-06-29', null, 'ANTR', '2018-06-29', null, null, null, null, null);
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (34, 1, 1, 3333, null, null, 'ANTR', '2020-11-11', '', '', '', '', '');
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (35, 1, 1, 343, null, null, 'ANTR', '2020-11-11', '', '', '', '', '');
INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, date_arrete_f, date_limite_solde_f,
                                statut_f, date_solde_f, commentaire_admin_f, commentaire_resp_f, numero_titre_f,
                                annee_titre_f, imputation_f)
VALUES (16, 1, 1, 0, '2018-06-29', null, 'ANTR', '2020-11-10', null, null, null, null, null);
