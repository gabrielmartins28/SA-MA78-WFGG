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

    sql = """
    SELECT id_viagem, destino_viagem, dia_saida, dia_retorno, status_viagem, id_colaborador, id_objetivo, id_veiculo
    FROM Viagem
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'DESTINO':<25} | {'SAÍDA':<12} | {'RETORNO':<12} | {'STATUS':<15} | {'COLAB.':<7} | {'OBJET.':<7} | {'VEÍC.':<6}")
    print("-" * 100)
    for viagem in dados:
        id_viagem, destino, saida, retorno, status, id_colaborador, id_objetivo, id_veiculo = viagem
        saida_str = saida.strftime('%d/%m/%Y') if saida and hasattr(saida, 'strftime') else str(saida or '')
        retorno_str = retorno.strftime('%d/%m/%Y') if retorno and hasattr(retorno, 'strftime') else str(retorno or '')
        destino_resumido = (destino[:22] + '...') if destino and len(destino) > 22 else (destino or '')
        veiculo_str = str(id_veiculo) if id_veiculo is not None else '-'
        print(f"{id_viagem:<5} | {destino_resumido:<25} | {saida_str:<12} | {retorno_str:<12} | {status:<15} | {id_colaborador:<7} | {id_objetivo:<7} | {veiculo_str:<6}")

    print(f"\nTotal de viagens: {len(dados)}")

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

def buscar_viagem(id_viagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_viagem, destino_viagem, dia_saida, dia_retorno, status_viagem, id_colaborador, id_objetivo, id_veiculo
    FROM Viagem
    WHERE id_viagem = %s
    """
    cursor.execute(sql, (id_viagem,))
    viagem = cursor.fetchone()

    if viagem:
        id_viagem, destino, saida, retorno, status, id_colaborador, id_objetivo, id_veiculo = viagem
        saida_str = saida.strftime('%d/%m/%Y') if saida and hasattr(saida, 'strftime') else str(saida or '')
        retorno_str = retorno.strftime('%d/%m/%Y') if retorno and hasattr(retorno, 'strftime') else str(retorno or '')
        destino_resumido = (destino[:22] + '...') if destino and len(destino) > 22 else (destino or '')
        veiculo_str = str(id_veiculo) if id_veiculo is not None else '-'
        print(f"\nViagem encontrada:")
        print(f"ID: {id_viagem}")
        print(f"Destino: {destino_resumido}")
        print(f"Saída: {saida_str}")
        print(f"Retorno: {retorno_str}")
        print(f"Status: {status}")
        print(f"Colaborador ID: {id_colaborador}")
        print(f"Objetivo ID: {id_objetivo}")
        print(f"Veículo ID: {veiculo_str}")
    else:
        print(f"\n❌ Nenhuma viagem encontrada com ID {id_viagem}.")

    cursor.close()
    conexao.close()