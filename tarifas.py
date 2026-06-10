from abc import ABC, abstractmethod


class EstrategiaTarifa(ABC):
    @abstractmethod
    def calcular(self, valor_base: float) -> float:
        pass


class TarifaPadrao(EstrategiaTarifa):
    def calcular(self, valor_base: float) -> float:
        return valor_base


class TarifaPico(EstrategiaTarifa):
    def calcular(self, valor_base: float) -> float:
        return valor_base * 1.25


class TarifaEstudantil(EstrategiaTarifa):
    def calcular(self, valor_base: float) -> float:
        return valor_base * 0.50
