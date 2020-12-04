create table role_utilisateur
(
    id_ra integer not null
        constraint pk_role
            references role_acces,
    id_u  integer not null
        constraint pk_utilisateur
            references utilisateur,
    constraint pk_id_role_utilisateur
        primary key (id_ra, id_u)
);

alter table role_utilisateur
    owner to hello_flask;

create unique index ux_role_utilisateur
    on role_utilisateur (id_ra, id_u);

