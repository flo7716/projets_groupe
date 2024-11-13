CREATE TABLE ASSOCIATION(
    idAsso VARCHAR(255) NOT NULL,
    nomAsso VARCHAR(255) NOT NULL,
    domaineAsso VARCHAR(255) NOT NULL,
    PRIMARY KEY(idAsso)
)


CREATE TABLE EVENEMENT_ORGANISE_PAR_ASSO(
    idAsso VARCHAR(255) NOT NULL,
    idEvent VARCHAR(255) NOT NULL,
    dateEvent DATE NOT NULL,
    descriptionEvent VARCHAR(255) NOT NULL,
    PRIMARY KEY(idAsso, idEvent),
    FOREIGN KEY(idAsso) REFERENCES ASSOCIATION(idAsso),
    FOREIGN KEY(idEvent) REFERENCES EVENEMENT(idEvent)
)






