-- Active: 1783459483750@@mysql-20e679b3-sama78wfgg.b.aivencloud.com@15321@Sistema_interno_Viagens

#Relatório de Eficácia (ROI): Viagens que "deram ruim"
-- ==============================================================================
SELECT 
    v.id_viagem,
    v.destino_viagem,
    c.nome_colaborador AS solicitante,
    obj.descricao AS objetivo_da_viagem,
    aev.indicador_sucesso AS nota_avaliacao,
    aev.observacao_colaborador
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN Objetivo_Viagem obj ON v.id_objetivo = obj.id_objetivo
JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
WHERE aev.indicador_sucesso <= 2
ORDER BY aev.indicador_sucesso ASC;


#Relatório Financeiro: Custo total de viagens por Departamento
-- ==============================================================================
SELECT 
    d.nome_departamento,
    COUNT(DISTINCT v.id_viagem) AS total_viagens,
    SUM(desp.valor) AS gasto_total_reais
FROM departamentos d
JOIN colaborador c ON d.id_departamento = c.id_departamento
JOIN Viagem v ON c.id_colaborador = v.id_colaborador
JOIN Despesas desp ON v.id_viagem = desp.id_viagem
GROUP BY d.nome_departamento
ORDER BY gasto_total_reais DESC;

#Onde a empresa gasta mais?
-- ==============================================================================
SELECT categoria, SUM(valor) AS gasto_total, COUNT(id_despesas) AS qtd_lancamentos
FROM Despesas
GROUP BY categoria
ORDER BY gasto_total DESC;

#As 5 viagens mais caras da história da empresa
-- ==============================================================================
SELECT v.id_viagem, v.destino_viagem, c.nome_colaborador, SUM(d.valor) AS custo_total
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN Despesas d ON v.id_viagem = d.id_viagem
GROUP BY v.id_viagem, v.destino_viagem, c.nome_colaborador
ORDER BY custo_total DESC
LIMIT 5;

#Orçamento do Departamento vs. Gasto com Viagens
-- ==============================================================================
SELECT 
    d.nome_departamento, 
    d.orcamento_departamento, 
    IFNULL(SUM(desp.valor), 0) AS total_gasto,
    (d.orcamento_departamento - IFNULL(SUM(desp.valor), 0)) AS saldo_restante
FROM departamentos d
LEFT JOIN colaborador c ON d.id_departamento = c.id_departamento
LEFT JOIN Viagem v ON c.id_colaborador = v.id_colaborador
LEFT JOIN Despesas desp ON v.id_viagem = desp.id_viagem
GROUP BY d.id_departamento, d.nome_departamento, d.orcamento_departamento
ORDER BY total_gasto DESC;

#Formas de pagamento mais utilizadas
-- ==============================================================================
SELECT forma_pagamento, COUNT(*) AS quantidade_uso, SUM(valor) AS volume_reais
FROM Despesas
GROUP BY forma_pagamento
ORDER BY quantidade_uso DESC;

#Média de gasto por viagem (Ticket Médio)
-- ==============================================================================
SELECT ROUND(AVG(custo_por_viagem), 2) AS media_gasto_por_viagem
FROM (
    SELECT id_viagem, SUM(valor) AS custo_por_viagem
    FROM Despesas
    GROUP BY id_viagem
) AS subconsulta;

#RANKING DOS VEÍCULOS MAIS UTILIZADOS
-- ==============================================================================
SELECT f.placa, f.modelo, COUNT(v.id_viagem) AS total_viagens
FROM Frota_Veiculo f
JOIN Viagem v ON f.id_veiculo = v.id_veiculo
GROUP BY f.id_veiculo, f.placa, f.modelo
ORDER BY total_viagens DESC;

#VIAGENS FEITAS SEM VEÍCULO DA FROTA (Carro próprio, avião, ônibus)
-- ==============================================================================
SELECT id_viagem, destino_viagem, dia_saida, status_viagem
FROM Viagem
WHERE id_veiculo IS NULL;

#TOP 5 VEÍCULOS MAIS RODADOS DA EMPRESA (Km Atual)
-- ==============================================================================
SELECT placa, modelo, marca, km_atual 
FROM Frota_Veiculo
ORDER BY km_atual DESC
LIMIT 5;

