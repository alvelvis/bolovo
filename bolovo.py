# -*- coding: utf-8 -*-

from datetime import date
import requests
import re
import random
import os
import sys

#Tenta importar o módulo Nltk
try:
	import nltk
except:
	from pip import main as pipmain
	pipmain(['install','nltk'])
	print('1/3 Nltk instalado com sucesso!')
	exit()

#Tenta importar o módulo Newspaper (que extrai os artigos)
try:
	from newspaper import Article
except:
	from pip import main as pipmain
	pipmain(['install','newspaper3k'])
	import nltk
	nltk.download('punkt')
	print('2/3 Newspaper3k instalado com sucesso!')
	exit()

#Tenta importar o módulo BeautifulSoup (que extrai os links)
try:
	from bs4 import BeautifulSoup
except:
	from pip import main as pipmain
	pipmain(['install','bs4'])
	print('3/3 BeautifulSoup instalado com sucesso!')
	exit()

#Tenta importar o módulo git (que atualiza o bolovo)
def atualizar():
	try:
		from git import Git
	except:
		from pip import main as pipmain
		pipmain(['install','GitPython'])
		print('GitPython instalado com sucesso!')
		exit()
	finally:
	    if os.path.isdir('.git'):
		    Git().pull()
	    else:
		    Git().init()
		    Git().remote('add','origin','https://github.com/alvelvis/bolovo.git')
		    Git().fetch()
		    if os.path.isfile('bolovo.py'): os.remove('bolovo.py')
		    if os.path.isfile('renomear.py'): os.remove('renomear.py')
		    if os.path.isfile('README.md'): os.remove('README.md')
		    Git().checkout('master')

if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
    atualizar()
    print('Atualizado com sucesso!')
    exit()

#Cria as listas de links "já vistos": aqueles que já foram baixados e não devem ser baixados novamente
seen = set()
repetidos = 0
maxrepetition = 10
linksvistos = list()

#Extrai os artigos dos links que já foram guardados em um "txt"
def extract_articles():

	#Tira os caracteres especiais dos nomes dos arquivos
	def slugify(value):
		return "".join(x if x.isalnum() else "_" for x in value)

	def inserir_url(url):

		#Checa se o link já não foi visto
		global linksvistos
		if (not url in seen) and (not url in linksvistos):
			#Tenta baixar o artigo. Se não conseguir, retorna falsos
			try:
				article = Article(url,'pt-br')
			except Exception as e:
				print('Erro em "'+url+'": '+str(e))
				if 'Not Found' in str(e): return True
				else: return False
			else:
				try:
					article.download()
				except Exception as e:
					print('Erro em "'+url+'": '+str(e))
					if 'Not Found' in str(e): return True
					else: return False
				else:
					try:
						article.parse()
					except Exception as e:
						print('Erro em "'+url+'": '+str(e))
						if 'Not Found' in str(e): return True
						else: return False
					else:
						try:
							article.nlp()
						except Exception as e:
							print('Erro em "'+url+'": '+str(e))
							if 'Not Found' in str(e): return True
							else: return False
						else:
							if True:
								#Adiciona o cabeçalho dos arquivos de texto
								texto = ("#-Corpus: " + corpus
									+ "\n" + "#-Data de publicação: " + str(article.publish_date)
									+ "\n" + "#-Data de adição ao corpus: " + datahoje
									+ "\n" + "#-Fonte: " + url
									+ "\n" + "#-Observações: " + obs
									+ "\n" + "#-Título: " + article.title
									+ "\n" + "#-Autores: " + str(article.authors)
									+ "\n\n" + article.text
									)
								#Salva o arquivo de texto
								if not os.path.exists(corpus): os.mkdir(corpus)
								arq = open(corpus+"/"+slugify(article.title)+".txt","w",encoding="utf-8")
								arq.write(texto)
								arq.close()
								seen.add(url)
							if os.path.isfile("seen"+corpus+".txt"):
								arq = open("seen"+corpus+".txt","r")
								linksvistos = arq.read()
								linksvistos = linksvistos.splitlines()
								arq.close()
							links2 = "\n".join(linksvistos)
							novoslinks = "\n".join(seen)
							arq = open("seen"+corpus+".txt","w")
							arq.write(links2+"\n"+url)
							arq.close()
							print('('+str(i+1)+'/'+str(len(links))+') "' + article.title+'"')
							#Se deu tudo certo, retorna True
							return True

		#Se o arquivo já foi baixado, retorna True mas avisa que já foi baixado
		else:
			print('('+str(i+1)+'/'+str(len(links))+') JÁ EXTRAÍDO: "' + url +'"')
			return True

	#Após guardar os links, começa a extrair os artigos
	print("")
	print("Aguarde...")

	datahoje = str(date.today())

	#Arquivo de links já baixados
	seen = set()
	if os.path.isfile("seen"+corpus+".txt"):
		arq = open("seen"+corpus+".txt","r")
		linksvistos = arq.read()
		linksvistos = linksvistos.splitlines()
		arq.close()

	#Arquivo de links a serem baixados
	arq = open("links"+corpus+".txt","r")
	links = arq.read()
	arq.close()
	links = links.splitlines()
	linkscopy = links.copy()

	#Para cada link, um novo "inserir_url()"
	for i,link in enumerate(links):
		if link != "":
			#Apenas se não conseguir baixar a matéria (inserir_url() == False) que ele mantém o link na lista de links
			if inserir_url(link):
				linkscopy[i] = ""
				novolinks = str()
				for linha in linkscopy:
					if linha != "":
						novolinks = novolinks + linha + "\n"

				arq = open("links"+corpus+".txt","w")
				arq.write(novolinks)
				arq.close()

