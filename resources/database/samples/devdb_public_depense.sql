create table depense
(
    id_d      serial           not null
        constraint pk_d
            primary key,
    annee_d   integer          not null
        constraint depense_annee_d_key
            unique,
    montant_d double precision not null
);

alter table depense
    owner to hello_flask;

