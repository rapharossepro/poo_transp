import random
import string
from typing import Optional
from dominio import Motorista, Rota
from pagamento import CartaoTransporte, PagamentoDinheiro
from sistema import SistemaTransporte
from tarifas import TarifaPadrao, TarifaPico, TarifaEstudantil, EstrategiaTarifa
from transporte import Metro, Onibus, Veiculo


def criar_dados_padrao(sistema: SistemaTransporte) -> None:
    # 3 Rotas Padrão
    r1 = Rota("101", "Sao Jose", 4.50)
    r2 = Rota("202", "Inoa", 5.00)
    r3 = Rota("303", "Itaipuacu", 3.80)
    sistema.rotas.update({r1.codigo: r1, r2.codigo: r2, r3.codigo: r3})

    # 3 Motoristas e Veículos Padrão
    m1 = Motorista("11111111111", "Carlos Silva", r1)
    m1.veiculo = Onibus("ABC-1234", "Mercedes-Benz")
    m2 = Motorista("22222222222", "Maria Oliveira", r2)
    m2.veiculo = Metro("XYZ-9876", "Alstom")
    m3 = Motorista("33333333333", "Joao Santos", r3)
    m3.veiculo = Onibus("DEF-5678", "Volvo")
    sistema.motoristas.update({m1.nome: m1, m2.nome: m2, m3.nome: m3})

    # 3 Cartões Padrão
    c1 = CartaoTransporte("888", "Ana Costa (Estudante)", 50.00)
    c2 = CartaoTransporte("999", "Pedro Alves", 100.00)
    c3 = CartaoTransporte("777", "Mariana Lima", 20.00)
    sistema.cartoes.update({c1.id_cartao: c1, c2.id_cartao: c2, c3.id_cartao: c3})

    # Histórico fake gerado executando cobranças reais na inicialização
    print("⏳ Carregando dados do sistema e gerando histórico de viagens...\n")
    sistema.executar_cobranca(m1, c2, TarifaPadrao())
    sistema.executar_cobranca(m3, c1, TarifaEstudantil())
    sistema.executar_cobranca(m2, c3, TarifaPico())
    sistema.executar_cobranca(m1, PagamentoDinheiro(10.00), TarifaPadrao())


def selecionar_estrategia_tarifa(opcao: str) -> EstrategiaTarifa:
    if opcao == "2":
        return TarifaPico()
    if opcao == "3":
        return TarifaEstudantil()
    return TarifaPadrao()


def criar_rota(sistema: SistemaTransporte) -> None:
    print("\n--- CRIAR NOVA ROTA ---")
    if sistema.rotas:
        print("Rotas já cadastradas:")
        for rota in sistema.rotas.values():
            print(f"  • Rota {rota.codigo}: {rota.destino} - Tarifa Base: R${rota.tarifa_base:.2f}")
        print("-" * 25)

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
        cnh = input("Número da CNH (deixe em branco para gerar aleatório): ").strip()
        
        if not cnh:
            cnh = str(random.randint(10000000000, 99999999999))
            print(f"ℹ️  CNH gerada automaticamente: {cnh}")
            
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
        placa = input("Placa do Veículo (deixe em branco para gerar aleatório): ").strip()
        
        if not placa:
            letras = ''.join(random.choices(string.ascii_uppercase, k=3))
            numeros = f"{random.randint(0, 9999):04d}"
            placa = f"{letras}-{numeros}"
            print(f"ℹ️  Placa gerada automaticamente: {placa}")
            
        modelo = input("Modelo/Marca: ").strip()
        print("Selecione a Modalidade (LSP):")
        print("1 - Ônibus (Tarifa Normal)")
        print("2 - Metrô (Tarifa + 30%)")
        tipo = input("Opção: ").strip()

        if tipo == "1":
            veiculo: Veiculo = Onibus(placa, modelo)
        elif tipo == "2":
            veiculo = Metro(placa, modelo)
        else:
            print("❌ Opção de veículo inválida. Operação cancelada.")
            return
            
        sistema.motoristas[nome_mot].veiculo = veiculo
        print(f"✨ Veículo {veiculo.obter_tipo()} ({placa}) alocado ao motorista {nome_mot}!")
    else:
        print("❌ Motorista não encontrado.")


