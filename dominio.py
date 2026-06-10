from typing import Optional
from transporte import Veiculo


class Rota:
    def __init__(self, codigo: str, destino: str, tarifa_base: float):
        self.codigo = codigo
        self.destino = destino
        self.tarifa_base = tarifa_base


class Motorista:
    def __init__(self, cnh: str, nome: str, rota: Rota):
        self.cnh = cnh
        self.nome = nome
        self.rota = rota
        self.veiculo: Optional[Veiculo] = None
