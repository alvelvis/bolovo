# -*- coding: utf-8 -*-

import os

diretorio = input('Deseja renomear os arquivos de qual pasta?\n').replace('"','')
while not os.path.isdir(diretorio):
	diretorio = input('\nDeseja renomear os arquivos de qual pasta?\n').replace('"','')
if diretorio == 'exit': exit()

novonome = input('\nOs arquivos receberão um nome e uma numeração. Que nome você deseja que os arquivos recebam?\n')
while novonome.strip() == '':
	novonome = input('\nOs arquivos receberão um nome e uma numeração. Que nome você deseja que os arquivos recebam?\n')
if novonome == 'exit': exit()

arquivos = os.listdir(diretorio)

print('\nAguarde...\n')

for i,arquivo in enumerate(arquivos):
	if os.path.isfile(diretorio + '/' + arquivo):
		texto = open(diretorio + '/' + arquivo, 'r').read()
		print('(' + str(i+1) + '/' + str(len(arquivos)) + ') ' + arquivo)
		os.remove(diretorio + '/' + arquivo)
		open(diretorio + '/' + novonome + '-' + str(i+1) + '.txt', 'w').write('#-ID: ' + novonome + '-' + str(i+1) + '\n' + texto)
