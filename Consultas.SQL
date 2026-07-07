1. Listar todos os colaboradores e seus departamentos
SELECT c.nome_colaborador, d.nome_departamento
FROM colaborador c
JOIN departamentos d
ON c.id_departamento = d.id_departamento;

2. Listar colaboradores e seus gestores
SELECT c.nome_colaborador AS Colaborador,
       g.nome_colaborador AS Gestor
FROM colaborador c
LEFT JOIN colaborador g
ON c.id_gestor = g.id_colaborador;

3. Mostrar todos os veículos disponíveis
SELECT *
FROM Frota_Veiculo
WHERE status_veiculo = 'Disponivel';

4. Listar todas as viagens aprovadas
SELECT *
FROM Viagem
WHERE status_viagem = 'Aprovada';

5. Mostrar todas as viagens com nome do colaborador
SELECT c.nome_colaborador,
       v.destino_viagem,
       v.dia_saida,
       v.dia_retorno
FROM Viagem v
JOIN colaborador c
ON v.id_colaborador = c.id_colaborador;

6. Mostrar viagens com o objetivo da viagem
SELECT c.nome_colaborador,
       o.descricao,
       v.destino_viagem
FROM Viagem v
JOIN colaborador c
ON v.id_colaborador = c.id_colaborador
JOIN Objetivo_Viagem o
ON v.id_objetivo = o.id_objetivo;

7. Calcular o total gasto por viagem
SELECT id_viagem,
       SUM(valor) AS Total_Gasto
FROM Despesas
GROUP BY id_viagem;

8. Mostrar o total gasto por colaborador
SELECT c.nome_colaborador,
       SUM(d.valor) AS Total_Gasto
FROM colaborador c
JOIN Viagem v
ON c.id_colaborador = v.id_colaborador
JOIN Despesas d
ON v.id_viagem = d.id_viagem
GROUP BY c.nome_colaborador;

9. Mostrar o orçamento de cada departamento
SELECT nome_departamento,
       orcamento_departamento
FROM departamentos;

10. Mostrar quantos colaboradores existem em cada departamento
SELECT d.nome_departamento,
       COUNT(c.id_colaborador) AS Quantidade
FROM departamentos d
LEFT JOIN colaborador c
ON d.id_departamento = c.id_departamento
GROUP BY d.nome_departamento;

11. Mostrar viagens com seus respectivos veículos
SELECT v.id_viagem,
       v.destino_viagem,
       f.modelo,
       f.placa
FROM Viagem v
JOIN Frota_Veiculo f
ON v.id_veiculo = f.id_veiculo;

12. Mostrar colaboradores que possuem CNH
SELECT nome_colaborador
FROM colaborador
WHERE possui_cnh = TRUE;

13. Mostrar quantidade de viagens por destino
SELECT destino_viagem,
       COUNT(*) AS Total
FROM Viagem
GROUP BY destino_viagem;

14. Mostrar quantidade de viagens por objetivo
SELECT o.descricao,
       COUNT(*) AS Total
FROM Viagem v
JOIN Objetivo_Viagem o
ON v.id_objetivo = o.id_objetivo
GROUP BY o.descricao;

15. Mostrar despesas acima de R$500,00
SELECT *
FROM Despesas
WHERE valor > 500;

16. Mostrar a média das avaliações das viagens
SELECT AVG(indicador_sucesso) AS Media_Avaliacao
FROM analise_eficacia_viagem;

17. Mostrar todas as viagens avaliadas com nota 5
SELECT v.id_viagem,
       c.nome_colaborador,
       a.indicador_sucesso
FROM analise_eficacia_viagem a
JOIN Viagem v
ON a.id_viagem = v.id_viagem
JOIN colaborador c
ON v.id_colaborador = c.id_colaborador
WHERE a.indicador_sucesso = '5';

18. Mostrar quantidade de aprovações e rejeições
SELECT status_decisao,
       COUNT(*) AS Quantidade
FROM Aprovacao
GROUP BY status_decisao;

19. Mostrar colaboradores que participaram como carona
SELECT c.nome_colaborador,
       ca.id_viagem
FROM Carona ca
JOIN colaborador c
ON ca.id_colaborador = c.id_colaborador;

20. Relatório completo das viagens
SELECT
    v.id_viagem,
    c.nome_colaborador,
    d.nome_departamento,
    o.descricao AS Objetivo,
    v.destino_viagem,
    f.modelo AS Veiculo,
    v.status_viagem,
    SUM(ds.valor) AS Total_Despesas,
    a.indicador_sucesso
FROM Viagem v
JOIN colaborador c
ON v.id_colaborador = c.id_colaborador
JOIN departamentos d
ON c.id_departamento = d.id_departamento
JOIN Objetivo_Viagem o
ON v.id_objetivo = o.id_objetivo
LEFT JOIN Frota_Veiculo f
ON v.id_veiculo = f.id_veiculo
LEFT JOIN Despesas ds
ON v.id_viagem = ds.id_viagem
LEFT JOIN analise_eficacia_viagem a
ON v.id_viagem = a.id_viagem
GROUP BY
    v.id_viagem,
    c.nome_colaborador,
    d.nome_departamento,
    o.descricao,
    v.destino_viagem,
    f.modelo,
    v.status_viagem,
    a.indicador_sucesso;
