-- Active: 1783533724186@@mysql-20e679b3-sama78wfgg.b.aivencloud.com@15321@Sistema_interno_Viagens
-- ==============================================================================
-- CATEGORIA 1: GESTÃO FINANCEIRA E CUSTOS
-- ==============================================================================

-- 1. TOTAL DE GASTOS POR CATEGORIA DE DESPESA
SELECT categoria, SUM(valor) AS gasto_total, COUNT(id_despesas) AS qtd_lancamentos
FROM Despesas
GROUP BY categoria
ORDER BY gasto_total DESC;

-- 2. AS 5 VIAGENS MAIS CARAS
SELECT v.id_viagem, v.destino_viagem, v.dia_saida, v.dia_retorno, c.nome_colaborador, SUM(d.valor) AS custo_total
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN Despesas d ON v.id_viagem = d.id_viagem
GROUP BY v.id_viagem, v.destino_viagem, c.nome_colaborador
ORDER BY custo_total DESC
LIMIT 5;

-- 3. ORÇAMENTO DO DEPARTAMENTO VS. GASTO COM VIAGENS (Saldo orçamentário)
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

-- 4. FORMAS DE PAGAMENTO MAIS UTILIZADAS
SELECT forma_pagamento, COUNT(*) AS quantidade_uso, SUM(valor) AS volume_reais
FROM Despesas
GROUP BY forma_pagamento
ORDER BY quantidade_uso DESC;

-- 5. MÉDIA DE GASTO POR VIAGEM (Ticket médio)
SELECT ROUND(AVG(custo_por_viagem), 2) AS media_gasto_por_viagem
FROM (
    SELECT id_viagem, SUM(valor) AS custo_por_viagem
    FROM Despesas
    GROUP BY id_viagem
) AS subconsulta;

-- 6. GASTO TOTAL POR COLABORADOR
SELECT c.nome_colaborador, SUM(d.valor) AS Total_Gasto
FROM colaborador c
JOIN Viagem v ON c.id_colaborador = v.id_colaborador
JOIN Despesas d ON v.id_viagem = d.id_viagem
GROUP BY c.nome_colaborador
ORDER BY Total_Gasto DESC;

-- 7. AUDITORIA: DESPESAS ACIMA DE R$ 1000,00 (Análise de compliance)
SELECT *
FROM Despesas
WHERE valor > 1000
ORDER BY valor DESC;


-- ==============================================================================
-- CATEGORIA 2: LOGÍSTICA E FROTA
-- ==============================================================================

-- 8. RANKING DOS VEÍCULOS MAIS UTILIZADOS
SELECT f.placa, f.modelo, COUNT(v.id_viagem) AS total_viagens
FROM Frota_Veiculo f
JOIN Viagem v ON f.id_veiculo = v.id_veiculo
GROUP BY f.id_veiculo, f.placa, f.modelo
ORDER BY total_viagens DESC;

-- 9. VIAGENS FEITAS SEM VEÍCULO DA FROTA (Transporte externo)
SELECT id_viagem, destino_viagem, dia_saida, status_viagem
FROM Viagem
WHERE id_veiculo IS NULL;

-- 10. TOP 5 VEÍCULOS COM MAIOR QUILOMETRAGEM
SELECT placa, modelo, marca, km_atual 
FROM Frota_Veiculo
ORDER BY km_atual DESC
LIMIT 5;

-- 11. VEÍCULOS INDISPONÍVEIS NO MOMENTO
SELECT placa, modelo, status_veiculo
FROM Frota_Veiculo
WHERE status_veiculo != 'Disponivel';

-- 12. CAPACIDADE OCIOSA DA FROTA (Análise de ocupação de assentos)
SELECT 
    v.id_viagem, f.modelo, f.capacidade_passageiros,
    (1 + (SELECT COUNT(*) FROM Carona c WHERE c.id_viagem = v.id_viagem)) AS total_ocupantes
FROM Viagem v
JOIN Frota_Veiculo f ON v.id_veiculo = f.id_veiculo
HAVING total_ocupantes < f.capacidade_passageiros;


-- ==============================================================================
-- CATEGORIA 3: COLABORADORES, HIERARQUIA E CARONAS
-- ==============================================================================

