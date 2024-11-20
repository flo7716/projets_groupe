CREATE TABLE ASSOCIATION(
    idAsso VARCHAR(255) NOT NULL,
    nomAsso VARCHAR(255) NOT NULL,
    domaineAsso VARCHAR(255) NOT NULL,
    PRIMARY KEY(idAsso)
);


CREATE TABLE EVENEMENT_ORGANISE_PAR_ASSO(
    idAsso VARCHAR(255) NOT NULL,
    idEvent VARCHAR(255) NOT NULL,
    dateEvent DATE NOT NULL,
    lieuEvent VARCHAR(255) NOT NULL,
    descriptionEvent VARCHAR(255) NOT NULL,
    PRIMARY KEY(idAsso, idEvent),
    FOREIGN KEY(idAsso) REFERENCES ASSOCIATION(idAsso)
);


CREATE TABLE ENTREPRISE(
    idEntreprise VARCHAR(255) NOT NULL,
    nomEntreprise VARCHAR(255) NOT NULL,
    domaineEntreprise VARCHAR(255) NOT NULL,
    PRIMARY KEY(idEntreprise)
);


CREATE TABLE EVENEMENT_ORGANISE_PAR_ENTREPRISE(
    idEntreprise VARCHAR(255) NOT NULL,
    idEvent VARCHAR(255) NOT NULL,
    dateEvent DATE NOT NULL,
    lieuEvent VARCHAR(255) NOT NULL,
    descriptionEvent VARCHAR(255) NOT NULL,
    PRIMARY KEY(idEntreprise, idEvent),
    FOREIGN KEY(idEntreprise) REFERENCES ENTREPRISE(idEntreprise)
);






