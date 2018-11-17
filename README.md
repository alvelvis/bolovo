# Salvar matérias de jornais em arquivos de texto

**bolovo** salva matérias de jornais em arquivos de texto.

**bolovo**, diferente de outros robôs, é inteligente e procura por novas versões ao utilizar o parâmetro *--atualizar* .

* [Metadados](#Metadados)
* [Como usar](#Como-usar)
* [renomear.py](#renomearpy)
* [pós-processamento.py](#pós-processamentopy)

# Metadados

Além dos artigos jornalísticos, o **bolovo** acrescenta alguns metadados:

* Nome do corpus (nome da pasta (escolhido pelo usuário))
* Data de publicação
* Data de adição ao corpus
* Fonte
* Observações (a critério do usuário)
* Título
* Autores

# Como usar

Tendo instalado o *[Python 3+](https://www.python.org/)* e o *python3-pip* , execute o **bolovo**:

	>> python3 bolovo.py

**bolovo** baixará os módulos *nltk*, *newspaper3k* e *bs4* automaticamente na primeira inicialização.

Alguns comandos serão requisitados ao usuário:

* Insira o nome do corpus: a pasta onde os artigos serão salvos será criada automaticamente.
* Alguma observação? Por exemplo: "busca pelos termos 'x e y'"
* Insira os termos de busca: note que termos diferentes podem dar resultados diferentes.
* Aguarde...
* Ao término, será requisitado outro termo de busca. As pesquisas com esse novo termo serão salvas com os mesmos metadados.

# renomear.py

Caso os nomes dos arquivos gerados pelo **bolovo** sejam grandes demais, você pode renomeá-los seguindo uma sigla e uma numeração.

Exemplo:

>FSP-1

>FSP-2

>FSP-3

>FSP-4

>...

# pós-processamento.py

Código para ajustar os arquivos de texto gerados pelo **bolovo** dentro de uma determinada pasta.

As regras de pós-processamento são as seguintes:

1) Excluir as linhas de texto que sigam uma das expressões regulares:

	^[^a-záéíóúãẽĩõũàèìòùâêîôû]+$
	exemplo: AMEAÇA A EX-ESTRATEGISTA

	^[^a-záéíóúãẽĩõũàèìòùâêîôû]+?\s?[:]
	exemplo: LEIA: Geraldo Alckmin garante o maior tempo de televisão
