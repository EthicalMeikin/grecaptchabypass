<link rel="stylesheet" href="https://gist.githubusercontent.com/EthicalMeikin/c4d7bf093ba6ef5710924adf80009dba/raw/b07036c7e122fa8e14541d2ed8da3eb1774a3d1c/index.css">

# Introdução e Instalação
Nesta página iremos acompanhar a instalação da nossa biblioteca para depois
finalmente então começar a realizar a quebra de Google reCAPTCHAs.

## Instalação via Python Package Index (PIP)
Esta é uma instalação diretamente do *PyPi*, onde será baixada somente versões
que foram aprovadas antes de serem publicadas.

Para fazer a instalação da última versão da biblioteca utilizando o `pip`,
digite a seguinte linha de comando:

```
pip install grecaptchabypass
```

ou

```
python -m pip install grecaptchabypass
```

## Instalação via GIT
Esta é uma instalação utilizando GIT, cujo o projeto vem do *GitHub*, e
portanto esta é uma maneira de instalar versões betas que ainda serão
publicadas no *PyPi*.

Para fazer a instalação da biblioteca via GIT, clone o repositório digitando a
seguinte linha de comando:

```
git clone https://github.com/EthicalMeikin/grecaptchabypass.git
```

Logo após clonar o diretório, instale a biblioteca digitando a seguinte linha
de comando:

```
pip install -e grecaptchabypass
```

## Primeiros Passos
Para começar a fazer a utilização da biblioteca e realizar a quebra de _Google
reCAPTCHAs_, você irá precisar ter uma noção de **Selenium** e também talvez
**Requests** caso queira uma solução mais rápida.

_Você pode ler a documentação de todos os objetos [aqui](/objects-documentation)._

<br/>
**1.** Comece importando a biblioteca da forma que você achar melhor.

```python
import grecaptchabypass as gre
```
<br/>
**2.** Após a importação, crie uma instância do webdriver já configurado para não ser
detectado.
[Saiba mais sobre a função **getBrowserFirefox**.](/objects-documentation#getBrowserFirefox)

```python
# Criando a instância do webdriver sem rodar o browser em background.
browser = gre.getBrowserFirefox(headless=False)
```
<br/>
**3.** Instancie a classe responsável por obter os ReCAPTCHAs da página atual.
[Saiba mais sobre a classe **Bypass**.](/objects-documentation#Bypass)
```python
# Instanciando a classe responsável por obter os ReCAPTCHAs da página atual
bypass = gre.Bypass(webdriver=browser)
```
<br/>
**4.** Navegue para a página que seu ReCAPTCHA é exibido.
```python
# Navegando para a página que há o ReCAPTCHA.
browser.get('https://patrickhlauke.github.io/recaptcha/')
```
<br/>
**5.** Obtenha os ReCAPTCHAs da página. [Saiba mais sobre o método **getRecaptchas**.](/objects-documentation#Bypass.getRecaptchas)
```python
# Obtendo o todos os ReCAPTCHAs que foram encontrados na página.
recaptchas = bypass.getRecaptchas()

# Assert para interromper o programa caso não houver resultados.
assert recaptchas, "Não foram encontrados nenhum ReCAPTCHA."

# Obtendo o primeiro ReCAPTCHA que for encontrado.
recaptcha = recaptchas[0]
```
<br/>
**6.** Agora finalmente quebre o ReCAPTCHA. [Saiba mais sobre o método **solve**.](/objects-documentation#ReCAPTCHA.solve)
```python
# Quebrando o ReCAPTCHA e obtendo ReCAPTCHA Response e os Cookies da página.
gresponse, cookies = recaptcha.solve()
```
