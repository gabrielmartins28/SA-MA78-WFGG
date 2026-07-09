from database import conectar


# CRIAR
def criar_carona(nome_motorista, destino, valor, data_carona):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO carona
    (nome_motorista, destino, valor, data_carona)
    VALUES (%s, %s, %s, %s)
    """

    valores = (
        nome_motorista,
        destino,
        valor,
        data_carona
    )

    cursor.execute(sql, valores)
    conexao.commit()

    print("Carona cadastrada com sucesso!")

    cursor.close()
    conexao.close()



# LISTAR
def listar_carona():

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM carona"

    cursor.execute(sql)

    resultado = cursor.fetchall()

    for carona in resultado:
        print(carona)

    cursor.close()
    conexao.close()



# ATUALIZAR
def atualizar_carona(id_carona, nome_motorista, destino, valor, data_carona):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE carona
    SET 
        nome_motorista = %s,
        destino = %s,
        valor = %s,
        data_carona = %s
    WHERE id_carona = %s
    """

    valores = (
        nome_motorista,
        destino,
        valor,
        data_carona,
        id_carona
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print("Carona atualizada com sucesso!")

    cursor.close()
    conexao.close()



# DELETAR
def deletar_carona(id_carona):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    DELETE FROM carona
    WHERE id_carona = %s
    """

    cursor.execute(sql, (id_carona,))

    conexao.commit()

    print("Carona excluída com sucesso!")

    cursor.close()
    conexao.close()
