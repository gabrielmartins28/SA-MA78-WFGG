create TABLE departamentos(
    id_departamento int PRIMARY key AUTO_INCREMENT,
    nome_departamento varchar(20),
    orcamento_departamento DECIMAL(10,2)
);


CREATE Table colaborador(
    id_colaborador int PRIMARY key AUTO_INCREMENT,
    nome_colaborador VARCHAR(30),
    email_colaborador VARCHAR(40) UNIQUE,
    telefone_colaborador INT UNIQUE,
    cargo_funcionario VARCHAR(15),
    status_funcionario ENUM("Ativo", "Inativo"),
    possui_cnh BOOLEAN not null DEFAULT false


);

CREATE Table Viagem(
    id_viagem int PRIMARY KEY AUTO_INCREMENT
    dia_saida date,
    dia_retorno date,
    id_colaborador int,--------------
    justificativa_viagem varchar(100),
    destino_viagem varchar(30),
    status_viagem enum("Pendente", "Aprovada", "Em andamento", "Concluída", "Cancelada" ),

);

CREATE table analise_eficacia_viagem(
    id_analise int PRIMARY key AUTO_INCREMENT,
    data_analise date,
    id_viagem int,---------------
    id_colaborador int, ----------------
    indicador_sucesso enum("1","2","3","4","5"),
    observacao_colaborador varchar(100)

);