def criar_cartao(sistema: SistemaTransporte) -> None:
    print("\n--- CRIAR CARTÃO DE TRANSPORTE ---")
    id_cartao = input("Número/ID do Cartão (deixe em branco para gerar aleatório): ").strip()

    if not id_cartao:
        id_cartao = str(random.randint(100000, 999999))
        nomes = ["Ana", "Carlos", "Beatriz", "João", "Mariana", "Lucas", "Fernanda", "Rafael"]
        sobrenomes = ["Silva", "Costa", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves"]
        titular = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        saldo = round(random.uniform(10.0, 100.0), 2)
        sistema.cartoes[id_cartao] = CartaoTransporte(id_cartao, titular, saldo)
        print(f"ℹ️  Cartão gerado automaticamente: ID {id_cartao} | Titular: {titular} | Saldo: R${saldo:.2f}")
        return
        
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

    print("Motoristas em operação:")
    for m in sistema.motoristas.values():
        print(f"  • {m.nome} (Rota {m.rota.codigo})")
    nome_mot = input("\nQuem está dirigindo nesta viagem? ").strip()

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

    valor_passagem = sistema.calcular_valor_viagem(motorista, estrategia)
    print(f"\n💵 Valor calculado para esta viagem: R${valor_passagem:.2f}")

    print("\nEscolha a Forma de Cobrança (DIP):")
    print("1 - Cartão de Transporte")
    print("2 - Dinheiro Físico na Catraca")
    op_pagamento = input("Opção: ").strip()

    if op_pagamento == "1":
        if not sistema.cartoes:
            print("❌ Nenhum cartão cadastrado no sistema.")
            return

        print("\nCartões disponíveis:")
        for c in sistema.cartoes.values():
            print(f"  • ID: {c.id_cartao} | {c.titular} (Saldo: R${c.saldo:.2f})")
            
        id_car = input("\nDigite o ID do cartão: ").strip()
        if id_car in sistema.cartoes:
            print("\n--- RESULTADO DA COBRANÇA ---")
            sistema.executar_cobranca(motorista, sistema.cartoes[id_car], estrategia)
            print(f"📊 Status atualizado: {sistema.cartoes[id_car].debugar_saldo()}")
            print("-" * 29)
        else:
            print("❌ Cartão não encontrado.")
    elif op_pagamento == "2":
        try:
            valor_cedula = float(input("Valor da nota entregue pelo passageiro (R$): "))
            print("\n--- RESULTADO DA COBRANÇA ---")
            sistema.executar_cobranca(motorista, PagamentoDinheiro(valor_cedula), estrategia)
            print("-" * 29)
        except ValueError:
            print("❌ Valor de cédula inválido.")
    else:
        print("❌ Opção de pagamento inválida.")


def listar_status(sistema: SistemaTransporte) -> None:
    print("\n--- STATUS FINANCEIRO E COBRANÇAS ---")

    print("\n Cartões Ativos:")
    for cartao in sistema.cartoes.values():
        print(f"  • {cartao.debugar_saldo()}")

    print("\n📋 Histórico de Cobranças:")
    if not sistema.historico_cobrancas:
        print("  Nenhuma cobrança efetuada ainda.")
    for log in sistema.historico_cobrancas:
        print(f"  {log}")

    print("-" * 45)
    print(f"💰 TOTAL ARRECADADO NO SISTEMA: R${sistema.total_arrecadado:.2f}")
    print("-" * 45)


def exibir_cadastros(sistema: SistemaTransporte) -> None:
    print("\n--- LISTA DE CADASTROS (ROTAS / MOTORISTAS / VEÍCULOS) ---")
    
    print("\n🛣️  Rotas Cadastradas:")
    if not sistema.rotas:
        print("  Nenhuma rota cadastrada.")
    for rota in sistema.rotas.values():
        print(f"  • Rota {rota.codigo}: {rota.destino} - Tarifa Base: R${rota.tarifa_base:.2f}")

    print("\n👨‍✈️ Motoristas Cadastrados:")
    if not sistema.motoristas:
        print("  Nenhum motorista cadastrado.")
    for motorista in sistema.motoristas.values():
        print(f"  • {motorista.nome} (CNH: {motorista.cnh}) - Rota alocada: {motorista.rota.codigo}")

    print("\n🚌 Veículos da Frota:")
    veiculos_encontrados = False
    for motorista in sistema.motoristas.values():
        if motorista.veiculo:
            veiculos_encontrados = True
            print(f"  • {motorista.veiculo.obter_tipo()} | Placa: {motorista.veiculo.placa} | Modelo: {motorista.veiculo.modelo} (Conduzido por: {motorista.nome})")
    if not veiculos_encontrados:
        print("  Nenhum veículo vinculado à frota no momento.")


def salvar_relatorio(sistema: SistemaTransporte) -> None:
    with open("relatorio_final.txt", "w", encoding="utf-8") as f:
        f.write("--- RELATÓRIO FINAL DE COBRANÇAS ---\n\n")
        if not sistema.historico_cobrancas:
            f.write("Nenhuma cobrança efetuada nesta sessão.\n")
        else:
            for log in sistema.historico_cobrancas:
                f.write(f"{log}\n")
        f.write("\n" + "-" * 45 + "\n")
        f.write(f"TOTAL ARRECADADO NO SISTEMA: R${sistema.total_arrecadado:.2f}\n")
        f.write("-" * 45 + "\n")
    print("📄 Relatório salvo com sucesso em 'relatorio_final.txt'!")


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
        print("7. Exibir Cadastros (Rotas/Motoristas/Veículos)")
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
        elif opcao == "7":
            exibir_cadastros(sistema)
        elif opcao == "0":
            print("\nEncerrando o sistema de transportes...")
            salvar_relatorio(sistema)
            print("Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            
        input("\nPressione Enter para continuar...")
