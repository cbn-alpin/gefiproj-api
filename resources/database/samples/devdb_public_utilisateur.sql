create table utilisateur
(
    id_u        serial       not null
        constraint pk_u
            primary key,
    nom_u       varchar(250),
    prenom_u    varchar(250),
    initiales_u varchar(3)   not null
        constraint utilisateur_initiales_u_key
            unique,
    email_u     varchar(250) not null
        constraint utilisateur_email_u_key
            unique,
    password_u  varchar(250) not null,
    active_u    boolean default true
);

alter table utilisateur
    owner to hello_flask;

INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, active_u)
VALUES (1, 'monnom', 'super', 'ms', 'testmaill@mail.ml',
        '$pbkdf2-sha256$29000$fo8xBsD4f6.1FiLEeK/V.g$tAVL90p3.1hZilV7vDVci2hywMdoGrE5nVnFWsmtW4A', true);
INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, active_u)
VALUES (4, 'monnom', 'super', 'msu', 'testimaill@mail.ml',
        '$pbkdf2-sha256$29000$sDYm5BzD2Ns7R8gZg/C.Vw$3z88ckd3MUppg2.c4PNYt168pf4Ts8Sa7rrRpqB7iwE', true);
