# Comparação entre Algoritmo Guloso e Programação Dinâmica

Projeto desenvolvido para comparar duas abordagens de solução para o Problema da Seleção de Atividades:

- algoritmo guloso
- algoritmo de programação dinâmica

O objetivo é mostrar como as duas estratégias resolvem o mesmo problema, comparar corretude, custo computacional e gerar artefatos que apoiem o trabalho acadêmico.

## Problema resolvido

Dado um conjunto de atividades com horário de início e fim, o objetivo é selecionar o maior número possível de atividades compatíveis, ou seja, que não se sobreponham no tempo.

Neste projeto:

- a abordagem gulosa escolhe sempre a atividade compatível com menor horário de término
- a abordagem dinâmica calcula a melhor solução ótima considerando as combinações compatíveis anteriores

## Estrutura do projeto

```text
.
├── activity_selection/
│   ├── algorithms.py
│   ├── benchmark.py
│   ├── datasets.py
│   └── models.py
├── docs/
│   └── atividade_pratica.md
├── results/
│   └── benchmark_results.csv
├── tests/
│   └── test_activity_selection.py
├── main.py
└── Trabalho_Final (2).pdf
```

## Pré-requisitos

- Python 3.12 ou superior
- ambiente virtual Python opcional, mas recomendado

Se quiser usar o ambiente virtual já existente no diretório:

```bash
source .venv/bin/activate
```

Se preferir criar um novo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

O projeto usa apenas biblioteca padrão do Python, então não há dependências externas para instalar.

## Como executar

### 1. Exemplo manual

Executa uma instância conhecida e imprime o resultado dos dois algoritmos.

```bash
python main.py example
```

Saída esperada, em formato semelhante a:

```text
Exemplo manual
algoritmo=greedy quantidade=4 comparacoes=11 selecionadas=[A(1-4), D(5-7), H(8-11), K(12-16)]
algoritmo=dynamic_programming quantidade=4 comparacoes=22 selecionadas=[A(1-4), D(5-7), H(8-11), K(12-16)]
```

### 2. Benchmark comparativo

Executa medições com diferentes tamanhos de entrada e perfis de sobreposição, salvando os resultados em CSV.

```bash
python main.py benchmark
```

Para definir outro caminho de saída:

```bash
python main.py benchmark --output results/meu_benchmark.csv
```

O benchmark mede:

- tempo de execução
- uso de memória
- quantidade de comparações
- quantidade de atividades selecionadas

### 3. Atividade prática para a turma

Mostra uma instância guiada para execução manual do algoritmo em sala.

```bash
python main.py classroom
```

O roteiro detalhado também está em [docs/atividade_pratica.md](docs/atividade_pratica.md).

## Como testar

Execute a suíte automatizada com:

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem:

- entrada vazia
- uma única atividade
- atividades totalmente compatíveis
- atividades totalmente conflitantes
- empates no horário de término
- múltiplas soluções ótimas
- validação de ausência de sobreposição
- comparação com ótimo conhecido

## Principais arquivos

- [main.py](main.py): interface de linha de comando para exemplo, benchmark e atividade prática
- [activity_selection/algorithms.py](activity_selection/algorithms.py): implementação dos algoritmos guloso e de programação dinâmica
- [activity_selection/datasets.py](activity_selection/datasets.py): instâncias de exemplo e geração de dados aleatórios
- [activity_selection/benchmark.py](activity_selection/benchmark.py): execução e persistência dos experimentos em CSV
- [tests/test_activity_selection.py](tests/test_activity_selection.py): testes automatizados

## Resultados gerados

O arquivo [results/benchmark_results.csv](results/benchmark_results.csv) contém os resultados dos experimentos já executados no projeto.

Cada linha registra:

- algoritmo utilizado
- perfil de sobreposição
- tamanho da entrada
- repetição
- quantidade de atividades selecionadas
- tempo em nanossegundos
- pico de memória em bytes
- número de comparações

## Observações

- O algoritmo guloso é a solução clássica e ótima para este problema quando ordenado por menor horário de término.
- A versão de programação dinâmica foi mantida para comparação acadêmica entre abordagens.
- O PDF [Trabalho_Final (2).pdf](<Trabalho_Final (2).pdf>) permanece no repositório como referência do enunciado.
