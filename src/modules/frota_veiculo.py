# Módulo responsável por funcionalidades referentes à frota de veículos
from database import conectar


def listar_veiculos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
        id_veiculo, marca, modelo, placa, capacidade_passageiros, km_atual, status_veiculo
    FROM Frota_Veiculo
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'MARCA':<12} | {'MODELO':<15} | {'PLACA':<10} | {'CAPAC.':<7} | {'KM ATUAL':<10} | {'STATUS':<12}")
    print("-" * 85)
    for veiculo in dados:
        id_veiculo, marca, modelo, placa, capacidade, km_atual, status = veiculo
        km_str = f"{km_atual:,}".replace(",", ".")
        print(f"{id_veiculo:<5} | {marca:<12} | {modelo:<15} | {placa:<10} | {capacidade:<7} | {km_str:<10} | {status:<12}")

    print(f"\nTotal de veículos: {len(dados)}")

    cursor.close()
    conexao.close()


def cadastrar_veiculo(placa, modelo, marca, capacidade, km_atual=0):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO Frota_Veiculo
        (placa, modelo, marca, capacidade_passageiros, km_atual, status_veiculo)
    VALUES
        (%s, %s, %s, %s, %s, 'Disponivel')
    """
    valores = (placa, modelo, marca, capacidade, km_atual)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Veículo cadastrado na frota!")

    cursor.close()
    conexao.close()


def atualizar_status_veiculo(id_veiculo, novo_status):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE Frota_Veiculo
    SET status_veiculo = %s
    WHERE id_veiculo = %s
    """
    valores = (novo_status, id_veiculo)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Status do veículo atualizado!")

    cursor.close()
    conexao.close()


def deletar_veiculo(id_veiculo):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM Frota_Veiculo WHERE id_veiculo = %s"
    cursor.execute(sql, (id_veiculo,))
    conexao.commit()
    print("Veículo deletado!")

    cursor.close()
    conexao.close()

def buscar_veiculo(id_veiculo):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id_veiculo, marca, modelo, placa, capacidade_passageiros, km_atual, status_veiculo FROM Frota_Veiculo WHERE id_veiculo = %s"
    cursor.execute(sql, (id_veiculo,))
    veiculo = cursor.fetchone()

    if veiculo:
        id_veic, marca, modelo, placa, capacidade, km_atual, status = veiculo
        km_str = f"{km_atual:,}".replace(",", ".")
        print(f"\n{'ID':<5} | {'MARCA':<12} | {'MODELO':<15} | {'PLACA':<10} | {'CAPAC.':<7} | {'KM ATUAL':<10} | {'STATUS':<12}")
        print("-" * 85)
        print(f"{id_veic:<5} | {marca:<12} | {modelo:<15} | {placa:<10} | {capacidade:<7} | {km_str:<10} | {status:<12}")
    else:
        print(f"❌ Nenhum veículo encontrado com ID {id_veiculo}")

    cursor.close()
    conexao.close()