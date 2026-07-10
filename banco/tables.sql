-- Active: 1783533724186@@mysql-20e679b3-sama78wfgg.b.aivencloud.com@15321@Sistema_interno_Viagens
create TABLE departamentos(
    id_departamento int PRIMARY key AUTO_INCREMENT,
    nome_departamento varchar(20),
    orcamento_departamento DECIMAL(10,2)
);


CREATE Table colaborador(
    id_colaborador int PRIMARY key AUTO_INCREMENT,
    nome_colaborador VARCHAR(30),
    email_colaborador VARCHAR(40) UNIQUE,
    telefone_colaborador varchar(15) UNIQUE,
    cargo_funcionario VARCHAR(15),
    status_funcionario ENUM('Ativo', 'Inativo'),
    possui_cnh BOOLEAN not null DEFAULT True,
    id_departamento int,
    id_gestor int,

    Foreign Key (id_departamento) REFERENCES departamentos(id_departamento),
    Foreign Key (id_gestor) REFERENCES colaborador(id_colaborador)

);

CREATE TABLE Objetivo_Viagem (
    id_objetivo INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE Frota_Veiculo (
    id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(8) NOT NULL UNIQUE,
    modelo VARCHAR(80) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    capacidade_passageiros int not null,
    km_atual INT UNSIGNED NOT NULL DEFAULT 0,
    status_veiculo ENUM('Disponivel','Em Viagem','Em Manutencao') NOT NULL DEFAULT 'Disponivel'
);


CREATE Table Viagem(
    id_viagem int PRIMARY KEY AUTO_INCREMENT,
    dia_saida DATETIME,
    dia_retorno DATETIME,
    id_colaborador int,
    justificativa_viagem varchar(100),
    destino_viagem varchar(30),
    status_viagem enum('Pendente', 'Aprovada', 'Em andamento', 'Concluída', 'Cancelada'),
    id_objetivo int not null,
    id_veiculo int,

    Foreign Key (id_colaborador) REFERENCES colaborador(id_colaborador),
    Foreign Key (id_objetivo) REFERENCES Objetivo_Viagem(id_objetivo),
    Foreign Key (id_veiculo) REFERENCES Frota_Veiculo(id_veiculo)
);

CREATE table analise_eficacia_viagem(
    id_analise int PRIMARY key AUTO_INCREMENT,
    data_analise date,
    id_viagem int UNIQUE,
    id_colaborador int,
    indicador_sucesso enum('1','2','3','4','5'),
    observacao_colaborador varchar(100),

    Foreign Key (id_viagem) REFERENCES Viagem(id_viagem),
    Foreign Key (id_colaborador) REFERENCES colaborador(id_colaborador)
);


CREATE TABLE Despesas (
    id_despesas INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    data_hora DATETIME NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL,
    id_viagem int,

    Foreign Key (id_viagem) REFERENCES Viagem(id_viagem)
);


CREATE TABLE Aprovacao (
    id_aprovacao INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_viagem INT NOT NULL,
    id_colaborador int NOT NULL,
    data_hora_avaliacao DATETIME NOT NULL,
    status_decisao ENUM('Aprovado','Rejeitado') NOT NULL,
    observacoes_justificativa TEXT,

    Foreign Key (id_viagem) REFERENCES Viagem(id_viagem),
    Foreign Key (id_colaborador) REFERENCES colaborador(id_colaborador)
  
);

CREATE table Carona(
    id_carona int PRIMARY key AUTO_INCREMENT,
    id_viagem int,
    id_colaborador int,

    Foreign Key (id_viagem) REFERENCES Viagem(id_viagem),
    Foreign Key (id_colaborador) REFERENCES colaborador(id_colaborador)

);