from typing import Dict, List
from dominio import Motorista, Rota
from pagamento import CartaoTransporte, MeioDePagamento
from tarifas import EstrategiaTarifa


class SistemaTransporte:
    def __init__(self):
        self.rotas: Dict[str, Rota] = {}
        self.motoristas: Dict[str, Motorista] = {}
        self.cartoes: Dict[str, CartaoTransporte] = {}
        self.historico_cobrancas: List[str] = []

    def executar_cobranca(self, motorista: Motorista, meio_pagamento: MeioDePagamento, estrategia_tarifa: EstrategiaTarifa):
        if not motorista.veiculo:
            print("❌ Erro: Este motorista está sem veículo alocado. Não pode operar a linha.")
            return

        preco_da_rota = motorista.rota.tarifa_base
        multiplicador_veiculo = motorista.veiculo.obter_multiplicador_tarifa()

        valor_calculado = preco_da_rota * multiplicador_veiculo
        valor_final = estrategia_tarifa.calcular(valor_calculado)

        if meio_pagamento.conferir_e_debitar(valor_final):
            log = (
                f"✅ Sucesso: R${valor_final:.2f} cobrados no [{meio_pagamento.debugar_saldo()}]. "
                f"Linha: {motorista.rota.codigo} via {motorista.veiculo.obter_tipo()}"
            )
            self.historico_cobrancas.append(log)
            print(log)
        else:
            print(f"❌ Falha: Meio de pagamento recusado ou saldo insuficiente para o valor de R${valor_final:.2f}")
