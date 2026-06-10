from abc import ABC, abstractmethod


class Veiculo(ABC):
    def __init__(self, placa: str, modelo: str):
        self.placa = placa
        self.modelo = modelo

    @abstractmethod
    def obter_tipo(self) -> str:
        pass

    @abstractmethod
    def obter_multiplicador_tarifa(self) -> float:
        pass


class Onibus(Veiculo):
    def obter_tipo(self) -> str:
        return "Ônibus"

    def obter_multiplicador_tarifa(self) -> float:
        return 1.0


class Metro(Veiculo):
    def obter_tipo(self) -> str:
        return "Metrô"

    def obter_multiplicador_tarifa(self) -> float:
        return 1.3

"""class Van(Veiculo):
    def obter_tipo(self) -> str:
        return "Van"

    def obter_multiplicador_tarifa(self) -> float:
        return 0.8
"""

"""class Taxi(Veiculo):
    def obter_tipo(self) -> str:
        return "Táxi"

    def obter_multiplicador_tarifa(self) -> float:
        return 2.5
"""