#VEÍCULOS QUE ESTÃO DISPONÍVEIS NO MOMENTO
-- ==============================================================================
SELECT placa, modelo, status_veiculo
FROM Frota_Veiculo
WHERE status_veiculo != 'Disponivel';

#CAPACIDADE OCIOSA DA FROTA 
-- Veículos grandes usados para poucas pessoas (Cruza capacidade com passageiros)
-- ==============================================================================
SELECT 
    v.id_viagem, f.modelo, f.capacidade_passageiros,
    (1 + (SELECT COUNT(*) FROM Carona c WHERE c.id_viagem = v.id_viagem)) AS total_ocupantes
FROM Viagem v
JOIN Frota_Veiculo f ON v.id_veiculo = f.id_veiculo
HAVING total_ocupantes < f.capacidade_passageiros;

#QUANTIDADE DE VIAGENS SOLICITADAS POR CADA COLABORADOR
-- ==============================================================================
SELECT c.nome_colaborador, d.nome_departamento, COUNT(v.id_viagem) AS qtd_viagens
FROM colaborador c
JOIN departamentos d ON c.id_departamento = d.id_departamento
LEFT JOIN Viagem v ON c.id_colaborador = v.id_colaborador
GROUP BY c.id_colaborador, c.nome_colaborador, d.nome_departamento
ORDER BY qtd_viagens DESC;

#QUEM SÃO OS CHEFES/GESTORES DA EMPRESA? (Auto-relacionamento em ação)
-- Lista apenas os funcionários que têm outras pessoas respondendo a eles.
-- ==============================================================================
SELECT DISTINCT gestor.nome_colaborador AS nome_gestor, gestor.cargo_funcionario
FROM colaborador funcionario
JOIN colaborador gestor ON funcionario.id_gestor = gestor.id_colaborador;

#LISTA DE SUBORDINADOS DE UM GESTOR ESPECÍFICO (Exemplo: id_gestor = 1)
-- ==============================================================================
SELECT nome_colaborador, cargo_funcionario, email_colaborador
FROM colaborador
WHERE id_gestor = 1;

#COLABORADORES ATIVOS QUE DEPENDEM DE CARONA (Não possuem CNH)
-- ==============================================================================
SELECT nome_colaborador, cargo_funcionario, telefone_colaborador
FROM colaborador
WHERE possui_cnh = FALSE AND status_funcionario = 'Ativo';

#QUANTAS CARONAS CADA COLABORADOR JÁ PEGOU
-- ==============================================================================
SELECT c.nome_colaborador, COUNT(car.id_carona) AS vezes_que_pegou_carona
FROM colaborador c
JOIN Carona car ON c.id_colaborador = car.id_colaborador
GROUP BY c.id_colaborador, c.nome_colaborador
ORDER BY vezes_que_pegou_carona DESC;


#HISTÓRICO DE VIAGENS REJEITADAS E O MOTIVO
-- ==============================================================================
SELECT v.id_viagem, c.nome_colaborador AS solicitante, a.observacoes_justificativa AS motivo_rejeicao
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN Aprovacao a ON v.id_viagem = a.id_viagem
WHERE a.status_decisao = 'Rejeitado';

#OBJETIVOS DE VIAGEM MAIS COMUNS (Por que a empresa viaja tanto?)
-- ==============================================================================
SELECT o.descricao AS objetivo, COUNT(v.id_viagem) AS total_solicitacoes
FROM Objetivo_Viagem o
JOIN Viagem v ON o.id_objetivo = v.id_objetivo
GROUP BY o.id_objetivo, o.descricao
ORDER BY total_solicitacoes DESC;

#MÉDIA DA NOTA DE EFICÁCIA POR DEPARTAMENTO
-- Avalia qual setor faz viagens mais "úteis" e eficientes para a empresa.
-- ==============================================================================
SELECT d.nome_departamento, ROUND(AVG(aev.indicador_sucesso), 1) AS nota_media
FROM departamentos d
JOIN colaborador c ON d.id_departamento = c.id_departamento
JOIN Viagem v ON c.id_colaborador = v.id_colaborador
JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
GROUP BY d.id_departamento, d.nome_departamento
ORDER BY nota_media DESC;

