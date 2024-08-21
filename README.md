
# Steam Screenshot Exporter

#### Aluno: [Murillo Dario Gomes Carvalho](https://github.com/Murillodgc)
#### Orientador: [Felipe Borges](https://github.com/FelipeBorgesC)

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [screenshot_exporter.py](https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/screenshot_exporter.py).
- [ss exporter.rar](https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/ss%20exporter.rar).

---

### Resumo


O presente trabalho tem como objetivo o desenvolvimento de uma ferramenta para o download em massa de capturas de tela e artes visuais de produtos disponibilizados na plataforma [Steam](https://store.steampowered.com/). A ferramenta visa otimizar e automatizar um processo anteriormente realizado de forma manual, proporcionando uma significativa economia de tempo e aumentando a eficiência na execução de tarefas como o cadastro de produtos em lojas virtuais de jogos. Esse tipo de atividade, que demanda a inserção de um grande volume de produtos diariamente, tem se beneficiado diretamente da aplicação desenvolvida, resultando em uma redução de 5 a 10 minutos, em média por produto cadastrado. Esse ganho de tempo permite que a equipe direcionada a essa tarefa possa se concentrar em outras demandas operacionais ou até mesmo aumentar a quantidade de cadastros por dia, contribuindo para uma maior produtividade e eficiência no fluxo de trabalho.

### Abstract

The present work aims to develop a tool for mass downloading of screenshots and visual artwork of products available on the [Steam](https://store.steampowered.com/)[Steam](https://store.steampowered.com/) platform. The tool seeks to optimize and automate a process previously carried out manually, providing significant time savings and increasing efficiency in tasks such as product registration in online game stores. This type of activity, which requires the daily insertion of a large volume of products, has directly benefited from the developed application, resulting in a reduction of 5 to 10 minutes on average per product registered. This time saving allows the team responsible for this task to focus on other operational demands or even increase the number of registrations per day, contributing to greater productivity and efficiency in the workflow.

### 1. Introdução

Antes de apresentar a aplicação, é fundamental compreender o problema em questão. Este problema foi identificado no contexto da plataforma [Nuuvem](https://www.nuuvem.com/-/), a maior empresa brasileira no setor de venda de jogos digitais. A [Nuuvem](https://www.nuuvem.com/-/) possui um vasto portfólio de produtos, que inclui títulos de diversas publishers de jogos de todo o mundo. A grande maioria delas exige que um padrão específico seja seguido na apresentação de seus produtos, indicando a página da [Steam](https://store.steampowered.com/)—atualmente a maior plataforma de venda de jogos digitais globalmente—como referência.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/steampage.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

Dessa forma, torna-se necessário replicar grande parte das informações provenientes dessa fonte, incluindo as artes e capturas de tela, que são essenciais para ilustrar a página e proporcionar ao cliente uma visão mais clara do produto que pretende adquirir. No entanto, não existe um padrão definido quanto à quantidade de imagens por página, podendo variar de uma única imagem até mais de 30, em casos mais extremos. O processo de obtenção dessas imagens segue o fluxo manual padrão de salvamento oferecido pelo sistema operacional do usuário, o que pode levar até 30 segundos por captura de tela, variando conforme a velocidade da conexão à internet. Além disso, para as artes de banner, background e capa do produto, é necessário inspecionar o código da página para localizar a versão em alta qualidade, o que demanda ainda mais tempo, aumenta a probabilidade de erros humanos e impõe dificuldades adicionais para pessoas menos familiarizadas com o processo. 

O processo de cadastro de produtos, que atualmente demanda em média 25 minutos por item, limita o número de cadastros que podem ser realizados diariamente. Com um backlog crescente e um grupo de analistas incapaz de acompanhar a velocidade de novas adições à fila, tornou-se evidente a necessidade de otimizar etapas que consomem tempo significativo. Especificamente, o gasto de mais de 5 minutos apenas para salvar imagens representava uma ineficiência crítica. Cada analista cadastra, em média, 5 produtos por dia; assim, automatizar essa tarefa permitiria o cadastro de um produto adicional diariamente. Ao final de uma semana de trabalho, essa mudança equivaleria a um dia extra de produtividade para cada analista, resultando em um aumento de 20% na eficiência do processo. Foi nesse contexto que surgiu a ideia do Screenshot Exporter, uma ferramenta simples, mas eficaz, que reduz o tempo necessário para o salvamento de imagens de 5 minutos para 5 segundos, otimizando significativamente o processo de cadastro.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/ss_exporter.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

### 2. Modelagem

Em síntese, o Screenshot Exporter é uma aplicação desenvolvida a partir de um script em Python, que integra funcionalidades de diversas bibliotecas para automatizar o download e o salvamento local, na máquina do usuário, de todas as artes e capturas de tela necessárias para o cadastro de um produto, ou para outras finalidades. O processo é simplificado através da inserção de uma URL de produto da Steam em uma interface gráfica de fácil utilização. O script foi convertido em um executável utilizando o PyInstaller, visando facilitar sua distribuição e uso em maior escala. A seguir, será feita uma análise detalhada do código, explicando seu funcionamento de forma segmentada para maior clareza e favorecer a didática.

#### Bibliotecas

Iniciaremos a análise discutindo as bibliotecas utilizadas no projeto e a finalidade de cada uma delas.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/libraries.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

os: Permite a manipulação de diretórios e arquivos.
requests: Faz requisições HTTP, como baixar conteúdo de URLs.
re: Utilizado para expressões regulares, permitindo buscas textuais avançadas.
BeautifulSoup de bs4: Faz o parsing de HTML para facilitar a extração de dados ou Webscrapping.
tkinter: Constrói interfaces gráficas.
threading: Lida com threads para execução simultânea, dando mais agilidade ao processo.
webbrowser: Abre URLs no navegador.
concurrent.futures: Facilita a execução de funções em paralelo usando threads.

#### Diretório de Salvamento

Agora, seguiremos com a explicação de algumas das funções principais e da lógica do script. O código está devidamente comentado por etapas, proporcionando uma visão geral das operações de cada bloco até o resultado final. Iniciaremos pela função open_directory(). Essa função é responsável por abrir o diretório local onde as imagens baixadas são armazenadas, conforme especificado na variável save_folder, quando um clique é detectado no link presente no log de texto da interface gráfica da aplicação. Essa funcionalidade foi adicionada posteriormente como uma melhoria de qualidade de vida para o usuário.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco1.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>
<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco1_2.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

#### Donwload de Imagens

Este bloco de código refere-se à função download_images(), que desempenha o papel central no início do processo de download das imagens. Podemos dividi-lo em duas partes principais:

A primeira parte está relacionada à função download_image(img_url, save_folder, log_text, subfolder_name). Essa função é responsável por fazer o download de uma única imagem. Os passos envolvidos nessa etapa incluem:

Limpeza do nome do arquivo: Usa expressões regulares para remover caracteres inválidos no nome do arquivo para uso futuro em criação de pastas.
Download da imagem: Baixa a imagem da URL e a salva no diretório save_folder.
Log: Atualiza o log_text com uma mensagem sobre o sucesso ou falha do download.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco2.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

A segunda parte refere-se à função download_images(). Esta é a função principal responsável por iniciar o processo de download em segundo plano. Os passos envolvidos nessa etapa incluem:

Verificação da URL: Se a URL estiver vazia, mostra um erro.
Extração do APPID: Usa expressões regulares para extrair o APPID da URL do Steam, que é necessário para gerar URLs adicionais de imagens.
Download da página: Faz o download do HTML da página do jogo para extrair o nome do jogo e possíveis URLs de imagens.
Criação do diretório de salvamento: Cria um diretório baseado no nome do jogo para salvar as imagens.
Log de início: Atualiza o log com mensagens iniciais.
Busca de imagens: Encontra URLs de imagens específicas (1920x1080) e adiciona URLs extras geradas com base no APPID.
Thread para download: Inicia um thread que usa ThreadPoolExecutor para baixar as imagens em paralelo, diminuindo o tempo de execução do script.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco2.2.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

#### Criação da Interface Gráfica

O terceiro bloco de código refere-se à criação da interface gráfica da aplicação, ou GUI (Graphical User Interface), desenvolvida utilizando a biblioteca tkinter. Essa interface permite ao usuário interagir de forma intuitiva com o script, inserindo a URL do jogo e monitorando o progresso do download por meio de um log de mensagens. A interface também inclui funcionalidades adicionais, como um botão para iniciar o processo de download e um link que permite abrir o diretório onde as imagens foram armazenadas.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco3.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

#### Execução do Script

O último bloco de código refere-se à execução do programa, onde a interface gráfica é mantida ativa por meio do comando window.mainloop(), permitindo que o sistema permaneça em operação enquanto aguarda interações do usuário.

<img src="https://github.com/Murillodgc/Steam_Screenshot_Exporter/blob/main/images/bloco4.jpg" alt="mediana_nivel" style="height: 300px; width:700px;"/>

### 3. Conclusões

O script apresentado é um exemplo sólido de como a linguagem Python, em conjunto com bibliotecas poderosas como requests, BeautifulSoup e tkinter, pode ser utilizada para automatizar tarefas complexas, como o download de múltiplas imagens a partir de uma página web. Através da combinação de técnicas de web scraping, processamento paralelo e uma interface gráfica intuitiva, o script oferece uma solução eficiente para usuários que precisam coletar imagens de jogos da plataforma Steam. No caso específico para o qual foi desenvolvido, a ferramenta aumentou a produtividade dos analistas em aproximadamente 20%. Embora existam diversos aspectos do processo que ainda podem ser aprimorados seguindo a mesma lógica, toda jornada começa com o primeiro passo, e essa aplicação representou exatamente isso. Assim, este trabalho evidencia a versatilidade do Python na criação de ferramentas de automação, podendo servir como base para a implementação de sistemas mais complexos que necessitem de coleta e processamento automatizado de dados, seja na [Nuuvem](https://www.nuuvem.com/-/), em outras empresas, ou em projetos autônomos.
---

Matrícula: 221.100.812

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