#Pede o nome do corpus e dá a lista de opções disponíveis
corpus = ""
while corpus.strip() == "":
	print("Insira o nome do Corpus (é necessário ter 'oglobo|extra|g1' no final):")
	corpus = input()
if corpus == 'exit': exit()
print("")
#Pede alguma observação (opcional)
print("Alguma observação? (deixe em branco caso não)")
obs = input()
if obs == 'exit': exit()

#Função que retira os links de uma página específica
#Os comentários são de uma página de ajuda
def Vai(url):
	global repetidos
	global seen
	# Getting the webpage, creating a Response object.
	print(">>>> PESQUISA: '"+url+"'")
	try:
		response = requests.get(url)
	except:
		Vai(url)
	else:
		# Extracting the source code of the page.
		data = response.text

		# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
		soup = BeautifulSoup(data, 'lxml')

		# Extracting all the <a> tags into a list.
		tags = soup.find_all('a')

		# Extracting URLs from the attribute href in the <a> tags.
		links = str()

		#Cria o arquivo de links já vistos
		if os.path.exists('seen'+corpus+'.txt'):
			arq = open('seen'+corpus+'.txt')
			aaaa = arq.read()
			aaaa = aaaa.splitlines()
			arq.close()
		else: aaaa = list()

		#Cria o arquivo de links a serem baixados
		if os.path.exists('links'+corpus+'.txt'):
			arq = open('links'+corpus+'.txt')
			bbbb = arq.read()
			bbbb = bbbb.splitlines()
			arq.close()
		else: bbbb = list()

		#Para cada link, verifica se ele é realmente de uma matéria a ser baixada ou se é lixo
		for tag in tags:
			if ((tag.get('href')!=None)
				and ('' in corpus)
				and (not 'whatsapp://' in tag.get('href'))
				and (not 'whatsapp.com' in tag.get('href'))
				and (not 'facebook.com' in tag.get('href'))
				and (not 'twitter.com' in tag.get('href'))
				and (not 'pinterest' in tag.get('href'))
				and (re.search(expression, tag.get('href')) != None)
				and (not tag.get('href').split('u=')[1].split('&t')[0].split('&k')[0].replace('%2F','/').replace('%3A',':') in seen)
				and (not tag.get('href').split('u=')[1].split('&t')[0].split('&k')[0].replace('%2F','/').replace('%3A',':') in aaaa)
				and (not tag.get('href').split('u=')[1].split('&t')[0].split('&k')[0].replace('%2F','/').replace('%3A',':') in bbbb)
				and (not '/redacao.ghtml' in tag.get('href'))
				and (not 'share' in tag.get('href'))
				and (not 'like' in tag.get('href'))
				and (not 'globoplay' in tag.get('href'))
				and (not 'comment' in tag.get('href'))
				and (not 'siga-a-globonews' in tag.get('href'))
				and (not 'reply' in tag.get('href'))
				and (not '#print' in tag.get('href'))
				and (not "videos-" in tag.get('href'))
				):
				#Caso não seja lixo, adicionar à lista de links
				link_http = tag.get('href').split('u=')[1].split('&t')[0].split('&k')[0].replace('%2F','/').replace('%3A',':') #
				seen.add(link_http)
				links = links + link_http + "\n"
				print("NOVIDADE: " + link_http)

		#Carrega a lista de links
		if os.path.isfile("links"+corpus+".txt"):
			arq = open("links"+corpus+".txt","r")
			oldlinks = arq.read()
			arq.close()
		else: oldlinks = str()

		#Adiciona link à lista de links
		arq = open ("links"+corpus+".txt","w")
		arq.write(oldlinks+links)
		arq.close()
		return len(links.splitlines())


