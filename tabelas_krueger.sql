CREATE TABLE Frota_Veiculo (
    id_veiculo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(8) NOT NULL UNIQUE,
    modelo VARCHAR(80) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    ano_fabricacao SMALLINT UNSIGNED NOT NULL,
    km_atual INT UNSIGNED NOT NULL DEFAULT 0,
    status_veiculo ENUM('Disponivel','Em Viagem','Em Manutencao') NOT NULL DEFAULT 'Disponivel'
);

CREATE TABLE Aprovacao (
    id_aprovacao INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_viagem INT UNSIGNED NOT NULL,
    id_gestor VARCHAR(20) NOT NULL,
    data_hora_avaliacao DATETIME NOT NULL,
    status_decisao ENUM('Aprovado','Rejeitado') NOT NULL,
    observacoes_justificativa     TEXT,
    CONSTRAINT fk_aprovacao_viagem FOREIGN KEY (id_viagem) REFERENCES Viagem(id_viagem) ON DELETE CASCADE,
    CONSTRAINT fk_aprovacao_gestor FOREIGN KEY (id_gestor) REFERENCES Colaborador(id_colaborador)
);