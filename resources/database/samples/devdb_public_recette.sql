create table recette
(
    id_r      serial           not null
        constraint pk_r
            primary key,
    id_f      integer          not null
        constraint fk_recette_financement
            references financement,
    montant_r double precision not null,
    annee_r   integer          not null
);

alter table recette
    owner to hello_flask;

create index ux_recette
    on recette (id_f);

