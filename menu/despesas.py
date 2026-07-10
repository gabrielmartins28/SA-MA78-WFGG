import mysql.connector

# ==========================
# CONEXÃO COM O BANCO
# ==========================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA",
        database="SEU_BANCO"
    )

# ==========================
# CRIAR DESPESA
# ==========================
def criar_despesa(descricao, valor, data_despesa):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO despesas (descricao, valor, data_despesa)
    VALUES (%s, %s, %s)
    """

    valores = (descricao, valor, data_despesa)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Despesa cadastrada com sucesso!")

    cursor.close()
    conexao.close()


# ==========================
# LISTAR DESPESAS
# ==========================
def listar_despesas():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM despesas"

    cursor.execute(sql)
    resultado = cursor.fetchall()

    for despesa in resultado:
        print(despesa)

    cursor.close()
    conexao.close()


# ==========================
# ATUALIZAR DESPESA
# ==========================
def atualizar_despesa(id_despesa, descricao, valor, data_despesa):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE despesas
    SET descricao = %s,
        valor = %s,
        data_despesa = %s
    WHERE id_despesa = %s
    """

    valores = (descricao, valor, data_despesa, id_despesa)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Despesa atualizada com sucesso!")

    cursor.close()
    conexao.close()


# ==========================
# DELETAR DESPESA
# ==========================
def deletar_despesa(id_despesa):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM despesas WHERE id_despesa = %s"

    cursor.execute(sql, (id_despesa,))
    conexao.commit()

    print("Despesa excluída com sucesso!")

    cursor.close()
    conexao.close()