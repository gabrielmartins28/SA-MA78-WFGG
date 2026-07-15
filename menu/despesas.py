from database import conectar


def criar_despesa(valor, data_hora, categoria, forma_pagamento, id_viagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO Despesas (valor, data_hora, categoria, forma_pagamento, id_viagem)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (valor, data_hora, categoria, forma_pagamento, id_viagem)

    cursor.execute(sql, valores)
    conexao.commit()

    print("✅ Despesa cadastrada com sucesso!")

    cursor.close()
    conexao.close()


def listar_despesas():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id_despesas, valor, data_hora, categoria, forma_pagamento, id_viagem FROM Despesas"
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'VALOR':<12} | {'DATA/HORA':<17} | {'CATEGORIA':<18} | {'PAGAMENTO':<15} | {'VIAGEM':<7}")
    print("-" * 85)
    for despesa in dados:
        id_despesa, valor, data_hora, categoria, forma_pagamento, id_viagem = despesa
        data_str = data_hora.strftime('%d/%m/%Y %H:%M') if data_hora and hasattr(data_hora, 'strftime') else str(data_hora or '')
        valor_str = f"R$ {valor:,.2f}"
        print(f"{id_despesa:<5} | {valor_str:<12} | {data_str:<17} | {categoria:<18} | {forma_pagamento:<15} | {id_viagem:<7}")

    print(f"\nTotal de despesas: {len(dados)}")

    cursor.close()
    conexao.close()


def atualizar_despesa(id_despesas, valor, categoria, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE Despesas
    SET valor = %s, categoria = %s, forma_pagamento = %s
    WHERE id_despesas = %s
    """
    valores = (valor, categoria, forma_pagamento, id_despesas)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Despesa com ID {id_despesas} atualizada com sucesso!")

    cursor.close()
    conexao.close()


def deletar_despesa(id_despesas):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM Despesas WHERE id_despesas = %s"
    cursor.execute(sql, (id_despesas,))
    conexao.commit()

    print(f"✅ Despesa com ID {id_despesas} deletada com sucesso!")

    cursor.close()
    conexao.close()