-- 13. QUANTIDADE DE VIAGENS SOLICITADAS POR COLABORADOR
SELECT c.nome_colaborador, d.nome_departamento, COUNT(v.id_viagem) AS qtd_viagens
FROM colaborador c
JOIN departamentos d ON c.id_departamento = d.id_departamento
LEFT JOIN Viagem v ON c.id_colaborador = v.id_colaborador
GROUP BY c.id_colaborador, c.nome_colaborador, d.nome_departamento
ORDER BY qtd_viagens DESC;

-- 14. LISTAGEM DE GESTORES (Filtro por auto-relacionamento)
SELECT DISTINCT gestor.nome_colaborador AS nome_gestor, gestor.cargo_funcionario
FROM colaborador funcionario
JOIN colaborador gestor ON funcionario.id_gestor = gestor.id_colaborador;

-- 15. LISTA DE SUBORDINADOS POR GESTOR ESPECÍFICO (Ex: id_gestor = 1)
SELECT nome_colaborador, cargo_funcionario, email_colaborador
FROM colaborador
WHERE id_gestor = 1;

-- 16. COLABORADORES ATIVOS SEM CNH
SELECT nome_colaborador, cargo_funcionario, telefone_colaborador
FROM colaborador
WHERE possui_cnh = FALSE AND status_funcionario = 'Ativo';

-- 17. CONTAGEM DE CARONAS UTILIZADAS POR COLABORADOR
SELECT c.nome_colaborador, COUNT(car.id_carona) AS vezes_que_pegou_carona
FROM colaborador c
JOIN Carona car ON c.id_colaborador = car.id_colaborador
GROUP BY c.id_colaborador, c.nome_colaborador
ORDER BY vezes_que_pegou_carona DESC;

-- 18. HEADCOUNT POR DEPARTAMENTO
SELECT d.nome_departamento, COUNT(c.id_colaborador) AS Quantidade_Colaboradores
FROM departamentos d
LEFT JOIN colaborador c ON d.id_departamento = c.id_departamento
GROUP BY d.nome_departamento
ORDER BY Quantidade_Colaboradores DESC;


-- ==============================================================================
-- CATEGORIA 4: EFICÁCIA, OBJETIVOS E STATUS
-- ==============================================================================

-- 19. VIAGENS COM STATUS PENDENTE
SELECT id_viagem, destino_viagem, dia_saida, justificativa_viagem
FROM Viagem
WHERE status_viagem = 'Pendente';

-- 20. HISTÓRICO DE VIAGENS REJEITADAS E JUSTIFICATIVAS
SELECT v.id_viagem, c.nome_colaborador AS solicitante, a.observacoes_justificativa AS motivo_rejeicao
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN Aprovacao a ON v.id_viagem = a.id_viagem
WHERE a.status_decisao = 'Rejeitado';

-- 21. VOLUME DE DECISÕES DE APROVAÇÃO (Aprovado vs Rejeitado)
SELECT status_decisao, COUNT(*) AS Quantidade
FROM Aprovacao
GROUP BY status_decisao;

-- 22. FREQUÊNCIA DE OBJETIVOS DE VIAGEM
SELECT o.descricao AS objetivo, COUNT(v.id_viagem) AS total_solicitacoes
FROM Objetivo_Viagem o
JOIN Viagem v ON o.id_objetivo = v.id_objetivo
GROUP BY o.id_objetivo, o.descricao
ORDER BY total_solicitacoes DESC;

-- 23. DESTINOS COM MAIOR VOLUME DE VIAGENS
SELECT destino_viagem, COUNT(*) AS Total_Viagens
FROM Viagem
GROUP BY destino_viagem
ORDER BY Total_Viagens DESC;

-- 24. MÉDIA DO INDICADOR DE SUCESSO POR DEPARTAMENTO
SELECT d.nome_departamento, ROUND(AVG(aev.indicador_sucesso), 1) AS nota_media
FROM departamentos d
JOIN colaborador c ON d.id_departamento = c.id_departamento
JOIN Viagem v ON c.id_colaborador = v.id_colaborador
JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
GROUP BY d.id_departamento, d.nome_departamento
ORDER BY nota_media DESC;

