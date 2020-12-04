create table role
(
    id_role  serial not null
        constraint pk_role
            primary key,
    nom_role text
);

alter table role
    owner to hello_flask;

