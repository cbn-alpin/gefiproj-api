create table financement
(
    id_f                serial           not null
        constraint pk_f
            primary key,
    id_p                integer          not null
        constraint fk_f_p
            references projet,
    id_financeur        integer          not null
        constraint fk_f_f
            references financeur,
    montant_arrete_f    double precision not null,
    date_arrete_f       date,
    date_limite_solde_f date,
    statut_f            varchar(250)     not null
        constraint ck_statut
            check ((statut_f)::text = ANY
                   ((ARRAY ['ANTR'::character varying, 'ATR'::character varying, 'SOLDE'::character varying])::text[])),
    date_solde_f        date,
    commentaire_admin_f varchar(250),
    commentaire_resp_f  varchar(250),
    numero_titre_f      varchar(250),
    annee_titre_f       varchar(250),
    imputation_f        varchar(250)
);

alter table financement
    owner to hello_flask;

create index ux_financement
    on financement (id_p, id_financeur);

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
