create table role_acces
(
    id_ra   serial       not null
        constraint pk_ra
            primary key,
    nom_ra  varchar(250) not null,
    code_ra serial       not null
);

alter table role_acces
    owner to hello_flask;

INSERT INTO public.role_acces (id_ra, nom_ra, code_ra)
VALUES (1, 'administrateur', 1);
INSERT INTO public.role_acces (id_ra, nom_ra, code_ra)
VALUES (2, 'consultant', 2);
