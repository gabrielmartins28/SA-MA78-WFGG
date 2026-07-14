from database import conectar


def inserir_viagem(dia_saida, dia_retorno, id_colaborador, justificativa_viagem, destino_viagem, status_viagem, id_objetivo, id_veiculo=None):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO Viagem (dia_saida, dia_retorno, id_colaborador, justificativa_viagem, destino_viagem, status_viagem, id_objetivo, id_veiculo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (dia_saida, dia_retorno, id_colaborador, justificativa_viagem, destino_viagem, status_viagem, id_objetivo, id_veiculo)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Viagem para {destino_viagem} inserida com sucesso!")

    cursor.close()
    conexao.close()


def listar_viagem():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM Viagem"
    cursor.execute(sql)
    resultado = cursor.fetchall()

    for viagem in resultado:
        print(viagem)

    cursor.close()
    conexao.close()


def atualizar_viagem(id_viagem, destino_viagem, dia_saida, dia_retorno, status_viagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE Viagem
    SET destino_viagem = %s, dia_saida = %s, dia_retorno = %s, status_viagem = %s
    WHERE id_viagem = %s
    """
    valores = (destino_viagem, dia_saida, dia_retorno, status_viagem, id_viagem)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Viagem com ID {id_viagem} atualizada com sucesso!")

    cursor.close()
    conexao.close()


def deletar_viagem(id_viagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM Viagem WHERE id_viagem = %s"
    cursor.execute(sql, (id_viagem,))
    conexao.commit()

    print(f"✅ Viagem com ID {id_viagem} deletada com sucesso!")

    cursor.close()
    conexao.close()