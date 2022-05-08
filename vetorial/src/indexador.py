from math import log
import re

import logging

totalB = 0

logging.basicConfig(level=logging.DEBUG) # logging.DEBUG

def cada_documento(linhas: list) -> dict:
    logging.debug("IDX - cada_documento - IN")
    documentos = {}
    for l in linhas:
        # logging.debug(l.split(";")[1])
        docs = eval(l.split(";")[1])
        for d in docs:
            if d in documentos:
                documentos[d]+=1
            else:
                documentos[d]=1
    logging.debug("IDX - cada_documento - OUT")
    return documentos

def cada_palavra_documento(linhas: list) -> dict:
    logging.debug("IDX - cada_palavra_documento - IN")
    documentos = {}
    global totalB
    pattern = re.compile("[A-Z]{2,}")
    for l in linhas:
        totalB+=len(l)
        aux = l.split(";")
        docs = eval(aux[1])
        for d in docs:
            saux = aux[0].strip()
            if len(saux) < 2 or pattern.fullmatch(saux) is None: continue
            if d in documentos:
                if saux in documentos[d]:
                    documentos[d][saux]+=1
                else:
                    documentos[d][saux]=1
            else:
                documentos[d]={saux:1}
                
    logging.debug("IDX - cada_palavra_documento - OUT")
    return documentos

def contar_documentos(linhas: list) -> int:
    logging.debug("IDX - contar_documentos - IN")
    documentos = set()
    for l in linhas:
        documentos |= set(eval(l.split(";")[1]))
    logging.debug("IDX - contar_documentos - OUT")
    return len(sorted(documentos))

def calc_tf(f: dict) -> dict:
    logging.debug("IDX - calc_tf - IN")
    for i in f:
        for j in f[i]:
            f[i][j] = f[i][j]/max(f[i].values())
    logging.debug("IDX - calc_tf - OUT")
    return f

def calc_idf(N: int, linhas: list) -> dict:
    logging.debug("IDX - calc_idf - IN")
    idf = {}
    pattern = re.compile("[A-Z]{2,}")
    for l in linhas:
        aux = l.split(";")
        saux = aux[0].strip()
        if len(saux) < 2 or pattern.fullmatch(saux) is None: continue
        ni = len(sorted(set(eval(aux[1]))))
        idf[saux] = log(N/ni, 10)
    logging.debug("IDX - calc_idf - OUT")
    return idf

def calc_w(tf: dict, idf: dict) -> dict:
    logging.debug("IDX - calc_w - IN")
    w = {}
    for i in idf:
        for t in tf:
            if i not in w: w[i] = {}
            # w[i]["__idf__"] = idf[i]
            if i in tf[t]:
                # w[i][t] = (tf[t][i]*idf[i], tf[t][i])
                w[i][t] = tf[t][i]*idf[i]
            else:
                # w[i][t] = (0*idf[i], 0)
                w[i][t] = 0*idf[i]
    logging.debug("IDX - calc_w - OUT")
    return w
    
def read_LEIA(f: str):
    logging.debug("IDX - read_LEIA - IN")
    logging.debug("IDX - read_LEIA - Leitura do arquivo LEIA")
    f = open(f"./result/{f}", "r")
    linhas = f.readlines()
    
    f = cada_palavra_documento(linhas)
    
    tf = calc_tf(f)
    
    N = contar_documentos(linhas)
    
    idf = calc_idf(N, linhas)
    
    w = calc_w(tf, idf)
    
    logging.debug("IDX - read_LEIA - OUT")
    return w    

def escreva(nome: str, w: dict):
    logging.debug("IDX - escreva - IN")
    logging.debug("IDX - read_LEIA - Leitura do arquivo ESCREVA")
    f = open(f"./result/{nome}", "w")
    f.write(re.sub("[ ]+","",str(w)))
    f.close()
    logging.debug("IDX - escreva - OUT")
    

def read_config():
    global totalB
    logging.debug("IDX - read_config - IN")
    logging.debug("IDX - read_config - Leitura do arquivo de configuração")
    f = open("./config/INDEX.CFG", "r")
    w = None
    for linha in f.readlines():
        totalB+=len(linha)
        l = linha.split("=")
        if l[0] == "LEIA":
            w = read_LEIA(l[1].strip())
        elif l[0] == "ESCREVA":
            escreva(l[1].strip(), w)
    f.close()
    logging.debug("IDX - read_config - OUT")

if __name__ == "__main__":
    logging.debug("IDX - INICIO")
    try:
        read_config()
    except Exception as e:
        logging.debug(f"IDX - ERROR: {e}")
    logging.debug(f"IDX - TOTAL DE BYTES LIDOS - {totalB}")
    logging.debug("IDX - FIM")