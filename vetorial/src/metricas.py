import matplotlib.pyplot as plt
from math import log
import pandas as pd

expec = {}
expecRel = {}
resultA = {}
resultB = {}
jaadd = {}
SAIDA = ""

f = open("./config/METRICAS.CFG", "r")
linhas = f.readlines()
# print(linha)

f = open(f"./result/{linhas[0].strip().split('=')[1]}", "r")
for i in f.readlines()[1:]:
    linha = i.strip().split(";")
    if linha[0] not in expec: expec[linha[0]] = []
    if linha[0] not in expecRel: expecRel[linha[0]] = {}
    if linha[0] not in jaadd: jaadd[linha[0]] = []
    if linha[1].lstrip("0") in expec[linha[0]]: continue
    expec[linha[0]].append(linha[1].lstrip("0"))
    expecRel[linha[0]][linha[1].lstrip("0")] = int(linha[2])
f.close()
del(jaadd)
# print(linhas[1])
Astem = False if "NOSTEMMER" in linhas[1].strip().split('=')[1] else True
f = open(f"./result/{linhas[1].strip().split('=')[1]}", "r")
for i in f.readlines():
    linha = i.strip().split(";")
    if linha[0] not in resultA: resultA[linha[0]] = []
    lista = linha[1].strip()
    lista = lista[1:len(lista)-2].split(",")
    resultA[linha[0]].append((int(lista[0]), lista[1].lstrip("0")))
# print(result)
f.close()
B = linhas[2].strip().split('=')[1]
hasSecond = False
if len(B)>2: hasSecond = True

if hasSecond:
    Bstem = False if "NOSTEMMER" in linhas[2].strip().split('=')[1] else True
    f = open(f"./result/{B}", "r")
    for i in f.readlines():
        linha = i.strip().split(";")
        if linha[0] not in resultB: resultB[linha[0]] = []
        lista = linha[1].strip()
        lista = lista[1:len(lista)-2].split(",")
        resultB[linha[0]].append((int(lista[0]), lista[1].lstrip("0")))
    # print(result)
    f.close()

def precisao(expectativa, resultado):
    precisa = {}
    # print(resultado)
    for i in resultado:
        for j in resultado[i]:
            if j[1] in expectativa[i]:
                if i not in precisa: precisa[i] = 0
                precisa[i]+=1
        if i in precisa:
            precisa[i]=precisa[i]/len(resultado[i])
#     print(f"precisa = {precisa}")
    return precisa

def recall(expectativa, resultado):
    recal = {}
    for i in resultado:
        for j in resultado[i]:
            # print(j)
            # print(expectativa[i])
            if j[1] in expectativa[i]:
                if i not in recal: recal[i] = 0
                recal[i]+=1
        if i in recal:
            recal[i]=recal[i]/len(expectativa[i])
    # print(f"recal = {recal}")
    return recal

def precisao(expectativa, resultado, primeiros = 500):
    precisa = {}
    # print(resultado)
    for i in resultado:
        for j in resultado[i][:primeiros]:
            if j[1] in expectativa[i]:
                if i not in precisa: precisa[i] = 0
                precisa[i]+=1
        if i in precisa:
            precisa[i]=precisa[i]/primeiros
#     print(f"precisa = {precisa}")
    return precisa

def recall(expectativa, resultado, primeiros = 500):
    recal = {}
    for i in resultado:
        for j in resultado[i][:primeiros]:
            # print(j)
            # print(expectativa[i])
            if j[1] in expectativa[i]:
                if i not in recal: recal[i] = 0
                recal[i]+=1
        if i in recal:
            recal[i]=recal[i]/primeiros
    # print(f"recal = {recal}")
    return recal

def f1(precisao, recall):
#     print(f"recall = {recall.values()}")
    P = sum(precisao.values())/len(precisao)
    R = sum(recall.values())/len(recall)
    return (2*P*R)/(P+R)

SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} F1 = {f1(precisao(expec, resultA), recall(expec, resultA))}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} F1 = {f1(precisao(expec, resultA), recall(expec, resultA))}")
if hasSecond:
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} F1 = {f1(precisao(expec, resultB), recall(expec, resultB))}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} F1 = {f1(precisao(expec, resultB), recall(expec, resultB))}")


def averagePrecision(expectativa, resultado):
    aprecisa = {}
    arecall = {}
    aprecisarel = {}
    for i in resultado:
        posicao = 0
        if i not in aprecisa: aprecisa[i] = {}
        if i not in arecall: arecall[i] = {}
        if i not in aprecisarel: aprecisarel[i] = {}
        for j in resultado[i]:
            if j[1] in expectativa[i]:
                posicao+=1
                aprecisarel[i][j[1]] = posicao/j[0]
            aprecisa[i][j[1]]=posicao/j[0]
            arecall[i][j[1]]=posicao/len(expectativa[i])
    return (aprecisa, arecall, aprecisarel)


def calc_map(aprecisarel,expec):
    mq = {}
    for a in aprecisarel:
        mq[a] = sum(aprecisarel[a].values())/len(expec[a])
    MAP = sum(mq.values())/len(mq)
    # print(MAP)
    return mq, MAP


aprecisa, arecall, aprecisarel = averagePrecision(expec, resultA)
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} MAP = {calc_map(aprecisarel,expec)[1]}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} MAP = {calc_map(aprecisarel,expec)[1]}")
if hasSecond:
    aprecisa, arecall, aprecisarel = averagePrecision(expec, resultB)
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} MAP = {calc_map(aprecisarel,expec)[1]}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} MAP = {calc_map(aprecisarel,expec)[1]}")


def calc_mrr(expectativa, resultado):
    mrq = {}
    for i in resultado:
        for j in resultado[i]:
            if j[1] in expectativa[i]:
                mrq[i]=1/j[0]
                break
    # print(mrq)
    MRR = sum(mrq.values())/len(mrq)
    # print(MRR)
    return mrq, MRR

print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} MRR = {calc_mrr(expec, resultA)[1]}")
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} MRR = {calc_mrr(expec, resultA)[1]}\n\n"
if hasSecond:
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} MRR = {calc_mrr(expec, resultB)[1]}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} MRR = {calc_mrr(expec, resultB)[1]}")

def calc_precisionK(expectativa, resultado, k):
    precisaok = {}
    for i in resultado:
        relevantes = 0
        for j in resultado[i][:k]:
            if j[1] in expectativa[i]:
                # print(f"j[0] = {j[0]} - j[1] = {j[1]}")
                relevantes+=1
        precisaok[i] = relevantes/k
    # print(precisaok)
    return precisaok

com = calc_precisionK(expec, resultA, 5)
mcom = sum(com.values())/len(com)
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@5 = {mcom}")
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@5 = {mcom}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@5 = {com}")
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@5 = {com}\n\n"
if hasSecond:
    sem = calc_precisionK(expec, resultB, 5)
    msem = sum(sem.values())/len(sem)
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@5 = {msem}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@5 = {msem}")
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@5 = {sem}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@5 = {sem}")

com = calc_precisionK(expec, resultA, 10)
mcom = sum(com.values())/len(com)
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@10 = {mcom}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@10 = {mcom}")
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@10 = {com}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} P@10 = {com}")
if hasSecond:
    sem = calc_precisionK(expec, resultB, 10)
    msem = sum(sem.values())/len(sem)
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@10 = {msem}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@10 = {msem}")
    SAIDA += f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@10 = {sem}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} P@10 = {sem}")

def g11ppr(aprecisa, arecall):
    pre = {}
    g11 = []
    for r in arecall:
        i = 1
        recAtual = list(arecall[r].values())
        preAtual = list(aprecisa[r].values())
        pre[r] = [max(preAtual)]
        for j in recAtual:
            if j >= i/10:
                indice = recAtual.index(j)
                pre[r].append(max(preAtual[indice:]))
                i+=1
    # print(pre)
    for i in range(0, 11):
        total = 0
        for j in pre:
            total += pre[j][i]
        g11.append(total/len(pre))
    return g11

