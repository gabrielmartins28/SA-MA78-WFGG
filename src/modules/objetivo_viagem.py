from src.database import conectar

def cadastrar_objetivo(descricao):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
    INSERT INTO Objetivo_Viagem (descricao)
    VALUES (%s)
    """
    valores = (descricao,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Objetivo de viagem cadastrado!")
    cursor.close()
    conexao.close()

def listar_objetivos():
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "SELECT id_objetivo, descricao FROM Objetivo_Viagem"
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'DESCRIÇÃO':<60}")
    print("-" * 70)
    for obj in dados:
        id_obj, descricao = obj
        desc_resumida = (descricao[:57] + '...') if descricao and len(descricao) > 57 else (descricao or '')
        print(f"{id_obj:<5} | {desc_resumida:<60}")

    print("\nConsulta de objetivos finalizada.")
    cursor.close()
    conexao.close()

def atualizar_objetivo(id_objetivo, nova_descricao):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
    UPDATE Objetivo_Viagem 
    SET descricao = %s 
    WHERE id_objetivo = %s
    """
    valores = (nova_descricao, id_objetivo)
    cursor.execute(sql, valores)
    conexao.commit()
    print(f"Objetivo ID {id_objetivo} atualizado com sucesso.")
    cursor.close()
    conexao.close()

def deletar_objetivo(id_objetivo):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM Objetivo_Viagem WHERE id_objetivo = %s"
    cursor.execute(sql, (id_objetivo,))
    conexao.commit()
    print(f"Objetivo ID {id_objetivo} deletado.")
    cursor.close()
    conexao.close()