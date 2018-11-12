# Salvar matérias de jornais em arquivos de texto

**bolovo** salva matérias de jornais em arquivos de texto.

**bolovo**, diferente de outros robôs, é inteligente e procura por novas versões automaticamente.

* [Metadados](#Metadados)
* [Como usar](#Como-usar)

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

Tendo instalado o *[Python 3+](https://www.python.org/)*, execute o **bolovo**:

	>> python3 bolovo.py

**bolovo** baixará os módulos *newspaper3k*, *bs4* e *GitPython* automaticamente na primeira inicialização.

Alguns comandos serão requisitados ao usuário:

* Insira o nome do corpus: a pasta onde os artigos serão salvos será criada automaticamente.
* Alguma observação? Por exemplo: "busca pelos termos 'x e y'"
* Insira os termos de busca: note que termos diferentes podem dar resultados diferentes.
* Aguarde...
* Ao término, será requisitado outro termo de busca. As pesquisas com esse novo termo serão salvas com os mesmos metadados.
