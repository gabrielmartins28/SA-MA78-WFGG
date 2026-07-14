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

    sql = "SELECT * FROM Despesas"
    cursor.execute(sql)
    resultado = cursor.fetchall()

    for despesa in resultado:
        print(despesa)

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