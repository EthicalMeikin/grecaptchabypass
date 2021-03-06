<link rel="stylesheet" href="https://grecaptchabypass.readthedocs.io/index.css">

# Documentação dos Objetos
Neste artigo, entenda como funciona e como utilizar os objetos da biblioteca.
<br/><br/>

## Obtendo instância do webdriver do Firefox
**def** <span id="getBrowserFirefox">_**getBrowserFirefox(headless=True, \*args, \*\*kwargs)**_</span>

&nbsp;&nbsp;&nbsp;*Função que retorna uma instância do webdriver do
Firefox.*

* **headless (opcional)**: *Argumento recebido com True por padrão, com
objetivo de rodar o WebDriver sem interface gráfica.*<br/><br/>

* **args e kwargs (opcional)**: *Adicione argumentos adicionais que você
adicionaria em selenium.webdriver.Firefox.*
<br/><br/>


## Criando Parser da Nossa Página
**class** <span id="Bypass">_**Bypass(webdriver: object)**_</span>

&nbsp;&nbsp;&nbsp;*Classe responsável por controlar as atualizações e fazer um
parse da página.*

* **webdriver**: *Você deve passar a instância do seu WebDriver.*


&nbsp;&nbsp;&nbsp;**def** <span id="Bypass.getRecaptchas">_**getRecaptchas**_</span>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Método que retorna uma lista de
instâncias da classe [ReCAPTCHA](#manipulador-do-recaptcha) que referencia
cada Google ReCAPTCHA atual da página que foi obtido.*
<br/><br/>


## Manipulador do ReCAPTCHA
**class** _**ReCAPTCHA(webdriver: object, frame_name: str)**_

&nbsp;&nbsp;&nbsp;*Classe que referencia e manipula um Google ReCAPTCHA específico.*

* **webdriver**: *Você deve passar a instância do seu WebDriver.*
* **frame_name**: *Você deve passar o nome do frame do ReCAPTCHA que deseja
manipular.*

&nbsp;&nbsp;&nbsp;**def** *getState*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Método que retorna o
[Estado do ReCAPTCHA](#estados-do-recaptcha) atual.*

&nbsp;&nbsp;&nbsp;**def** *show*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Método que adiciona uma borda verde no
ReCAPTCHA com o propósito de localiza-lo.*
<center>
  <img src="https://github.com/EthicalMeikin/grecaptchabypass/raw/master/assets/ReCAPTCHA_show.png"/>
</center>

&nbsp;&nbsp;&nbsp;**def** *hide*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Método que remove a borda verde do
ReCAPTCHA para ocultar a exposição da localização.*
<center>
  <img src="https://github.com/EthicalMeikin/grecaptchabypass/raw/master/assets/ReCAPTCHA_hide.png"/>
</center>

&nbsp;&nbsp;&nbsp;**def** <span id="ReCAPTCHA.solve">_**solve**_</span>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Método que soluciona o ReCAPTCHA e retorna o código de resposta e os cookies atual do site.*
<center>
  <img
    src="https://github.com/EthicalMeikin/grecaptchabypass/raw/master/assets/ReCAPTCHA_solve.png"
    width="600"
  />
</center>
<br/><br/>


## Estados do ReCAPTCHA
**class** _**States**_

*Classe dos estados do ReCAPTCHA, responsável por identificar
o que está havendo com o ReCAPTCHA.*

| Estados                     | Descrição                                |
|-----------------------------|------------------------------------------|
| `recaptcha_unchecked`       | Desafio não resolvido.                   |
| `recaptcha_checked`         | Desafio resolvido.                       |
| `recaptcha_expired`         | Já esteve resolvido mas expirou.         |
| `recaptcha_image_challenge` | Desafio por imagem está selecionado.     |
| `recaptcha_audio_challenge` | Desafio por áudio está selecionado.      |
| `recaptcha_loading`         | Aguardando uma ação acontecer.           |

<br/>

## Exceções
**class** _exceptions.**InvalidRecaptchaException**_

&nbsp;&nbsp;&nbsp;*Exceção destinada para caso o ReCAPTCHA for inválido.*
<br/><br/>

**class** _exceptions.**RecaptchaNotFoundException**_

&nbsp;&nbsp;&nbsp;*Exceção destinada para caso o elemento do ReCAPTCHA suma.*
<br/><br/>

**class** _exceptions.**TimeoutException**_

&nbsp;&nbsp;&nbsp;*Exceção destinada para caso o tempo limite exceder.*
