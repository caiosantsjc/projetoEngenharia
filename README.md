# Sistema de Controle de Estoque

## Visão Geral
O **Sistema de Controle de Estoque** é uma aplicação de desktop desenvolvida em Python utilizando a biblioteca Tkinter para a interface gráfica e SQLite para o banco de dados. Este sistema é projetado para gerenciar produtos em um estoque, permitindo adicionar, editar, listar e buscar produtos.

## Estrutura do Projeto
O projeto é dividido em três componentes principais:

1. **Interface Gráfica (Tkinter)**: A parte visível da aplicação onde o usuário interage. A interface é dividida em diferentes "telas" ou "frames", cada uma com uma funcionalidade específica.
2. **Banco de Dados (SQLite)**: Armazena todas as informações dos produtos. O banco de dados é criado e manipulado pelo código Python.
3. **Lógica do Programa (Python)**: Gerencia a interação entre a interface gráfica e o banco de dados, realizando operações como adicionar, editar e buscar produtos.

## Componentes da Interface

### Tela Inicial (HomeFrame)
- **Descrição**: Tela principal do aplicativo.
- **Função**: Permite ao usuário escolher entre as opções de cadastro, gerenciamento ou busca de produtos.
- **Botões**:
  - *Cadastrar Produto*: Leva à tela de cadastro.
  - *Gerenciar Estoque*: Leva à tela de gerenciamento.
  - *Procurar Produto*: Leva à tela de busca.

### Tela de Cadastro (CadastroFrame)
- **Descrição**: Tela para inserir novos produtos no estoque.
- **Campos**: Nome, Quantidade e Preço.
- **Função**: Salva os dados do produto no banco de dados após validação dos inputs.

### Tela de Gerenciamento (GerenciamentoFrame)
- **Descrição**: Tela para visualizar e gerenciar produtos existentes.
- **Função**: Mostra uma lista de produtos e permite a edição de qualquer item ao clicar duas vezes em um deles.
- **Botão de Atualizar**: Atualiza a lista de produtos exibida.

### Tela de Busca (ProcurarFrame)
- **Descrição**: Tela para buscar produtos por nome.
- **Função**: Exibe os produtos que correspondem ao nome digitado pelo usuário.

## Banco de Dados

- **Criação**: O banco de dados `estoque.db` é criado automaticamente quando a aplicação é iniciada.
- **Estrutura**: Contém uma tabela chamada `produtos` com colunas para `id`, `nome`, `quantidade` e `preço`.
- **Operações**: O banco de dados armazena, atualiza e recupera informações sobre os produtos conforme as ações do usuário.

## Funções Principais

- **Conexão com o Banco de Dados**: Conecta ao banco de dados SQLite sempre que necessário.
- **Criação de Tabelas**: Cria a tabela `produtos` se ainda não existir.
- **Salvar Produto**: Insere um novo produto no banco de dados.
- **Carregar Dados**: Atualiza a lista de produtos exibida.
- **Editar Produto**: Permite modificar os detalhes de um produto existente.
- **Buscar Produto**: Pesquisa produtos pelo nome e exibe os resultados.

## Fluxo de Trabalho

1. **Início do Aplicativo**: Ao iniciar a aplicação, as tabelas no banco de dados são criadas.
2. **Interação do Usuário**:
   - O usuário escolhe uma das opções na tela inicial.
   - Dependendo da escolha, o usuário é levado para a tela correspondente onde pode cadastrar novos produtos, gerenciar o estoque ou procurar produtos.
3. **Manipulação de Dados**: O aplicativo manipula os dados no banco de dados conforme as ações realizadas pelo usuário.

## Requisitos para Funcionamento

- **Python**: A linguagem utilizada para a implementação do código.
- **Tkinter**: Biblioteca para a interface gráfica.
- **SQLite**: Banco de dados local.

## Como Executar o Projeto

1. **Clone o Repositório**
   ```bash
   git clone https://github.com/seuusuario/seurepositorio.git
