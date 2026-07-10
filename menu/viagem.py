from estrutura_inicial_python.database import conectar

def listar_viagem():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """SELECT * FROM Viagem"""

    cursor.execute(sql)
    resultado = cursor.fetchall()

    for viagem in resultado:
        print(viagem)

    conexao.close()
    cursor.close()


def atualizar_viagem(id_viagem, destino, data_ida, data_volta):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """UPDATE Viagem SET destino = %s, data_ida = %s, data_volta = %s WHERE id = %s"""
    valores = (destino, data_ida, data_volta, id_viagem)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Viagem com ID {id_viagem} atualizada com sucesso!")

    conexao.close()
    cursor.close()

def deletar_viagem(id_viagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """DELETE FROM Viagem WHERE id = %s"""
    valores = (id_viagem,)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Viagem com ID {id_viagem} deletada com sucesso!")

    conexao.close()
    cursor.close()

def inserir_viagem(destino, data_ida, data_volta):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """INSERT INTO Viagem (destino, data_ida, data_volta) VALUES (%s, %s, %s)"""
    valores = (destino, data_ida, data_volta)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Viagem para {destino} inserida com sucesso!")

    conexao.close()
    cursor.close()