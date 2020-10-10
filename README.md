<link rel="stylesheet" href="https://gist.githubusercontent.com/EthicalMeikin/c4d7bf093ba6ef5710924adf80009dba/raw/b07036c7e122fa8e14541d2ed8da3eb1774a3d1c/index.css">

<center>
  <img src="https://image.prntscr.com/image/_buFoHQMQ2S6TmMWrYi_zw.png"/>
</center>

![](https://img.shields.io/badge/grecaptchabypass-v2.0.2b0-dodgerblue.svg)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-dodgerblue.svg)](https://www.python.org/downloads/)
[![WebDriver Geckodriver](https://img.shields.io/badge/WebDriver-GeckoDriver-dodgerblue.svg)](https://github.com/mozilla/geckodriver/releases)
[![Apoia-se](https://img.shields.io/badge/Apoie-apoia.se-dodgerblue.svg)](https://apoia.se/grecaptchabypass)
![Português - Brasil](https://img.shields.io/badge/Português-BR-dodgerblue.svg)
[![License](https://img.shields.io/badge/License-GPL-%235d5d5d.svg)](https://github.com/EthicalMeikin/grecaptchabypass/blob/master/LICENSE.md)

Programa feito com **_Selenium + Speech-to-text_** e com o propósito de
realizar quebras de _Google reCAPTCHAs_, com e sem desafios visuais, sem uso de
proxy e com simulação de interação humana com a página.

**_Projeto escrito e criado para os demais fins estudantis e
para colaboração em comunidades éticas com o fiel propósito de realizar uma
determinada tarefa ou serviço ético e totalmente racional sem intervenção
fraudulenta._**

_Projeto mantido por financiamento coletivo, quer ser um apoiador?
[Apoie](https://apoia.se/grecaptchabypass) :)_

## Sumário
  * [Início: Saiba informações sobre a biblioteca](https://grecaptchabypass.readthedocs.io/)
    - [O que esta nova versão tem à oferecer?](https://grecaptchabypass.readthedocs.io/#o-que-esta-nova-versao-tem-a-oferecer)
    - [Observações e Avisos Legais](https://grecaptchabypass.readthedocs.io/#observacoes-e-avisos-legais)
    - [Recomendações](https://grecaptchabypass.readthedocs.io/#recomendacoes)<br/><br/>
  * [Introdução e Instalação: Formas de instalação da biblioteca.](https://grecaptchabypass.readthedocs.io/introduction-and-installation)
    - [Instalação via Python Package Index (PIP)](https://grecaptchabypass.readthedocs.io/introduction-and-installation/#instalacao-via-python-package-index-pip)
    - [Instalação via GIT](https://grecaptchabypass.readthedocs.io/introduction-and-installation/#instalacao-via-git)
    - [Primeiros Passos](https://grecaptchabypass.readthedocs.io/introduction-and-installation/#primeiros-passos)<br/><br/>
  * [Documentação dos Objetos](https://grecaptchabypass.readthedocs.io/objects-documentation)
    - [Obtendo instância do webdriver do Firefox](https://grecaptchabypass.readthedocs.io/objects-documentation/#obtendo-instancia-do-webdriver-do-firefox)
    - [Criando Parser da Nossa Página](https://grecaptchabypass.readthedocs.io/objects-documentation/#criando-parser-da-nossa-pagina)
    - [Manipulador do ReCAPTCHA](https://grecaptchabypass.readthedocs.io/objects-documentation/#manipulador-do-recaptcha)
    - [Estados do ReCAPTCHA](https://grecaptchabypass.readthedocs.io/objects-documentation/#estados-do-recaptcha)
    - [Exceções](https://grecaptchabypass.readthedocs.io/objects-documentation/#excecoes)<br/><br/>
  * [Extra: Descubra como funcionam requisições, cookies, sessões e o reCAPTCHA.](https://grecaptchabypass.readthedocs.io/extra)
    - [O que é uma requisição?](https://grecaptchabypass.readthedocs.io/extra/#o-que-e-uma-requisicao)
    - [O que são Cookies e como funcionam?](https://grecaptchabypass.readthedocs.io/extra/#o-que-sao-cookies-e-como-funcionam)
    - [O que são Sessões e como funcionam?](https://grecaptchabypass.readthedocs.io/extra/#o-que-sao-sessoes-e-como-funcionam)
    - [O que é um Google reCAPTCHA e como funciona?](https://grecaptchabypass.readthedocs.io/extra/#o-que-e-um-google-recaptcha-e-como-funciona)
    <br/><br/>

## O que esta nova versão tem à oferecer?

1. **Desempenho e Velocidade**: O código antigo foi refatorado e reescrito.
2. **Precisão**: O reCAPTCHA pode ter mais chances de ser quebrado.
3. **Funcionalidades**: Agora é possível solucionar mais de um reCAPTCHA da
mesma página e outros.<br/><br/>

## Observações e Avisos Legais

* Este projeto se encontrará em constantes mudanças sem aviso prévio e todas as
mudanças de código serão publicadas primeiro no
[repositório](https://github.com/EthicalMeikin/grecaptchabypass) antes de
serem publicadas no [PyPi](https://pypi.com/project/grecaptchabypass).<br/><br/>

* Não é recomendada a utilização de Proxies com *Certificado SSL/TLS* inseguro,
infelizmente a Google possui uma política de segurança chamada
*HTTP Strict Transport Security (HSTS)* que impede a conexão de certificados
inseguros no Firefox.<br/><br/>

* Certificar se não há nenhum elemento sobrepondo o reCAPTCHA na página e se a
conexão com a internet está razoável.<br/><br/>

* Não é recomendada a solução de reCAPTCHAs em massa (paralelamente),
isto pode levantar suspeitas de que há uma automação e seu IP será banido de
forma que o desafio por audio não funcione e consequentemente você terá que
resolver manualmente o desafio por imagem para que as suspeitas sejam
retiradas.<br/><br/>

* A quebra do reCAPTCHA com desafios pode durar no mínimo 8 segundos ou menos
dependendo da sua conexão de rede e processador.<br/><br/>

* Conexão muito fraca pode comprometer a quebra do reCAPTCHA e exibir um erro.
<br/><br/>

* A utilização do DevTools faz com que o viewport fique menor, atrapalhando a
simulação do cursor de usuário e consequentemente estourando uma exceção, evite
o uso dessas ferramentas que ocupem o viewport enquanto a quebra do reCAPTCHA
estiver em andamento.<br/><br/>


## Recomendações
[**Eduardo Mendes**](http://youtube.com/c/eduardomendes) é um canal mega didático
com diversos assuntos pythônicos em geral e mantido por financiamento
coletivo.

Você também pode participar e ser um [apoiador](https://apoia.se/livedepython)
para incentivar o autor do canal à continuar disponibilizando vídeos bem
produzidos e com mais assuntos interessantes.

**Siga algumas playlists no YouTube:**

 - [**Curso de Selenium**](http://encurtador.com.br/hEHY9): _Aprenda à utilizar
 mais que o básico do Selenium no Python._
 - [**Live de Python**](http://encurtador.com.br/cpIU3): _Aprenda diversos assuntos
 definidos por sugestões dos espectadores._


## Introdução & Instalação

Para realizar a instalação via PyPi, apenas digite esta única linha de comando:
`pip install grecaptchabypass`.

Veja a documentação completa.

[<img src="https://bestbooks.thelargelibrary.com/BUTTON/BUTTON4.png" width="100">](https://grecaptchabypass.readthedocs.io/)