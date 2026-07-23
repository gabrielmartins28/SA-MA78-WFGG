from src.database import conectar


# ==============================================================================
# UTILITÁRIO GENÉRICO DE EXECUÇÃO E IMPRESSÃO
# ==============================================================================

def _formatar_valor(valor):
    """Formata um valor de célula para exibição amigável no terminal."""
    if valor is None:
        return "-"
    if hasattr(valor, "strftime"):
        # datas e datetimes
        if hasattr(valor, "hour"):
            return valor.strftime("%d/%m/%Y %H:%M")
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def executar_consulta(titulo, sql, parametros=None):
    """
    Executa uma consulta SQL de leitura e imprime o resultado em uma
    tabela formatada, descobrindo as colunas dinamicamente.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(sql, parametros or ())
    linhas = cursor.fetchall()
    colunas = [descricao[0] for descricao in cursor.description]

    print(f"\n📈 {titulo}")
    print("=" * 100)

    if not linhas:
        print("Nenhum resultado encontrado para esta consulta.")
    else:
        # calcula a largura de cada coluna com base no cabeçalho e nos dados
        larguras = [len(col) for col in colunas]
        linhas_formatadas = []
        for linha in linhas:
            linha_fmt = [_formatar_valor(v) for v in linha]
            linhas_formatadas.append(linha_fmt)
            for i, valor in enumerate(linha_fmt):
                larguras[i] = min(max(larguras[i], len(valor)), 30)

        cabecalho = " | ".join(
            col[:larguras[i]].ljust(larguras[i]) for i, col in enumerate(colunas)
        )
        print(cabecalho)
        print("-" * len(cabecalho))

        for linha_fmt in linhas_formatadas:
            print(" | ".join(
                valor[:larguras[i]].ljust(larguras[i]) for i, valor in enumerate(linha_fmt)
            ))

        print(f"\nTotal de registros: {len(linhas)}")

    cursor.close()
    conexao.close()


# ==============================================================================
# CATEGORIA 1: GESTÃO FINANCEIRA E CUSTOS
# ==============================================================================

def consulta_gastos_por_categoria():
    executar_consulta(
        "Total de gastos por categoria de despesa",
        """
        SELECT categoria, SUM(valor) AS gasto_total, COUNT(id_despesas) AS qtd_lancamentos
        FROM Despesas
        GROUP BY categoria
        ORDER BY gasto_total DESC
        """,
    )


def consulta_viagens_mais_caras():
    executar_consulta(
        "As 5 viagens mais caras",
        """
        SELECT v.id_viagem, v.destino_viagem, v.dia_saida, v.dia_retorno, c.nome_colaborador, SUM(d.valor) AS custo_total
        FROM Viagem v
        JOIN colaborador c ON v.id_colaborador = c.id_colaborador
        JOIN Despesas d ON v.id_viagem = d.id_viagem
        GROUP BY v.id_viagem, v.destino_viagem, c.nome_colaborador
        ORDER BY custo_total DESC
        LIMIT 5
        """,
    )


def consulta_orcamento_vs_gasto():
    executar_consulta(
        "Orçamento do departamento vs. gasto com viagens (saldo orçamentário)",
        """
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
        ORDER BY total_gasto DESC
        """,
    )


def consulta_formas_pagamento():
    executar_consulta(
        "Formas de pagamento mais utilizadas",
        """
        SELECT forma_pagamento, COUNT(*) AS quantidade_uso, SUM(valor) AS volume_reais
        FROM Despesas
        GROUP BY forma_pagamento
        ORDER BY quantidade_uso DESC
        """,
    )


def consulta_media_gasto_por_viagem():
    executar_consulta(
        "Média de gasto por viagem (ticket médio)",
        """
        SELECT ROUND(AVG(custo_por_viagem), 2) AS media_gasto_por_viagem
        FROM (
            SELECT id_viagem, SUM(valor) AS custo_por_viagem
            FROM Despesas
            GROUP BY id_viagem
        ) AS subconsulta
        """,
    )


def consulta_gasto_por_colaborador():
    executar_consulta(
        "Gasto total por colaborador",
        """
        SELECT c.nome_colaborador, SUM(d.valor) AS Total_Gasto
        FROM colaborador c
        JOIN Viagem v ON c.id_colaborador = v.id_colaborador
        JOIN Despesas d ON v.id_viagem = d.id_viagem
        GROUP BY c.nome_colaborador
        ORDER BY Total_Gasto DESC
        """,
    )


def consulta_despesas_acima_mil():
    executar_consulta(
        "Auditoria: despesas acima de R$ 1000,00 (análise de compliance)",
        """
        SELECT *
        FROM Despesas
        WHERE valor > 1000
        ORDER BY valor DESC
        """,
    )


# ==============================================================================
# CATEGORIA 2: LOGÍSTICA E FROTA
# ==============================================================================

def consulta_ranking_veiculos():
    executar_consulta(
        "Ranking dos veículos mais utilizados",
        """
        SELECT f.placa, f.modelo, COUNT(v.id_viagem) AS total_viagens
        FROM Frota_Veiculo f
        JOIN Viagem v ON f.id_veiculo = v.id_veiculo
        GROUP BY f.id_veiculo, f.placa, f.modelo
        ORDER BY total_viagens DESC
        """,
    )


def consulta_viagens_sem_veiculo():
    executar_consulta(
        "Viagens feitas sem veículo da frota (transporte externo)",
        """
        SELECT id_viagem, destino_viagem, dia_saida, status_viagem
        FROM Viagem
        WHERE id_veiculo IS NULL
        """,
    )


def consulta_top5_km():
    executar_consulta(
        "Top 5 veículos com maior quilometragem",
        """
        SELECT placa, modelo, marca, km_atual
        FROM Frota_Veiculo
        ORDER BY km_atual DESC
        LIMIT 5
        """,
    )


def consulta_veiculos_indisponiveis():
    executar_consulta(
        "Veículos indisponíveis no momento",
        """
        SELECT placa, modelo, status_veiculo
        FROM Frota_Veiculo
        WHERE status_veiculo != 'Disponivel'
        """,
    )


def consulta_capacidade_ociosa():
    executar_consulta(
        "Capacidade ociosa da frota (análise de ocupação de assentos)",
        """
        SELECT
            v.id_viagem, f.modelo, f.capacidade_passageiros,
            (1 + (SELECT COUNT(*) FROM Carona c WHERE c.id_viagem = v.id_viagem)) AS total_ocupantes
        FROM Viagem v
        JOIN Frota_Veiculo f ON v.id_veiculo = f.id_veiculo
        HAVING total_ocupantes < f.capacidade_passageiros
        """,
    )


# ==============================================================================
# CATEGORIA 3: COLABORADORES, HIERARQUIA E CARONAS
# ==============================================================================

def consulta_viagens_por_colaborador():
    executar_consulta(
        "Quantidade de viagens solicitadas por colaborador",
        """
        SELECT c.nome_colaborador, d.nome_departamento, COUNT(v.id_viagem) AS qtd_viagens
        FROM colaborador c
        JOIN departamentos d ON c.id_departamento = d.id_departamento
        LEFT JOIN Viagem v ON c.id_colaborador = v.id_colaborador
        GROUP BY c.id_colaborador, c.nome_colaborador, d.nome_departamento
        ORDER BY qtd_viagens DESC
        """,
    )


def consulta_listagem_gestores():
    executar_consulta(
        "Listagem de gestores (filtro por auto-relacionamento)",
        """
        SELECT DISTINCT gestor.nome_colaborador AS nome_gestor, gestor.cargo_funcionario
        FROM colaborador funcionario
        JOIN colaborador gestor ON funcionario.id_gestor = gestor.id_colaborador
        """,
    )


def consulta_subordinados_por_gestor(id_gestor=1):
    executar_consulta(
        f"Subordinados do gestor de ID {id_gestor}",
        """
        SELECT nome_colaborador, cargo_funcionario, email_colaborador
        FROM colaborador
        WHERE id_gestor = %s
        """,
        (id_gestor,),
    )


def consulta_colaboradores_sem_cnh():
    executar_consulta(
        "Colaboradores ativos sem CNH",
        """
        SELECT nome_colaborador, cargo_funcionario, telefone_colaborador
        FROM colaborador
        WHERE possui_cnh = FALSE AND status_funcionario = 'Ativo'
        """,
    )


def consulta_caronas_por_colaborador():
    executar_consulta(
        "Contagem de caronas utilizadas por colaborador",
        """
        SELECT c.nome_colaborador, COUNT(car.id_carona) AS vezes_que_pegou_carona
        FROM colaborador c
        JOIN Carona car ON c.id_colaborador = car.id_colaborador
        GROUP BY c.id_colaborador, c.nome_colaborador
        ORDER BY vezes_que_pegou_carona DESC
        """,
    )


def consulta_headcount_departamento():
    executar_consulta(
        "Headcount por departamento",
        """
        SELECT d.nome_departamento, COUNT(c.id_colaborador) AS Quantidade_Colaboradores
        FROM departamentos d
        LEFT JOIN colaborador c ON d.id_departamento = c.id_departamento
        GROUP BY d.nome_departamento
        ORDER BY Quantidade_Colaboradores DESC
        """,
    )


# ==============================================================================
# CATEGORIA 4: EFICÁCIA, OBJETIVOS E STATUS
# ==============================================================================

def consulta_viagens_pendentes():
    executar_consulta(
        "Viagens com status pendente",
        """
        SELECT id_viagem, destino_viagem, dia_saida, justificativa_viagem
        FROM Viagem
        WHERE status_viagem = 'Pendente'
        """,
    )


def consulta_viagens_rejeitadas():
    executar_consulta(
        "Histórico de viagens rejeitadas e justificativas",
        """
        SELECT v.id_viagem, c.nome_colaborador AS solicitante, a.observacoes_justificativa AS motivo_rejeicao
        FROM Viagem v
        JOIN colaborador c ON v.id_colaborador = c.id_colaborador
        JOIN Aprovacao a ON v.id_viagem = a.id_viagem
        WHERE a.status_decisao = 'Rejeitado'
        """,
    )


def consulta_volume_decisoes():
    executar_consulta(
        "Volume de decisões de aprovação (aprovado vs. rejeitado)",
        """
        SELECT status_decisao, COUNT(*) AS Quantidade
        FROM Aprovacao
        GROUP BY status_decisao
        """,
    )


def consulta_frequencia_objetivos():
    executar_consulta(
        "Frequência de objetivos de viagem",
        """
        SELECT o.descricao AS objetivo, COUNT(v.id_viagem) AS total_solicitacoes
        FROM Objetivo_Viagem o
        JOIN Viagem v ON o.id_objetivo = v.id_objetivo
        GROUP BY o.id_objetivo, o.descricao
        ORDER BY total_solicitacoes DESC
        """,
    )


def consulta_destinos_mais_frequentes():
    executar_consulta(
        "Destinos com maior volume de viagens",
        """
        SELECT destino_viagem, COUNT(*) AS Total_Viagens
        FROM Viagem
        GROUP BY destino_viagem
        ORDER BY Total_Viagens DESC
        """,
    )


def consulta_media_sucesso_departamento():
    executar_consulta(
        "Média do indicador de sucesso por departamento",
        """
        SELECT d.nome_departamento, ROUND(AVG(aev.indicador_sucesso), 1) AS nota_media
        FROM departamentos d
        JOIN colaborador c ON d.id_departamento = c.id_departamento
        JOIN Viagem v ON c.id_colaborador = v.id_colaborador
        JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
        GROUP BY d.id_departamento, d.nome_departamento
        ORDER BY nota_media DESC
        """,
    )


def consulta_viagens_sem_analise():
    executar_consulta(
        "Viagens concluídas sem registro de análise de eficácia",
        """
        SELECT v.id_viagem, v.destino_viagem, c.nome_colaborador AS solicitante
        FROM Viagem v
        JOIN colaborador c ON v.id_colaborador = c.id_colaborador
        LEFT JOIN analise_eficacia_viagem aev ON v.id_viagem = aev.id_viagem
        WHERE v.status_viagem = 'Concluída' AND aev.id_analise IS NULL
        """,
    )


# ==============================================================================
# CATEGORIA 5: EXPORTAÇÃO E INTEGRAÇÃO (BI)
# ==============================================================================

def consulta_tabela_plana_bi():
    executar_consulta(
        "Tabela plana (flat table) de viagens e custos",
        """
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
            a.indicador_sucesso
        """,
    )


# ==============================================================================
# CATEGORIA 6: AUDITORIA AVANÇADA E COMPLIANCE
# ==============================================================================

def consulta_evolucao_gastos_mensal():
    executar_consulta(
        "Evolução temporal de gastos (mês a mês)",
        """
        SELECT
            YEAR(v.dia_saida) AS ano,
            MONTH(v.dia_saida) AS mes,
            SUM(d.valor) AS gasto_mensal,
            COUNT(DISTINCT v.id_viagem) AS total_viagens_no_mes
        FROM Viagem v
        JOIN Despesas d ON v.id_viagem = d.id_viagem
        GROUP BY ano, mes
        ORDER BY ano DESC, mes DESC
        """,
    )


def consulta_duracao_viagens():
    executar_consulta(
        "Cálculo de duração das viagens",
        """
        SELECT
            v.id_viagem,
            c.nome_colaborador,
            v.destino_viagem,
            DATEDIFF(v.dia_retorno, v.dia_saida) AS duracao_em_dias
        FROM Viagem v
        JOIN colaborador c ON v.id_colaborador = c.id_colaborador
        WHERE v.dia_retorno IS NOT NULL AND v.dia_saida IS NOT NULL
        ORDER BY duracao_em_dias DESC
        """,
    )


def consulta_sla_aprovacao():
    executar_consulta(
        "SLA de aprovação (diferença em dias entre aprovação e saída)",
        """
        SELECT
            v.id_viagem,
            c.nome_colaborador AS solicitante,
            v.dia_saida,
            a.data_hora_avaliacao,
            DATEDIFF(v.dia_saida, a.data_hora_avaliacao) AS dias_de_antecedencia
        FROM Viagem v
        JOIN Aprovacao a ON v.id_viagem = a.id_viagem
        JOIN colaborador c ON v.id_colaborador = c.id_colaborador
        ORDER BY dias_de_antecedencia ASC
        """,
    )


def consulta_despesas_fora_do_periodo():
    executar_consulta(
        "Compliance: despesas fora do período da viagem",
        """
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
        ORDER BY d.data_hora DESC
        """,
    )


def consulta_viagens_sem_despesas():
    executar_consulta(
        "Viagens concluídas sem registro de despesas",
        """
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
        HAVING IFNULL(SUM(d.valor), 0) = 0
        """,
    )


# ==============================================================================
# ESTRUTURA USADA PELO MENU (main.py)
# ==============================================================================
# Cada categoria é uma tupla (titulo, emoji, [ (rotulo_no_menu, funcao), ... ])
# A consulta nº 15 (subordinados por gestor) pede um ID, por isso é tratada
# separadamente no main.py (não recebe argumento aqui, tem valor padrão).

CATEGORIAS = [
    (
        "Gestão Financeira e Custos", "💰",
        [
            ("Total de gastos por categoria de despesa", consulta_gastos_por_categoria),
            ("As 5 viagens mais caras", consulta_viagens_mais_caras),
            ("Orçamento do departamento vs. gasto com viagens", consulta_orcamento_vs_gasto),
            ("Formas de pagamento mais utilizadas", consulta_formas_pagamento),
            ("Média de gasto por viagem (ticket médio)", consulta_media_gasto_por_viagem),
            ("Gasto total por colaborador", consulta_gasto_por_colaborador),
            ("Auditoria: despesas acima de R$ 1000,00", consulta_despesas_acima_mil),
        ],
    ),
    (
        "Logística e Frota", "🚗",
        [
            ("Ranking dos veículos mais utilizados", consulta_ranking_veiculos),
            ("Viagens feitas sem veículo da frota", consulta_viagens_sem_veiculo),
            ("Top 5 veículos com maior quilometragem", consulta_top5_km),
            ("Veículos indisponíveis no momento", consulta_veiculos_indisponiveis),
            ("Capacidade ociosa da frota", consulta_capacidade_ociosa),
        ],
    ),
    (
        "Colaboradores, Hierarquia e Caronas", "👤",
        [
            ("Quantidade de viagens solicitadas por colaborador", consulta_viagens_por_colaborador),
            ("Listagem de gestores", consulta_listagem_gestores),
            ("Subordinados de um gestor específico", consulta_subordinados_por_gestor),
            ("Colaboradores ativos sem CNH", consulta_colaboradores_sem_cnh),
            ("Contagem de caronas utilizadas por colaborador", consulta_caronas_por_colaborador),
            ("Headcount por departamento", consulta_headcount_departamento),
        ],
    ),
    (
        "Eficácia, Objetivos e Status", "🎯",
        [
            ("Viagens com status pendente", consulta_viagens_pendentes),
            ("Histórico de viagens rejeitadas e justificativas", consulta_viagens_rejeitadas),
            ("Volume de decisões de aprovação", consulta_volume_decisoes),
            ("Frequência de objetivos de viagem", consulta_frequencia_objetivos),
            ("Destinos com maior volume de viagens", consulta_destinos_mais_frequentes),
            ("Média do indicador de sucesso por departamento", consulta_media_sucesso_departamento),
            ("Viagens concluídas sem análise de eficácia", consulta_viagens_sem_analise),
        ],
    ),
    (
        "Exportação e Integração (BI)", "📤",
        [
            ("Tabela plana (flat table) de viagens e custos", consulta_tabela_plana_bi),
        ],
    ),
    (
        "Auditoria Avançada e Compliance", "🔍",
        [
            ("Evolução temporal de gastos (mês a mês)", consulta_evolucao_gastos_mensal),
            ("Cálculo de duração das viagens", consulta_duracao_viagens),
            ("SLA de aprovação", consulta_sla_aprovacao),
            ("Compliance: despesas fora do período da viagem", consulta_despesas_fora_do_periodo),
            ("Viagens concluídas sem registro de despesas", consulta_viagens_sem_despesas),
        ],
    ),
]