#Função para criar os 50 links da página de busca dos jornais
def termo():
	termo = input('\nTermo de busca:\n')
	while termo == '':
		termo = input('\nTermo de busca:\n')
	if termo == 'exit': exit()
	termobusca = str()
	for palavra in termo.split():
		termobusca = termobusca + palavra + '+'

	_search = list()

	if 'oglobo' in corpus:
		for i in range (49):
			_search.append('http://oglobo.globo.com/busca/?q='+termobusca+'&page='+str(i+1)+'&species=not%C3%ADcias')

		with open('oglobo_search.txt','w') as arq:
			arq.write("\n".join(_search))

	if 'g1' in corpus:
		for i in range (49):
			_search.append('https://g1.globo.com/busca/?q='+termobusca+'&page='+str(i+1))

		with open('g1_search.txt','w') as arq:
			arq.write("\n".join(_search))

	if 'extra' in corpus:
		for i in range (49):
			_search.append('http://extra.globo.com/busca/?q='+termobusca+'&page='+str(i+1)+'&species=not%C3%ADcias')

		with open('extra_search.txt','w') as arq:
			arq.write("\n".join(_search))

	busca()


#Salva os links de matérias nessas 50 páginas de busca dos jornais
def busca():
	global repetidos
	global maxrepet
	global obs
	repetidos = 0
	while repetidos <= maxrepet:
		if "oglobo" in corpus:
			arq = open('oglobo_search.txt',"r")
		if "g1" in corpus:
			arq = open('g1_search.txt',"r")
		if "extra" in corpus:
			arq = open('extra_search.txt','r')
		linksrecursivos = arq.read()
		arq.close()
		linksrecursivos = linksrecursivos.splitlines()
		maxrepet = maxrepetition + len(linksrecursivos)
		if len(linksrecursivos) > 0:
			i = random.randint(0,len(linksrecursivos)-1)
			while (linksrecursivos[i] in seen2) and (repetidos <= maxrepet):
				i = random.randint(0,len(linksrecursivos)-1)
				repetidos += 1
			url = linksrecursivos[i]
			seen2.add(linksrecursivos[i])
			if Vai(url) == 0:
				repetidos += 1
				print(">>>> PROCURANDO ("+str(repetidos)+"/"+str(maxrepet)+")")
		else:
			print('Nenhuma novidade na página :(')
			if 'oglobo' in corpus:
				obs = obs + '; Tipo: Notícias; '
			if 'extra' in corpus:
				obs = obs + '; Tipo: Notícias; '
			extract_articles()
			termo()

	#Baixa as páginas e depois volta para escolher um novo termo de busca
	extract_articles()
	termo()

#Repetições
seen2 = set()
maxrepet = maxrepetition

#Todo link da página de busca deve ter a expressão:
if 'oglobo' in corpus: expression = 'u='
elif 'extra' in corpus: expression = 'u='
elif 'g1' in corpus: expression = 'u='
else: exit()

#Efetivamente, pede os termos de busca
termo()
