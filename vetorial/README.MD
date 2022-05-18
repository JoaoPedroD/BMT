# Modelo vetorial

Implementação do modelo vetorial para o trabalho de BMT

## Getting Started

Essas instruções fornecerão uma cópia do projeto e modo de utilização para uso do código do trabalho.

### Pré-requisito

O programa foi feito com Python versão 3.8

Neste trabalho foram utilizadas as seguintes libs da linguagem Python:
- logging
- math
- nltk
- re
- time
- unidecode
- matplotlib
- xml

## Execução

O código pode ser executado no terminal com o
arquivo run.sh, que se encontra na raiz do projeto, com seguinte 
comando(Lembrar de permitir a execução do script):

```sh
./run.sh
```

ou

```sh
python3 src/<arquivo desejado>
```

Foi adicionado ao projeto o arquivo chamado metricas.py, cuja função é calcular as metricas do sistema. Para sua execução basta utilizar o comando 
```sh
python3 src/metricas.py
```
e configurar o arquivo config/METRICAS.CFG  

A primeira linha tem o parametro EXPECTATIVA com os Resultados Esperados.

A segunda tem o parametro RESULTADO_A com o resultado do sistema A.

Por fim, a terceira tem o parametro RESULTADO_B com o resultado do sistema B

## Autor

  - **João Pedro**
