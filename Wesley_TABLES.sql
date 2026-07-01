CREATE TABLE Objetivo_Viagem (
    id_objetivo INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE Despesa (
    id_despesa INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    data_hora DATETIME NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL
);

