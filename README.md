# Sistema de Transporte Urbano (SOLID)

Este projeto em Python simula um sistema básico de transporte urbano com motoristas, rotas, veículos, tarifas e meios de pagamento. A aplicação foi modularizada para separar responsabilidades e facilitar a manutenção.

## Estrutura do projeto

- `app_terminal.py`
  - Entrada principal do sistema. Inicia a interface de terminal que usa os módulos separados.
- `cli.py`
  - Contém a interface de linha de comando e as funções de interação com o usuário.
- `dominio.py`
  - Modelos de domínio: `Rota` e `Motorista`.
- `transporte.py`
  - Tipos de transporte: `Veiculo`, `Onibus` e `Metro`.
- `tarifas.py`
  - Estratégias de tarifa: `TarifaPadrao`, `TarifaPico`, `TarifaEstudantil`.
- `pagamento.py`
  - Abstração e implementações de pagamento: `MeioDePagamento`, `CartaoTransporte`, `PagamentoDinheiro`.
- `sistema.py`
  - Regras centrais de negócio: classe `SistemaTransporte` e método `executar_cobranca`.

## Como usar

1. Abra um terminal no diretório do projeto.
2. Execute:

```bash
python app_terminal.py
```

3. Use o menu para:
- Criar rotas
- Cadastrar motoristas
- Vincular veículos a motoristas
- Criar cartões de transporte
- Simular cobranças de passagem
- Verificar o histórico de cobranças

## Como o código foi criado

A aplicação original estava em um único arquivo com todas as classes e a interface de terminal. A modularização dividiu o sistema em camadas claras:

- `dominio.py` guarda as entidades do negócio.
- `transporte.py` define o comportamento polimórfico de veículos.
- `tarifas.py` encapsula as regras de cálculo de tarifa.
- `pagamento.py` abstrai o processamento de diferentes meios de pagamento.
- `sistema.py` centraliza a lógica de cobrança e histórico.
- `cli.py` organiza a interface de usuário e delega ações para o sistema.
- `app_terminal.py` é um ponto de entrada leve para iniciar o programa.

## Princípios SOLID aplicados

### S — Single Responsibility Principle

Cada módulo agora tem uma responsabilidade única:
- `dominio.py`: entidades de domínio.
- `transporte.py`: regras de veículos.
- `tarifas.py`: políticas de tarifa.
- `pagamento.py`: processamento de pagamento.
- `sistema.py`: orquestração do negócio.
- `cli.py`: interface com o usuário.

### O — Open/Closed Principle

A classe `EstrategiaTarifa` em `tarifas.py` permite adicionar novos tipos de tarifa sem alterar as classes existentes. A lógica de cobrança usa a abstração e permanece fechada para modificações diretas.

### L — Liskov Substitution Principle

Os veículos `Onibus` e `Metro` estendem `Veiculo` e podem ser usados onde quer que um `Veiculo` seja esperado. O sistema aplica o multiplicador de tarifa sem precisar saber o tipo exato de veículo.

### I — Interface Segregation Principle

Cada abstração é pequena e específica:
- `MeioDePagamento` define apenas o que o sistema precisa para processar pagamentos.
- `EstrategiaTarifa` define apenas o cálculo do valor.

### D — Dependency Inversion Principle
O `SistemaTransporte` depende de abstrações (`MeioDePagamento`, `EstrategiaTarifa`), não de implementações concretas. Assim, o sistema aceita `CartaoTransporte` ou `PagamentoDinheiro` sem mudanças.

## Destaque de Arquitetura: O Poder das Interfaces

No arquivo `pagamento.py`, a classe `MeioDePagamento` é uma Classe Abstrata (Interface) sem implementação lógica, contendo apenas assinaturas de métodos. Isso reflete uma das ferramentas mais poderosas da Orientação a Objetos:

- **Contrato Obrigatório**: A classe dita as regras. Qualquer meio de pagamento adicionado ao sistema é OBRIGADO a ter os métodos `debugar_saldo` e `conferir_e_debitar`.
- **Polimorfismo na Prática**: A responsabilidade da lógica é empurrada para as classes filhas:
  - O `CartaoTransporte` precisa validar o saldo suficiente e subtrair o valor do seu estado interno.
  - O `PagamentoDinheiro` apenas valida se a cédula entregue cobre o custo da passagem.

Isso blinda a classe `SistemaTransporte`, que executa a cobrança chamando `meio_pagamento.conferir_e_debitar(valor_final)` sem ter a menor ideia da lógica de pagamento por trás (ela apenas confia no contrato).

Se `MeioDePagamento` tivesse lógica genérica implementada com base no uso de `if/else` para avaliar o tipo de pagamento, quebraríamos o Princípio do Aberto/Fechado (OCP) e o Princípio da Inversão de Dependência (DIP). Da forma como foi desenhado, o "core" de pagamentos do sistema está perfeitamente protegido e desacoplado!

## Observações finais

A modularização torna o projeto mais fácil de estender e testar. Para evoluir o sistema, basta adicionar novas estratégias, meios de pagamento ou tipos de veículo nos módulos específicos, sem alterar a lógica de cobrança central.

