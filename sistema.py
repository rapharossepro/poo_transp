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
        self.total_arrecadado: float = 0.0

    def calcular_valor_viagem(self, motorista: Motorista, estrategia_tarifa: EstrategiaTarifa) -> float:
        if not motorista.veiculo:
            return 0.0
        preco_da_rota = motorista.rota.tarifa_base
        multiplicador_veiculo = motorista.veiculo.obter_multiplicador_tarifa()
        valor_calculado = preco_da_rota * multiplicador_veiculo
        return estrategia_tarifa.calcular(valor_calculado)

    def executar_cobranca(self, motorista: Motorista, meio_pagamento: MeioDePagamento, estrategia_tarifa: EstrategiaTarifa):
        if not motorista.veiculo:
            print("❌ Erro: Este motorista está sem veículo alocado. Não pode operar a linha.")
            return

        valor_final = self.calcular_valor_viagem(motorista, estrategia_tarifa)

        if meio_pagamento.conferir_e_debitar(valor_final):
            log = (
                f"✅ Sucesso: R${valor_final:.2f} cobrados no [{meio_pagamento.debugar_saldo()}]. "
                f"Linha: {motorista.rota.codigo} via {motorista.veiculo.obter_tipo()}"
            )
            self.historico_cobrancas.append(log)
            self.total_arrecadado += valor_final
            print(log)
        else:
            print(f"❌ Falha: Meio de pagamento recusado ou saldo insuficiente para o valor de R${valor_final:.2f}")
