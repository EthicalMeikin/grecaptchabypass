<link rel="stylesheet" href="https://grecaptchabypass.readthedocs.io/index.css">

<center>
  <img src="https://github.com/EthicalMeikin/grecaptchabypass/raw/master/assets/header.png"/>
</center>

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

1. [Início: Saiba informações sobre a biblioteca](/)<br/>
1.1 [O que esta nova versão tem à oferecer?](/#o-que-esta-nova-versao-tem-a-oferecer)<br/>
1.2 [Observações e Avisos Legais](/#observacoes-e-avisos-legais)<br/>
1.3 [Recomendações](/#recomendacoes)<br/>
1.4 [Agradecimentos aos apoiadores](/#Agradecimentos-aos-apoiadores)<br/><br/>
2. [Introdução e Instalação: Formas de instalação da biblioteca.](/introduction-and-installation)<br/>
2.1 [Instalação via Python Package Index (PIP)](/introduction-and-installation/#instalacao-via-python-package-index-pip)<br/>
2.2 [Instalação via GIT](/introduction-and-installation/#instalacao-via-git)<br/>
2.3 [Primeiros Passos](/introduction-and-installation/#primeiros-passos)<br/><br/>
3. [Documentação dos Objetos](/objects-documentation)<br/>
3.1 [Obtendo instância do webdriver do Firefox](/objects-documentation/#obtendo-instancia-do-webdriver-do-firefox)<br/>
3.2 [Criando Parser da Nossa Página](/objects-documentation/#criando-parser-da-nossa-pagina)<br/>
3.3 [Manipulador do ReCAPTCHA](/objects-documentation/#manipulador-do-recaptcha)<br/>
3.4 [Estados do ReCAPTCHA](/objects-documentation/#estados-do-recaptcha)<br/>
3.5 [Exceções](/objects-documentation/#excecoes)<br/><br/>
4. [Extra: Descubra como funcionam requisições, cookies, sessões e o reCAPTCHA.](/extra)<br/>
4.1 [O que é uma requisição?](/extra/#o-que-e-uma-requisicao)<br/>
4.2 [O que são Cookies e como funcionam?](/extra/#o-que-sao-cookies-e-como-funcionam)<br/>
4.3 [O que são Sessões e como funcionam?](/extra/#o-que-sao-sessoes-e-como-funcionam)<br/>
4.4 [O que é um Google reCAPTCHA e como funciona?](/extra/#o-que-e-um-google-recaptcha-e-como-funciona)<br/>

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
 definidos por sugestões dos espectadores._<br/><br/>


## Agradecimentos aos apoiadores
É com o apoio de vocês que este projeto é melhorado e que também ajuda com
minha vida pessoal e financeira, então eu agradeço grandemente à todas as
pessoas pela sua maravilhosa contribuição, **Muito Obrigado! <3**
<br/><br/>

<span align="center">

| Rank | Perfil | Nome | Data |
|-|-|-|-|
| #1   | <img src="https://www.gravatar.com/avatar/3516fabc30e2a6a444de239f80b133cd?d=mp" width="25"/> | Lucas Barros | 10/12/20 às 04:16:46 |

</span>
