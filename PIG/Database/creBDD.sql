CREATE TABLE ASSOCIATION(
    nomAsso VARCHAR(255) NOT NULL,       -- nomAsso devient la clé primaire
    domaineAsso VARCHAR(255) NOT NULL,
    PRIMARY KEY(nomAsso)                 -- nomAsso est la clé primaire
);

CREATE TABLE EVENEMENT_ORGANISE_PAR_ASSO(
    shortCode VARCHAR(255) NOT NULL,
    nomAsso VARCHAR(255) NOT NULL,       -- nomAsso est une clé étrangère
    descriptionEvent VARCHAR(255) NOT NULL,
    PRIMARY KEY(shortCode),
    FOREIGN KEY(nomAsso) REFERENCES ASSOCIATION(nomAsso)   -- Référence à nomAsso
);