-- 25. VIAGENS CONCLUÍDAS SEM REGISTRO DE ANÁLISE DE EFICÁCIA
SELECT v.id_viagem, v.destino_viagem, c.nome_colaborador AS solicitante
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
LEFT JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
WHERE v.status_viagem = 'Concluída' AND aev.id_analise IS NULL;


-- ==============================================================================
-- CATEGORIA 5: EXPORTAÇÃO E INTEGRAÇÃO (BI)
-- ==============================================================================

-- 26. TABELA PLANA (Flat Table) DE VIAGENS E CUSTOS
SELECT 
    v.id_viagem,
    c.nome_colaborador,
    d.nome_departamento,
    o.descricao AS Objetivo,
    v.destino_viagem,
    f.modelo AS Veiculo,
    v.status_viagem,
    IFNULL(SUM(ds.valor), 0) AS Total_Despesas,
    a.indicador_sucesso AS Nota_Eficacia
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
JOIN departamentos d ON c.id_departamento = d.id_departamento
JOIN Objetivo_Viagem o ON v.id_objetivo = o.id_objetivo
LEFT JOIN Frota_Veiculo f ON v.id_veiculo = f.id_veiculo
LEFT JOIN Despesas ds ON v.id_viagem = ds.id_viagem
LEFT JOIN analise_eficacia_viagem a ON v.id_viagem = a.id_viagem
GROUP BY 
    v.id_viagem, 
    c.nome_colaborador, 
    d.nome_departamento, 
    o.descricao, 
    v.destino_viagem, 
    f.modelo, 
    v.status_viagem, 
    a.indicador_sucesso;


-- ==============================================================================
-- CATEGORIA 6: AUDITORIA AVANÇADA E COMPLIANCE
-- ==============================================================================

-- 27. EVOLUÇÃO TEMPORAL DE GASTOS (Mês a Mês)
SELECT 
    YEAR(v.dia_saida) AS ano, 
    MONTH(v.dia_saida) AS mes, 
    SUM(d.valor) AS gasto_mensal,
    COUNT(DISTINCT v.id_viagem) AS total_viagens_no_mes
FROM Viagem v
JOIN Despesas d ON v.id_viagem = d.id_viagem
GROUP BY ano, mes
ORDER BY ano DESC, mes DESC;

-- 28. CÁLCULO DE DURAÇÃO DAS VIAGENS
SELECT 
    v.id_viagem, 
    c.nome_colaborador, 
    v.destino_viagem, 
    DATEDIFF(v.dia_retorno, v.dia_saida) AS duracao_em_dias
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
WHERE v.dia_retorno IS NOT NULL AND v.dia_saida IS NOT NULL
ORDER BY duracao_em_dias DESC;

-- 29. SLA DE APROVAÇÃO (Diferença em dias entre aprovação e saída)
SELECT 
    v.id_viagem, 
    c.nome_colaborador AS solicitante,
    v.dia_saida, 
    a.data_hora_avaliacao, 
    DATEDIFF(v.dia_saida, a.data_hora_avaliacao) AS dias_de_antecedencia
FROM Viagem v
JOIN Aprovacao a ON v.id_viagem = a.id_viagem
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
ORDER BY dias_de_antecedencia ASC;

-- 30. COMPLIANCE: DESPESAS FORA DO PERÍODO DA VIAGEM
SELECT 
    d.id_despesas, 
    c.nome_colaborador,
    v.destino_viagem,
    v.dia_saida, 
    v.dia_retorno, 
    d.data_hora AS data_da_despesa, 
    d.valor,
    d.categoria
FROM Despesas d
JOIN Viagem v ON d.id_viagem = v.id_viagem
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
WHERE d.data_hora < v.dia_saida OR d.data_hora > v.dia_retorno
ORDER BY d.data_hora DESC;

-- 31. VIAGENS CONCLUÍDAS SEM REGISTRO DE DESPESAS
SELECT 
    v.id_viagem, 
    c.nome_colaborador, 
    v.destino_viagem,
    v.dia_saida
FROM Viagem v
JOIN colaborador c ON v.id_colaborador = c.id_colaborador
LEFT JOIN Despesas d ON v.id_viagem = d.id_viagem
WHERE v.status_viagem = 'Concluída'
GROUP BY v.id_viagem, c.nome_colaborador, v.destino_viagem, v.dia_saida
HAVING IFNULL(SUM(d.valor), 0) = 0;