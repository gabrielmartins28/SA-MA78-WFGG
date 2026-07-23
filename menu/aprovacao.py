from database import conectar


def inserir_aprovacao(id_viagem, id_colaborador, data_hora_avaliacao, status_decisao, observacoes_justificativa=None):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO Aprovacao (id_viagem, id_colaborador, data_hora_avaliacao, status_decisao, observacoes_justificativa)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (id_viagem, id_colaborador, data_hora_avaliacao, status_decisao, observacoes_justificativa)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Aprovação com status {status_decisao} inserida com sucesso!")

    cursor.close()
    conexao.close()


def listar_aprovacao():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_aprovacao, id_viagem, id_colaborador, data_hora_avaliacao, status_decisao, observacoes_justificativa
    FROM Aprovacao
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'VIAGEM':<8} | {'COLAB.':<8} | {'DATA/HORA':<17} | {'STATUS':<12} | {'OBSERVAÇÃO':<35}")
    print("-" * 95)
    for aprovacao in dados:
        id_aprovacao, id_viagem, id_colaborador, data_hora, status, observacao = aprovacao
        data_str = data_hora.strftime('%d/%m/%Y %H:%M') if data_hora and hasattr(data_hora, 'strftime') else str(data_hora or '')
        obs_resumida = (observacao[:32] + '...') if observacao and len(observacao) > 32 else (observacao or '')
        print(f"{id_aprovacao:<5} | {id_viagem:<8} | {id_colaborador:<8} | {data_str:<17} | {status:<12} | {obs_resumida:<35}")

    print(f"\nTotal de aprovações: {len(dados)}")

    cursor.close()
    conexao.close()


def atualizar_aprovacao(id_aprovacao, status_decisao, observacoes_justificativa):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE Aprovacao
    SET status_decisao = %s, observacoes_justificativa = %s
    WHERE id_aprovacao = %s
    """
    valores = (status_decisao, observacoes_justificativa, id_aprovacao)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Aprovação com ID {id_aprovacao} atualizada com sucesso!")

    cursor.close()
    conexao.close()


def deletar_aprovacao(id_aprovacao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM Aprovacao WHERE id_aprovacao = %s"
    cursor.execute(sql, (id_aprovacao,))
    conexao.commit()

    print(f"✅ Aprovação com ID {id_aprovacao} deletada com sucesso!")

    cursor.close()
    conexao.close()

def buscar_aprovacao(id_aprovacao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_aprovacao, id_viagem, id_colaborador, data_hora_avaliacao, status_decisao, observacoes_justificativa
    FROM Aprovacao
    WHERE id_aprovacao = %s
    """
    cursor.execute(sql, (id_aprovacao,))
    aprovacao = cursor.fetchone()

    if aprovacao:
        id_aprovacao, id_viagem, id_colaborador, data_hora, status, observacao = aprovacao
        data_str = data_hora.strftime('%d/%m/%Y %H:%M') if data_hora and hasattr(data_hora, 'strftime') else str(data_hora or '')
        print(f"\nDetalhes da Aprovação ID {id_aprovacao}:")
        print(f"Viagem: {id_viagem}")
        print(f"Colaborador: {id_colaborador}")
        print(f"Data/Hora da Avaliação: {data_str}")
        print(f"Status da Decisão: {status}")
        print(f"Observações/Justificativa: {observacao or 'N/A'}")
    else:
        print(f"❌ Nenhuma aprovação encontrada com ID {id_aprovacao}.")

    cursor.close()
    conexao.close()