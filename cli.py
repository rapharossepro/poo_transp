from typing import Optional

from dominio import Motorista, Rota
from pagamento import CartaoTransporte, PagamentoDinheiro
from sistema import SistemaTransporte
from tarifas import TarifaPadrao, TarifaPico, TarifaEstudantil
from transporte import Metro, Onibus, Veiculo


def criar_dados_padrao(sistema: SistemaTransporte) -> None:
    rota_padrao = Rota("101", "Centro Comercial", 4.50)
    sistema.rotas[rota_padrao.codigo] = rota_padrao

    motorista_padrao = Motorista("12345", "Carlos Silva", rota_padrao)
    motorista_padrao.veiculo = Onibus("ABC-1234", "Mercedes-Benz")
    sistema.motoristas[motorista_padrao.nome] = motorista_padrao

    sistema.cartoes["888"] = CartaoTransporte("888", "Ana Costa (Estudante)", 15.00)


def selecionar_estrategia_tarifa(opcao: str):
    if opcao == "2":
        return TarifaPico()
    if opcao == "3":
        return TarifaEstudantil()
    return TarifaPadrao()


def criar_rota(sistema: SistemaTransporte) -> None:
    print("\n--- CRIAR NOVA ROTA ---")
    codigo = input("Código/Número da Rota (ex: 404): ").strip()
    destino = input("Destino Final: ").strip()
    try:
        tarifa = float(input("Valor da Tarifa Base (R$): "))
        sistema.rotas[codigo] = Rota(codigo, destino, tarifa)
        print(f"✨ Rota {codigo} para '{destino}' criada com tarifa de R${tarifa:.2f}!")
    except ValueError:
        print("❌ Valor inválido para tarifa.")


def cadastrar_motorista(sistema: SistemaTransporte) -> None:
    print("\n--- CADASTRAR MOTORISTA ---")
    if not sistema.rotas:
        print("❌ Cadastre uma rota primeiro!")
        return

    print("Rotas disponíveis:", list(sistema.rotas.keys()))
    cod_rota = input("Escolha o código da rota para o motorista: ").strip()

    if cod_rota in sistema.rotas:
        nome = input("Nome do Motorista: ").strip()
        cnh = input("Número da CNH: ").strip()
        sistema.motoristas[nome] = Motorista(cnh, nome, sistema.rotas[cod_rota])
        print(f"✨ Motorista '{nome}' vinculado com sucesso à rota {cod_rota}!")
    else:
        print("❌ Rota não encontrada.")


def vincular_veiculo(sistema: SistemaTransporte) -> None:
    print("\n--- VINCULAR VEÍCULO AO MOTORISTA ---")
    if not sistema.motoristas:
        print("❌ Cadastre um motorista primeiro!")
        return

    print("Motoristas cadastrados:", list(sistema.motoristas.keys()))
    nome_mot = input("Digite o nome do motorista para receber o veículo: ").strip()

    if nome_mot in sistema.motoristas:
        placa = input("Placa do Veículo: ").strip()
        modelo = input("Modelo/Marca: ").strip()
        print("Selecione a Modalidade (LSP):")
        print("1 - Ônibus (Tarifa Normal)")
        print("2 - Metrô (Tarifa + 30%)")
        tipo = input("Opção: ").strip()

        veiculo: Veiculo = Onibus(placa, modelo) if tipo != "2" else Metro(placa, modelo)
        sistema.motoristas[nome_mot].veiculo = veiculo
        print(f"✨ Veículo {veiculo.obter_tipo()} ({placa}) alocado ao motorista {nome_mot}!")
    else:
        print("❌ Motorista não encontrado.")


def criar_cartao(sistema: SistemaTransporte) -> None:
    print("\n--- CRIAR CARTÃO DE TRANSPORTE ---")
    id_cartao = input("Número/ID do Cartão: ").strip()
    titular = input("Nome do Titular: ").strip()
    try:
        saldo = float(input("Saldo Inicial (R$): "))
        sistema.cartoes[id_cartao] = CartaoTransporte(id_cartao, titular, saldo)
        print(f"✨ Cartão {id_cartao} gerado para {titular}!")
    except ValueError:
        print("❌ Valor inválido para saldo.")


def simular_cobranca(sistema: SistemaTransporte) -> None:
    print("\n--- SIMULAR COBRANÇA ---")
    if not sistema.motoristas:
        print("❌ Sem motoristas ou linhas prontas para operar.")
        return

    print("Motoristas em operação:", list(sistema.motoristas.keys()))
    nome_mot = input("Quem está dirigindo nesta viagem? ").strip()

    if nome_mot not in sistema.motoristas:
        print("❌ Motorista inválido.")
        return

    motorista = sistema.motoristas[nome_mot]
    print("\nEscolha a Regra de Tarifa (OCP):")
    print("1 - Tarifa Padrão")
    print("2 - Horário de Pico (+25%)")
    print("3 - Desconto Estudantil (-50%)")
    opcao = input("Opção: ").strip()
    estrategia = selecionar_estrategia_tarifa(opcao)

    print("\nEscolha a Forma de Cobrança (DIP):")
    print("1 - Cartão de Transporte")
    print("2 - Dinheiro Físico na Catraca")
    op_pagamento = input("Opção: ").strip()

    if op_pagamento == "1":
        if not sistema.cartoes:
            print("❌ Nenhum cartão cadastrado no sistema.")
            return

        print("Cartões disponíveis:", list(sistema.cartoes.keys()))
        id_car = input("Digite o ID do cartão: ").strip()
        if id_car in sistema.cartoes:
            sistema.executar_cobranca(motorista, sistema.cartoes[id_car], estrategia)
        else:
            print("❌ Cartão não encontrado.")
    else:
        try:
            valor_cedula = float(input("Valor da nota entregue pelo passageiro (R$): "))
            sistema.executar_cobranca(motorista, PagamentoDinheiro(valor_cedula), estrategia)
        except ValueError:
            print("❌ Valor de cédula inválido.")


def listar_status(sistema: SistemaTransporte) -> None:
    print("\n--- STATUS DO SISTEMA & COBRANÇAS ---")
    print("\n🛒 Cartões Ativos:")
    for cartao in sistema.cartoes.values():
        print(f"  • {cartao.debugar_saldo()}")

    print("\n📋 Histórico de Cobranças Superiores:")
    if not sistema.historico_cobrancas:
        print("  Nenhuma cobrança efetuada ainda.")
    for log in sistema.historico_cobrancas:
        print(f"  {log}")


def menu_principal() -> None:
    sistema = SistemaTransporte()
    criar_dados_padrao(sistema)

    while True:
        print("\n" + "=" * 45)
        print("     SISTEMA DE TRANSPORTE URBANO (SOLID)     ")
        print("=" * 45)
        print("1. Criar Rota (Define valor da Tarifa)")
        print("2. Cadastrar Motorista para uma Rota")
        print("3. Cadastrar Veículo para um Motorista")
        print("4. Criar Cartão de Transporte (Saldo)")
        print("5. Simular Cobrança de Passagem (Viagem)")
        print("6. Listar Histórico de Cobranças / Status")
        print("0. Sair")
        print("=" * 45)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_rota(sistema)
        elif opcao == "2":
            cadastrar_motorista(sistema)
        elif opcao == "3":
            vincular_veiculo(sistema)
        elif opcao == "4":
            criar_cartao(sistema)
        elif opcao == "5":
            simular_cobranca(sistema)
        elif opcao == "6":
            listar_status(sistema)
        elif opcao == "0":
            print("\nEncerrando o sistema de transportes. Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
