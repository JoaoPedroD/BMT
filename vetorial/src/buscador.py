import re
import time
import unidecode
import numpy as np
from math import sqrt
from nltk.tokenize import word_tokenize

import logging

totalB = 0

logging.basicConfig(level=logging.DEBUG) # logging.DEBUG WARNING

def realizar_consultas(consultas: str, modelo: dict) -> dict:
    global totalB
    logging.debug("BUSCADOR - realizar_consultas - IN")
    pattern = re.compile("[A-Z]{2,}")
    logging.debug("BUSCADOR - Leitura do arquivo CONSULTAS")
    f = open(f"./result/{consultas}", "r")
    resultado = {}
    tempo = []
    tempop = []
    tempod = []
    linhass = f.readlines()
    totalB+=len(linhass[0])
    for i in linhass[1:]:
        totalB+=len(i)
        start = time.time()
        id = i.split(";")[0]
        resultado[id] = {}
        numerador = {}
        denominadora = {}
        denominadorb = {}
        for c in word_tokenize(unidecode.unidecode(i.split(";")[1].strip())):
            startp = time.time()
            if pattern.fullmatch(c) is not None:
                if c in modelo:
                    for j in modelo[c]:
                        startd = time.time()
                        if j == "__idf__": continue
                        if j not in numerador: numerador[j] = 0
                        numerador[j]+=modelo[c][j]
                        if j not in denominadora: denominadora[j] = 0
                        if j not in denominadorb: denominadorb[j] = 0
                        denominadora[j]+=modelo[c][j]*modelo[c][j]
                        denominadorb[j]+=1*1
                        tempod.append(time.time() - startd)
            tempop.append(time.time() - startp)
        for i in numerador:
            if numerador[i] == 0:
                resultado[id][i] = 0
                continue
            resultado[id][i] = numerador[i]/(sqrt(denominadora[i])*sqrt(denominadorb[i]))
        resultado[id] = {key: val for key, val in sorted(resultado[id].items(), key = lambda ele: ele[1], reverse = True)}
        tempo.append(time.time() - start)
    f.close()
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo medio das consultas {np.mean(tempo)}")
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo total das consultas {np.sum(tempo)}")
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo medio das palavras {np.mean(tempop)}")
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo total das palavras {np.sum(tempop)}")
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo medio das documentos {np.mean(tempod)}")
    logging.debug(f"BUSCADOR - realizar_consultas - Tempo total das documentos {np.sum(tempod)}")
    logging.debug("BUSCADOR - realizar_consultas - OUT")
    return resultado

def escrver(saida: str, resultado: dict):
    global totalB
    logging.debug("BUSCADOR - escrver - IN")
    logging.debug("BUSCADOR - Leitura do arquivo RESULTADOS")
    f = open(f"./result/{saida}", "w")
    for i in resultado:
        p = 1
        for j in resultado[i]:
            f.write(f"{i};[{p},{j},{resultado[i][j]}]\n")
            p+=1
    f.close()
    logging.debug("BUSCADOR - escrver - OUT")

def carregar_modelo(modelo: str) -> dict:
    global totalB
    logging.debug("BUSCADOR - carregar_modelo")
    m = open(f"./result/{modelo}").read()
    logging.debug(f"BUSCADOR - Leitura do arquivo MODELO {len(m)}B")
    totalB+=len(m)
    return eval(m)
    
def read_config():
    global totalB
    logging.debug("BUSCADOR - read_config - IN")
    f = open("./config/BUSCA.CFG", "r")
    modelo = None
    resulado = None
    for linha in f.readlines():
        totalB+=len(linha)
        l = linha.split("=")
        if l[0] == "MODELO":
            logging.debug(f"MODELO {l[1].strip()}")
            modelo = carregar_modelo(l[1].strip())
        elif l[0] == "CONSULTAS":
            logging.debug("CONSULTAS")
            resulado = realizar_consultas(l[1].strip(), modelo)
        elif l[0] == "RESULTADOS":
            logging.debug("RESULTADOS")
            escrver(l[1].strip(), resulado)
    f.close()
    logging.debug("BUSCADOR - read_config - OUT")


if __name__ == "__main__":
    logging.debug("BUSCADOR - INICIO")
    read_config()
    logging.debug(f"BUSCADOR - TOTAL DE BYTES LIDOS - {totalB}")
    logging.debug("BUSCADOR - FIM")