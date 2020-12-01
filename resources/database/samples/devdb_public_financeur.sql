create table financeur
(
    id_financeur                   serial       not null
        constraint pk_financeur
            primary key,
    nom_financeur                  varchar(250) not null
        constraint financeur_nom_financeur_key
            unique,
    ref_arret_attributif_financeur varchar(250)
);

alter table financeur
    owner to hello_flask;

INSERT INTO public.financeur (id_financeur, nom_financeur, ref_arret_attributif_financeur)
VALUES (1, 'MIAGE', null);
