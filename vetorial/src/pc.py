from xml.dom import minidom
import unidecode
import re

import logging

logging.basicConfig(level=logging.DEBUG) # logging.DEBUG

totalB = 0

consul = {}
espera = {}

def read_LEIA(f: str):
    global totalB
    logging.debug("PC - read_LEIA - IN")
    logging.debug("PC - read_LEIA - Leitura do arquivo LEIA")
    arq = open(f, "r").read()
    totalB+=len(arq)
    doc = minidom.parseString(arq)
    m = 0
    for q in doc.getElementsByTagName("QUERY"):
        qnumber = q.getElementsByTagName("QueryNumber")[0].firstChild.nodeValue
        # logging.debug(qnumber)
        qtext = q.getElementsByTagName("QueryText")[0].firstChild.nodeValue
        # logging.debug(qtext)
        consul[qnumber] = re.sub("(?:[\\n\;])(?:[ ]+)"," ",unidecode.unidecode(qtext.upper()).strip())
        # logging.debug(cosul)
        espera[qnumber] = []
        for r in q.getElementsByTagName("Records"):
            for i in r.getElementsByTagName("Item"):
                for d in i.childNodes:
                    votos = 0
                    for v in i.getAttribute("score"):
                        votos+=int(v)
                    # logging.debug(f'{d.data} - {votos}')
                    espera[qnumber].append((d.data,votos))
        # logging.debug(m)
        m+=1
        
    logging.debug("PC - read_LEIA - OUT")

def read_config():
    global totalB
    logging.debug("PC - read_config - IN")
    logging.debug("PC - read_config - Leitura do arquivo de configuração")
    f = open("./config/PC.CFG", "r")
    linha = f.readlines()
    totalB+=len(linha[0])
    leia = linha[0].strip().split("=")[1]
    read_LEIA(leia)
    
    totalB+=len(linha[1])
    consultas = linha[1].strip().split("=")[1]
    logging.debug("PC - read_config - Leitura do arquivo CONSULTAS")
    saida = open(f"./result/{consultas}", "w")
    saida.write("QueryNumber;QueryText\n")
    for c in consul.items():
        saida.write(f"{c[0]};{c[1]}\n")
    saida.close()
    
    totalB+=len(linha[2])
    esperados = linha[2].strip().split("=")[1]
    logging.debug("PC - read_config - Leitura do arquivo ESPERADOS")
    saida = open(f"./result/{esperados}", "w")
    saida.write("QueryNumber;DocNumber;DocVotes\n")
    for e in espera.items():
        for doc in e[1]:
            saida.write(f"{e[0]};{doc[0]};{doc[1]}\n")
    saida.close()

    f.close()
    logging.debug("PC - read_config - OUT")


if __name__ == "__main__":
    logging.debug("PC - INICIO")
    try:
        read_config()
    except Exception as e:
        logging.debug(f"PC - ERROR: {e}")
    logging.debug(f"PC - TOTAL DE BYTES LIDOS - {totalB}")
    logging.debug("PC - FIM")