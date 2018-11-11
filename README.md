# Salvar matérias de jornais em arquivos de texto

**bolovo** salva matérias de Jornais em arquivos de texto. Além do corpo do texto, alguns metadados também são acrescidos ao arquivo. O robô busca por links de matérias a partir de termos de busca escolhidos pelo usuário. Ele, então, navega por 50 páginas de busca utilizando o termo de busca e salva os links para, posteriormente, baixar os artigos correspondentes.

**bolovo**, diferente de outros robôs, é inteligente e procura por novas versões automaticamente.

* [Jornais suportados](#Jornais-suportados)
* [Metadados](#Metadados)
* [Como usar](#Como-usar)

# Jornais suportados

Atualmente, é possível salvar matérias dos jornais:

* [O Globo](http://oglobo.globo.com/busca/?q=bolovo)
* [G1](https://g1.globo.com/busca/?q=bolovo)
* [Extra](http://extra.globo.com/busca/?q=bolovo)

Novos veículos devem ser adicionados em um futuro próximo.

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

	>> bolovo.py

**bolovo** baixará os módulos *newspaper3k*, *bs4* e *GitPython* automaticamente na primeira inicialização.

Alguns comandos serão requisitados ao usuário:

* Insira o nome do corpus: a pasta onde os artigos serão salvos será criada automaticamente.
* Alguma observação? Por exemplo: "busca pelos termos 'x e y'"
* Insira os termos de busca: note que termos diferentes podem dar resultados diferentes.
* Aguarde...
* Ao término, será requisitado outro termo de busca. As pesquisas com esse novo termo serão salvas com os mesmos metadados.