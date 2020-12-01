create table historique
(
    id_h          serial  not null
        constraint pk_h
            primary key,
    id_u          integer not null
        constraint fk_h_utilisateur
            references utilisateur,
    date_h        date    not null,
    description_h varchar(250),
    id_p          integer not null
        constraint fk_h_projet
            references projet
);

alter table historique
    owner to hello_flask;

create index ux_historique
    on historique (id_u, id_p);

