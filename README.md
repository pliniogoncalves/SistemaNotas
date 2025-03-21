# Sistema de Gerenciamento de Notas de Estudantes

Este projeto é um sistema de gerenciamento de notas de estudantes desenvolvido em Python, utilizando a biblioteca `tkinter` para a interface gráfica. O sistema permite adicionar estudantes, calcular suas médias, classificá-los em aprovados, em recuperação ou reprovados, e remover estudantes da lista.

## Funcionalidades

- **Adicionar Estudante:** Insere um estudante com nome e três notas.
- **Remover Estudante:** Remove um estudante selecionado da lista.
- **Classificação Automática:** Classifica os estudantes em:
  - Aprovados (média >= 7).
  - Recuperação (5 <= média < 7).
  - Reprovados (média < 5).
- **Validação de Dados:** Valida o nome do estudante e as notas (devem estar entre 1 e 10).

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.x instalado.
- Biblioteca `tkinter` (já vem instalada com o Python).

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/SistemaNotasV2.git
2. Navegue até a pasta do projeto:
   ```
   cd SistemaNotasV2
3. Execute o arquivo principal:
    ```bash
    py sistemaNotas.py
    
## Executando os Testes

### Para rodar os testes unitários, execute o seguinte comando:
   ```bash
   git clone https://github.com/seu-usuario/SistemaNotasV2.git
  ```
## Estrutura do Código

### `sistemaNotas.py`
<ul>
  <li>Classe SistemaEstudantes:
    <ul>
      <li>Gerencia a lista de estudantes e suas médias.</li>
      <li>Contém métodos para adicionar, remover e atualizar estudantes.</li>
      <li>Utiliza funções de alta ordem, closures, lambdas e list comprehensions.</li>
    </ul>
  </li>
</ul>

<ul>
  <li>Interface Gráfica:
    <ul>
      <li>Desenvolvida com `tkinter`.</li>
      <li>Inclui campos para inserir nome e notas, botões para adicionar/remover estudantes e uma lista para exibir o ranking.</li>
    </ul>
  </li>
</ul>

### `test_sistemaNotas.py`
<ul>
  <li>Testes Unitários:
    <ul>
      <li>Cobrem a validação de entradas, adição de estudantes, remoção de estudantes e classificação automática.</li>
      <li>Utiliza a biblioteca unittest e unittest.mock para simular a interface gráfica.</li>
    </ul>
  </li>
</ul>

## Conceitos de Programação Funcional Utilizados

<ul>
  <li>Função Lambda: Usada para ordenar estudantes por média.</li>
  <li>List Comprehension: Usada para filtrar estudantes em aprovados, recuperação e reprovados.</li>
  <li>Closure: Usada no método criar_adicionador para capturar variáveis do escopo externo.</li>
  <li>Função de Alta Ordem: O método criar_validador recebe uma função como argumento e retorna outra função.</li>
</ul>
