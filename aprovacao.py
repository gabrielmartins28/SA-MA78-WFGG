from estrutura_inicial_python.database import conectar

def listar_aprovacao():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """SELECT * FROM Aprovacao"""

    cursor.execute(sql)
    resultado = cursor.fetchall()

    for aprovacao in resultado:
        print(aprovacao)

    conexao.close()
    cursor.close()

def atualizar_aprovacao(id_aprovacao, status, comentario):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """UPDATE Aprovacao SET status = %s, comentario = %s WHERE id = %s"""
    valores = (status, comentario, id_aprovacao)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Aprovacao com ID {id_aprovacao} atualizada com sucesso!")

    conexao.close()
    cursor.close()

def deletar_aprovacao(id_aprovacao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """DELETE FROM Aprovacao WHERE id = %s"""
    valores = (id_aprovacao,)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Aprovacao com ID {id_aprovacao} deletada com sucesso!")

    conexao.close()
    cursor.close()

def inserir_aprovacao(status, comentario):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """INSERT INTO Aprovacao (status, comentario) VALUES (%s, %s)"""
    valores = (status, comentario)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Aprovacao com status {status} inserida com sucesso!")

    conexao.close()
    cursor.close()