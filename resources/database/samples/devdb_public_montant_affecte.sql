create table montant_affecte
(
    id_ma      serial           not null
        constraint pk_ma
            primary key,
    montant_ma double precision not null,
    annee_ma   integer          not null,
    id_r       integer          not null
        constraint fk_ma_recette
            references recette
);

alter table montant_affecte
    owner to hello_flask;

create index ux_montant_affecte
    on montant_affecte (id_r);

