from estrutura_inicial_python.database import conectar

def listar_colaborador():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """SELECT * FROM Colaborador"""

    cursor.execute(sql)
    resultado = cursor.fetchall()

    for colaborador in resultado:
        print(colaborador)

    conexao.close()
    cursor.close()

def atualizar_colaborador(id_colaborador, nome, cargo, email):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """UPDATE Colaborador SET nome = %s, cargo = %s, email = %s WHERE id = %s"""
    valores = (nome, cargo, email, id_colaborador)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Colaborador com ID {id_colaborador} atualizado com sucesso!")

    conexao.close()
    cursor.close()

def deletar_colaborador(id_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """DELETE FROM Colaborador WHERE id = %s"""
    valores = (id_colaborador,)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Colaborador com ID {id_colaborador} deletado com sucesso!")

    conexao.close()
    cursor.close()

def inserir_colaborador(nome, cargo, email):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """INSERT INTO Colaborador (nome, cargo, email) VALUES (%s, %s, %s)"""
    valores = (nome, cargo, email)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Colaborador {nome} inserido com sucesso!")

    conexao.close()
    cursor.close()