# -*- coding: utf-8 -*-

import os
import re

expressões_para_excluir = [
    r'^[^a-záéíóúãẽĩõũàèìòùâêîôû]+$',
    r'^[^a-záéíóúãẽĩõũàèìòùâêîôû]+?\s?[:]',
]

def processa(texto):
    texto = texto.splitlines()
    novo_texto = list()
    for linha in texto:
        if linha.strip() == '':
            novo_texto.append('')
        else:
            printar = True
            for expressão in expressões_para_excluir:
                if re.search(expressão, linha):
                    printar = False
            if printar: novo_texto.append(linha)

    return "\n".join(novo_texto)


def main():
    pasta = input('Escolha a pasta onde está o corpus:\n').replace('"','')
    while pasta.strip() == '':
        pasta = input('Escolha a pasta onde está o corpus:\n').replace('"','')
    if pasta == 'exit': exit()

    arquivos = [x for x in os.listdir(pasta) if os.path.isfile(pasta + '/' + x)]

    for i, arquivo in enumerate(arquivos):
        print('(' + str(i+1) + '/' + str(len(arquivos)) + ') ' + arquivo)
        novo_arquivo = processa(open(pasta + '/' + arquivo, 'r').read())
        open(pasta + '/' + arquivo, 'w').write(novo_arquivo)

main()
