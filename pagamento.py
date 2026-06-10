from abc import ABC, abstractmethod


class MeioDePagamento(ABC):
    @abstractmethod
    def debugar_saldo(self) -> str:
        pass

    @abstractmethod
    def conferir_e_debitar(self, valor: float) -> bool:
        pass


class CartaoTransporte(MeioDePagamento):
    def __init__(self, id_cartao: str, titular: str, saldo_inicial: float):
        self.id_cartao = id_cartao
        self.titular = titular
        self.saldo = saldo_inicial

    def debugar_saldo(self) -> str:
        return f"Cartão {self.id_cartao} ({self.titular}) - Saldo: R${self.saldo:.2f}"

    def conferir_e_debitar(self, valor: float) -> bool:
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        return False


class PagamentoDinheiro(MeioDePagamento):
    def __init__(self, valor_entregue: float):
        self.valor_entregue = valor_entregue

    def debugar_saldo(self) -> str:
        return f"Dinheiro Físico - Cédula de: R${self.valor_entregue:.2f}"

    def conferir_e_debitar(self, valor: float) -> bool:
        return self.valor_entregue >= valor
