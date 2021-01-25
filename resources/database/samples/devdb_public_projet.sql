create table projet
(
    id_p     serial       not null
        constraint pk_p
            primary key,
    code_p   integer      not null
        constraint projet_code_p_key
            unique,
    nom_p    varchar(250) not null
        constraint projet_nom_p_key
            unique,
    statut_p boolean default false,
    id_u     integer      not null
        constraint fk_p_responsable
            references utilisateur
);

alter table projet
    owner to hello_flask;

create index ux_projet
    on projet (id_u);

INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (1, '210000', 'projet test 1', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (2, '210002', 'CBNA', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (4, '210004', 'CBNA Test', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (5, '210035', 'CBNA 2', false, 1);
INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u)
VALUES (6, '210001', 'test project', false, 1);
