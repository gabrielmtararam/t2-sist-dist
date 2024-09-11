import random

QTD_PRODUTOS = 5
QTD_PARTES_DIFERENTES = 100
QTD_PARTES_BASICAS = 43

produtos = {}
for i in range(QTD_PRODUTOS):
    nome = f"Pv{i+1}"
    qtd_partes = random.randint(20, 33)
    produtos[nome] = []
    for j in range (qtd_partes):
        id_parte = random.randint(0, 100)
        produtos[nome].append(id_parte)
    for j in range (QTD_PARTES_BASICAS):
        produtos[nome].append(j)

print(produtos)