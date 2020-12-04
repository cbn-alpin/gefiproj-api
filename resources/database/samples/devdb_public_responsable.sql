create table responsable
(
    id_responsable        serial not null
        constraint pk_responsable
            primary key,
    initiales_responsable text
        constraint initiales_chck
            check (char_length(initiales_responsable) <= 3),
    nom_responsable       text,
    prenom_responsable    text,
    statut_responsable    text
);

alter table responsable
    owner to hello_flask;