aprecisa, arecall, aprecisarel = averagePrecision(expec, resultA)
g11 = g11ppr(aprecisa, arecall)
plt.figure(0)
plt.plot([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g11, color="red", linewidth = 3, marker='o', markerfacecolor='red', markersize=12)
plt.savefig(f"./avalia/11pontos-{'stemmer' if Astem else 'nostemmer'}-2.png")
plt.savefig(f"./avalia/11pontos-{'stemmer' if Astem else 'nostemmer'}-2.pdf")
csv = {}
for z in zip([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g11):
    csv[z[0]] = [z[1]]
pd.DataFrame(csv).to_csv(f"./avalia/11pontos-{'stemmer' if Astem else 'nostemmer'}-1.csv")

if hasSecond:
    aprecisa, arecall, aprecisarel = averagePrecision(expec, resultB)
    g111 = g11ppr(aprecisa, arecall)
    plt.figure(1)
    plt.plot([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g111, color="blue", linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
    plt.savefig('./avalia/11pontos-nostemmer-1.png')
    plt.savefig('./avalia/11pontos-nostemmer-1.pdf')
    csv = {}
    for z in zip([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g111):
        csv[z[0]] = [z[1]]
    pd.DataFrame(csv).to_csv (f"./avalia/11pontos-{'stemmer' if Bstem else 'nostemmer'}-2.csv")
    plt.figure(2)
    plt.plot([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g111, linewidth = 3, marker='o', markerfacecolor='blue', color="blue",  markersize=12)
    plt.plot([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], g11, linewidth = 3, marker='o', markerfacecolor='red', color="red", markersize=12)
    plt.savefig('./avalia/11pontos-B_A-1.png')

def rprecision(expec, result):
    rpre = {}
    for r in result:
        lim = len(expec[r])
        if r not in rpre: rpre[r] = 0
        for i in range(0,lim):
            if result[r][i][1] in expec[r]:
                rpre[r]+=1
        rpre[r]=rpre[r]/lim
    return rpre
def histRprec(expec, resultA, resultB):
    hist = {}
    rpressB = rprecision(expec, resultB)
    rprecsA = rprecision(expec, resultA)
    listadeq = []
    for a in rprecsA:
        listadeq.append(int(a))
        hist[a] = rprecsA[a] - rpressB[a]
    return rprecsA, hist

if hasSecond:
    rprecsA, hist = histRprec(expec, resultA, resultB)
    plt.figure(figsize = (130, 47))
    plt.bar([r.lstrip("0") for r in rprecsA.keys()], list(hist.values()), width = 1)
    plt.yticks(fontsize=44)
    plt.xticks(fontsize=40)
    plt.grid()
    plt.savefig('./avalia/R_Precision-A-B-1.png')
    csv = {}
    for z in zip(list(rprecsA.keys()), list(hist.values())):
        csv[z[0]] = [z[1]]
    pd.DataFrame(csv).to_csv(r'./avalia/R_Precision-A-B-1.csv')

def dcg(expecR, result, tamlist = 10):
    dcg = {}
    cg = {}
    for r in result:
        if r not in dcg: dcg[r] = []
        if r not in cg: cg[r] = []
        for i, j in enumerate(result[r]):
            if j[1] in expecR[r]:
                if not i:
                    cg[r].append(expecR[r][j[1]])
                    dcg[r].append(expecR[r][j[1]])
                    continue
                cg[r].append(cg[r][len(cg[r])-1]+expecR[r][j[1]])
                dcg[r].append(dcg[r][len(dcg[r])-1]+expecR[r][j[1]]/log(i+1))
            else:
                if not i:
                    dcg[r].append(0)
                    cg[r].append(0)
                    continue
                cg[r].append(cg[r][len(cg[r])-1])
                dcg[r].append(dcg[r][len(dcg[r])-1])
    dcgm = {}
    cgm = {}
    for i in range(1,tamlist+1):
        dcgm[i] = 0
        cgm[i] = 0
        for j in dcg:
            cgm[i] += cg[j][i]
            dcgm[i] += dcg[j][i]
        dcgm[i] = dcgm[i]/tamlist
        cgm[i] = cgm[i]/tamlist
    return dcg, dcgm, cgm

csdcg, dcgm, cgm = dcg(expecRel, resultA)
plt.figure(figsize = (20, 7))
plt.plot(cgm.keys(), cgm.values(), linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
plt.plot(dcgm.keys(), dcgm.values(), linewidth = 3, marker='s', markerfacecolor='red', markersize=12)
plt.legend(['cg','dcg'])
plt.grid()
plt.savefig(f"./avalia/dcg-{'STEMMER' if Astem else 'NOSTEMMER'}-1.png")
pd.DataFrame(cgm, index=[0]).to_csv(f"./avalia/cg-{'stemmer' if Astem else 'nostemmer'}-1.csv")
pd.DataFrame(dcgm, index=[0]).to_csv(f"./avalia/dcg-{'stemmer' if Astem else 'nostemmer'}-1.csv")

if hasSecond:
    ssdcg, dcgm, cgm = dcg(expecRel, resultB)
    plt.figure(figsize = (20, 7))
    plt.plot(cgm.keys(), cgm.values(), linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dcgm.keys(), dcgm.values(), linewidth = 3, marker='s', markerfacecolor='red', markersize=12)
    plt.legend(['cg','dcg'])
    plt.grid()
    plt.savefig(f"./avalia/dcg-{'STEMMER' if Bstem else 'NOSTEMMER'}-2.png")
    pd.DataFrame(cgm, index=[0]).to_csv(f"./avalia/cg-{'stemmer' if Bstem else 'nostemmer'}-2.csv")
    pd.DataFrame(dcgm, index=[0]).to_csv(f"./avalia/dcg-{'stemmer' if Bstem else 'nostemmer'}-2.csv")

def ndcg(expecRel, dcg, limite = 10):
    nndcg = {}
    for e in expecRel:
        expecRel[e]=dict(sorted(expecRel[e].items(),key= lambda x:x[1], reverse=True))
    for e in expecRel:
        idcg = 0
        for i, j in enumerate(expecRel[e]):
            if i == limite: break
            if not i:
                idcg = expecRel[e][j]
                continue
            idcg += expecRel[e][j]/log(i+1)
        nndcg[e] = dcg[e][i-1 if i == limite else i]/idcg
#     print(nndcg)
    return nndcg

csdcg = ndcg(expecRel, csdcg)
pd.DataFrame(csdcg, index=[0]).to_csv(f"./avalia/ndcg-{'stemmer' if Astem else 'nostemmer'}-1.csv")
SAIDA += f"A {'STEMMER' if Astem else 'NOSTEMMER'} NDCG max = {max(csdcg.values())}\n\n"
print(f"A {'STEMMER' if Astem else 'NOSTEMMER'} NDCG max = {max(csdcg.values())}")

if hasSecond:
    ssdcg = ndcg(expecRel, ssdcg)
    pd.DataFrame(ssdcg, index=[0]).to_csv(f"./avalia/ndcg-{'stemmer' if Astem else 'nostemmer'}-2.csv")
    SAIDA +=f"B {'STEMMER' if Bstem else 'NOSTEMMER'} NDCG max = {max(ssdcg.values())}\n\n"
    print(f"B {'STEMMER' if Bstem else 'NOSTEMMER'} NDCG max = {max(ssdcg.values())}")

    plt.figure(figsize = (200, 87))
    plt.bar([i.lstrip("0") for i in ssdcg.keys()], list(ssdcg.values()), width = .5)
    plt.bar([int(i.lstrip("0"))+0.5 for i in csdcg.keys()], list(csdcg.values()), width = .5)
    plt.legend(['STEMMER' if Bstem else 'NOSTEMMER','STEMMER' if Astem else 'NOSTEMMER'], prop={'size': 60})
    plt.yticks(fontsize=44)
    plt.xticks(fontsize=34)
    plt.grid()
    plt.savefig(f"./avalia/ndcg-B-A-1.png")


f = open("./avalia/saida.txt", "w")
f.write(SAIDA)
f.close()