from database import conectar


def criar_carona(id_viagem, id_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO Carona (id_viagem, id_colaborador) VALUES (%s, %s)"
    valores = (id_viagem, id_colaborador)

    cursor.execute(sql, valores)
    conexao.commit()

    print("✅ Carona cadastrada com sucesso!")

    cursor.close()
    conexao.close()


def listar_carona():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id_carona, id_viagem, id_colaborador FROM Carona"
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'VIAGEM':<8} | {'COLABORADOR':<12}")
    print("-" * 32)
    for carona in dados:
        id_carona, id_viagem, id_colaborador = carona
        print(f"{id_carona:<5} | {id_viagem:<8} | {id_colaborador:<12}")

    print(f"\nTotal de caronas: {len(dados)}")

    cursor.close()
    conexao.close()


def atualizar_carona(id_carona, id_viagem, id_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE Carona SET id_viagem = %s, id_colaborador = %s WHERE id_carona = %s"
    valores = (id_viagem, id_colaborador, id_carona)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Carona com ID {id_carona} atualizada com sucesso!")

    cursor.close()
    conexao.close()


def deletar_carona(id_carona):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM Carona WHERE id_carona = %s"
    cursor.execute(sql, (id_carona,))
    conexao.commit()

    print(f"✅ Carona com ID {id_carona} deletada com sucesso!")

    cursor.close()
    conexao.close()