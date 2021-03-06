from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from xml.dom import minidom
import unidecode

import logging

logging.basicConfig(level=logging.DEBUG) # logging.DEBUG

gli = {}
totalB = 0

stemming = False

def gera_lista(renum: str, data: str):
    # logging.info("GLI - gera_lista - IN")
    global stemming
    if stemming: ps = PorterStemmer()
    for p in word_tokenize(data):
        if p == ";": continue
        if stemming: p = ps.stem(p).upper()
        p = unidecode.unidecode(p.upper())
        if p in gli:
            gli[p].append(renum.strip())
        else:
            gli[p] = [renum.strip()]
    # logging.info("GLI - gera_lista - OUT")
        
        

def read_LEIA(f: str):
    logging.debug("GLI - read_LEIA - IN")
    logging.debug("GLI - read_LEIA - Leitura do arquivo LEIA")
    global totalB
    try:
        arq = open(f, "r").read()
    except Exception as e:
        logging.debug(f"GLI - read_LEIA - Não foi possiver abrir o arquivo {f}")
        logging.debug(f"GLI - read_LEIA - ERROR: {e}")
        return
    totalB+=len(arq)
    doc = minidom.parseString(arq)
    for r in doc.getElementsByTagName("RECORD"):
        abst = r.getElementsByTagName("ABSTRACT")
        
        if not len(abst):
            abst = r.getElementsByTagName("EXTRACT")
        if not len(abst):
            abst = r.getElementsByTagName("TITLE")
        if len(abst) == 0: continue
        
        recnum = r.getElementsByTagName("RECORDNUM")[0].firstChild.nodeValue
        # logging.debug(recnum)
        
        for a in abst:
            for i in a.childNodes:
                gera_lista(recnum, i.data)
    logging.debug("GLI - read_LEIA - OUT")
        

def read_config():
    logging.debug("GLI - read_config - IN")
    logging.debug("GLI - read_config - Leitura do arquivo de configuração")
    f = open("./config/GLI.CFG", "r")
    global totalB
    global stemming
    for linha in f.readlines():
        totalB+=len(linha)
        l = linha.split("=")
        if l[0].strip() == "STEMMER":
            stemming = True
        elif l[0].strip() == "NOSTEMMER":
            stemming = False
        elif l[0] == "LEIA":
            read_LEIA(l[1].strip())
        elif l[0] == "ESCREVA":
            l = l[1].strip().split(".")
            saida = open(f"./result/{l[0].strip()}-{'STEMMER' if stemming else 'NOSTEMMER'}.{l[1]}","w")
            for g in gli.items():
                lista = list(g[1])
                lista.sort()
                saida.write(f"{g[0]};{lista}\n")
            saida.close()
    f.close()
    logging.debug("GLI - read_config - OUT")

if __name__ == "__main__":
    logging.debug("GLI - INICIO")
    try:
        read_config()
    except Exception as e:
        logging.debug(f"GLI - ERROR: {e}")
    logging.debug(f"GLI - TOTAL DE BYTES LIDOS - {totalB}")
    logging.debug("GLI - FIM")