<link rel="stylesheet" href="https://gist.githubusercontent.com/EthicalMeikin/c4d7bf093ba6ef5710924adf80009dba/raw/b07036c7e122fa8e14541d2ed8da3eb1774a3d1c/index.css">

# Extra

Esta página é destinada para os que não possuem muito conhecimento com
requisições, se você ja sabe o suficiente não irá precisar fazer a leitura.

## O que é uma requisição?

Uma requisição nada mais é que um pedido que você faz para um determinado
*Servidor Web (HTTP/HTTPs)* com a finalidade de ele te enviar uma resposta.

Esta resposta que o Servidor Web retorna pode se tratar de uma página
**HTML** ou mídia hospedada no *Servidor Web* como imagens, vídeos ou outros
arquivos que não são interpretados pelo Browser como uma página.

**Como assim? O que você quis dizer com "Interpretados pelo Browser"?**

Um Browser tem o propósito de realizar as requisições para o
Servidor Web que o usuário está querendo entrar, de forma que o usuário não
precise saber o que é uma requisição, somente uma interface gráfica é exibida e
não há complicações.

Então à partir do momento que o cliente tenta entrar num Servidor Web, o
Browser envia um pedido/requisição para o Servidor Web, o
Servidor Web então retorna uma resposta para o Browser e o Browser
analisa se é uma página **HTML** ou o conteúdo de um arquivo binário como
Imagens, Vídeos, PDF e entre outros arquivos.

Após a análise de resposta, se a resposta for uma página **HTML**, o
Browser irá interpretar o código **HTML** da página e irá exibir objetos
visíveis na página como imagens, divisões, formulários e entre outros objetos
que ajuda um usuário comum à visualizar a página.

**Certo, já entendemos o mecanismo de como tudo acontece, mas o que são esses
pedidos e essas respostas?**

Vamos então entender o básico do protocolo HTTP e simular a comunicação
entre um **Cliente** e um **Servidor Web**, então para acessar o nosso
Servidor Web imaginário, o URL que quero acessar
é: `http://website.com/login.php`.

O cliente então começa criando uma Conexão Socket com o IP do Site e
sua Porta. Em Python isto equivale à:

```python
import socket

"""
Versões de IP (Internet Protocol):

  socket.AF_INET  -> Indica a utilização de conexão com IPv4.
  socket.AF_INET6 -> Indica a utilização de conexão com IPv6.

Tipos de comunicações:

  socket.SOCK_DGRAM  -> Indica que queremos uma conexão UDP.
  socket.SOCK_STREAM -> Indica que queremos uma conexão TCP.
"""


# Queremos uma comunicação TCP e utilizando IPv4.
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Armazenando o nome do HOST e a porta do Servidor Web para realizar a conexão.
website = "website.com", 80

# Realizando a conexão com o Servidor web.
connection.connect(website)
```

**Pronto! Esta foi a conexão com o Servidor, não parece algo muito complicado
né?**

Feita a conexão, enviamos o pedido para o Servidor Web. Um pedido com o
protocolo HTTP é dividido em apenas duas seções, são elas:

* *Header (Cabeçalho)*: Responsável por explicar para o Servidor o que
exatamente quero receber e o que é o meu pedido.<br/><br/>

* *PostData (Parâmetros POST)*: Responsável por enviar dados isolados para
para se comunicar com o servidor.

Aqui está um exemplo de pedido com método *POST* para receber a resposta da
página `login.php`:

**\* Lembrando que a seção PostData só pode ser informada se o método da
requisição for POST.**

```
POST /login.php HTTP/1.1
Host: website.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT....
Referer: http://website.com/login.php

nome=EthicalMeikin
```

Em Python isto equivale á:

```python
# Nosso pedido em Byte-Code ('\r\n' é obrigatório nas quebras de linha).
request = (
  "POST /login.php HTTP/1.1\r\n"
  "Host: website.com\r\n"
  "Connection: keep-alive\r\n"
  "User-Agent: Mozilla/5.0 (Windows NT....\r\n"
  "Referer: http://website.com/login.php\r\n"
  "\r\n"
  "nome=EthicalMeikin\r\n"
).encode()

# Enviando o pedido para o Servidor Web.
connection.send(request)
```

**Bacana! Fizemos um pedido para o Servidor Web.**

Recapitulando, estes são os significados dos cabeçalhos que foram passados:

* `POST /login.php HTTP/1.1`: *Informando que meu pedido é do método
**POST**, arquivo do servidor que iremos acessar e a versão do protocolo HTTP
que estamos usando para se comunicar.*<br/><br/>

* `Host: website.com`: *Informando o HOST do Servidor Web da conexão.*<br/><br/>

* `Connection: keep-alive`: *Informando que queremos que o servidor mantenha
a mesma conexão ativa para não fecha-la após o envio do pedido.*<br/><br/>

* `User-Agent: Mozilla/5.0 (Windows NT..`: *Informando o Agente, aquele
que está agindo na comunicação, ele tem um formato que informa o sistema
operacional e o navegador que está sendo utilizado.*<br/><br/>

* `Referer: http://website.com/login.php`: *Informando a referência, ou o motivo
da requisição, aquele que foi por ele que a requisição foi pedida para ser
enviada.*

**Certo! Fizemos o pedido, agora vamos receber a resposta do Servidor Web.**

Uma resposta HTTP é dividida em apenas duas seções, são elas:

* *Header (Cabeçalho)*: Informa se a requisição foi bem sucedida, tipo de
página que foi retornada e entre outros.
* *Content (Conteúdo da Página)*: O conteúdo da página que estamos buscando.

Um exemplo da resposta do Servidor Web:

```
HTTP/1.1 200 OK
Server: TornadoServer/6.0.4
Content-Type: text/html
Date: Sat, 12 Sep 2020 16:00:11 GMT
Accept-Ranges: bytes
Content-Length: 75

<!DOCTYPE html>
<html>
  <body>
    <h1>Oi EthicalMeikin!</h1>
  </body>
</html>
```

Recapitulando, estes são os significados dos cabeçalhos que foram recebidos:

* `HTTP/1.1 200 OK`: *Retorna a versão do protocolo HTTP que o servidor usa, o
código de status e a mensagem referente ao código de status que quer dizer se a
página existe, se o houve erro ao processar o pedido e entre outras
coisas.*<br/><br/>

* `Server: TornadoServer/6.0.4`: *Retorna qual o nome e versão do servidor está
rodando o Servidor Web.*<br/><br/>

* `Content-Type: text/html`: *Retorna qual é o tipo de conteúdo que o servidor
está retornando.*<br/><br/>

* `Date: Sat, 12 Sep 2020 16:00:11 GMT`: *Retorna o horário atual do
Servidor Web.*<br/><br/>

* `Accept-Ranges: bytes`: *Retorna o tipo de tamanho de bytes
(Ex: Bytes, Kabytes).*<br/><br/>

* `Content-Length: 75`: *Retorna o tamanho do conteúdo referente ao tipo de
tamanho de bytes que foi retornado.*

A resposta em Python equivale à:

```python
# Pedindo até 9999 Bytes da resposta do Servidor Web, talvez o bastante para Obter a resposta completa se a resposta não for muito grande, decodificando para uma String UTF-8 e depois separando as seções resultando numa lista.
response = response_headers, response_content = self.recv(9999).decode().split("\r\n\r\n")
```

## O que são Cookies e como funcionam?
Eles são muito utilizados para armazenar chaves de segurança ou sua sessão em
um login.

Os *Cookies* tem o propósito de dar liberdade para o Servidor Web
armazenar dados no Browser do usuário, como um pequeno *Banco de Dados*
isolado para o Servidor Web específico.

**Como são criados os Cookies?**

Os Cookies são criados durante as requisições, especificamente no cabeçalho
da resposta do Servidor Web através do cabeçalho `Set-Cookie`.

Por exemplo: `Set-Cookie: nome_do_cookie=valor_do_cookie; expires=Sat, 12-Sep-2020 17:30:32 GMT; path=/; domain=website.com; secure; HttpOnly`

Este cabeçalho é o responsável pela criação de cookies no seu navegador, seu
navegador lê este cabeçalho de resposta e adiciona num banco de dados isolado.

Entendendo o Cookie criado:

* `domain`: *O Browser cria um banco de dados com o domínio que foi
especificado no Cookie para isolar os Cookies de cada Servidor Web.*<br/><br/>

* `expires`: *Contém a data de expiração do Cookie, que ele será apagado do
banco de dados do Browser.*<br/><br/>

* `path`: *Contém o local no servidor Web em que o Cookie irá existir.*<br/><br/>

* `secure`: *Informa que o cookie deve existir quando houver uma conexão segura
(SSL/TLS - HTTPs).*<br/><br/>

* `HttpOnly`: *Informa que o cookie deve existir quando o protocolo for HTTP.*
<br/><br/>

* `nome_do_cookie`: *Nome do Cookie e seu valor a ser criado e armazenado no
banco de dados do seu navegador.*

**Tá. Mas, como o Servidor Web está acessando o banco de dados
do meu navegador?**

Bem, na verdade a resposta é bem simples, ele não está acessando seu banco de
dados, você que está enviando os cookies criados em todas as requisições que
você faz para o Servidor Web através do cabeçalho `Cookie`.

Por exemplo: `Cookie: nome_do_cookie1=valor_do_cookie1; nome_do_cookie2=valor_do_cookie2`

No exemplo acima eu especifiquei dois Cookies, onde `;` se trata de um
delimitador para separar os cookies que você quer informar.

## O que são Sessões e como funcionam?
Uma sessão se trata de um Cookie no seu navegador onde no valor contém o nome
da sessão que foi criada, que quando especificado, o Servidor Web lê o nome
da sessão e acessa o conteúdo do arquivo que está armazenado no servidor com o
mesmo nome da sessão e assim revelando o que está armazenado, sendo um dos
métodos mais seguros de armazenar credenciais sem que elas fiquem expostas no
Cookie, mas dentro do arquivo da sessão.

Por exemplo: `Cookie: PHPSESSID=syxmawolcn`. No exemplo você está passando o
nome de uma sessão (`syxmawolcn`) no Cookie de sessão (`PHPSESSID`), e
então no servidor o conteúdo do arquivo `tmp_syxmawolcn` é acessado e sem
exibir o conteúdo para o usuário.

## O que é um *Google reCAPTCHA* e como funciona?
Um *Google Response* é o código de resposta que seu Google reCAPTCHA gera quando você
o-soluciona. O reCAPTCHA tem o propósito de impedir uma automatização
em um site específico, como em um formulário, de forma que para solucionar é
necessário se comportar como humano, selecionar imagens específicas ou digitar
o que um audio diz; Este é um dos problemas que o pessoal do scraping muitas
vezes passam por ficarem incapazes de fazer scraping numa página que contém um
reCAPTCHA.

**Para entender como ele funciona, precisamos entender como ele é integrado
numa página.**

Antes de tudo, é necessário ter um Servidor Web para você hospedar seu arquivo
HTML ou PHP que haja um domínio. Entretanto você também pode pode utilizar um
servidor local, porém deve ser acessado através do nome do *DNS (localhost)*
ao invés do *IPv4 (0.0.0.0/192.168.x.x/127.0.0.1)*.

Tendo um servidor em mãos, criaremos duas chaves para integrar nosso reCAPTCHA,
são elas:

  1. **Chave pública:** usada para gerar o reCAPTCHA, cada site tem sua chave.
  2. **Chave secreta:** usada para verificar se o reCAPTCHA foi solucionado.

> *Para criar estas chaves você pode clicar
[aqui](https://www.google.com/recaptcha/admin/create).*

Tendo as duas chaves em mão, adicionamos duas tags em nosso arquivo HTML ou
PHP, são elas:

 1. `<script src='https://www.google.com/recaptcha/api.js'></script>`:
 *Irá carregar o código JavaScript do reCAPTCHA.*

 2. `<div class='g-recaptcha' data-sitekey='CHAVE-PUBLICA'></div>`:
 *Irá ser o reCAPTCHA que aparecerá na página.*

Então basta adiciona-los:

```html
<!DOCTYPE html>
<html>
  <body>
    <!-- Seu formulário POST -->
    <form method='POST'>
      <!-- Seu campo (opcional) -->
      <input name='nome' placeholder='insira seu nome:'>

      <!-- Seu reCAPTCHA que será carregado -->
      <div class='g-recaptcha' data-sitekey='SUA-CHAVE-PUBLICA-AQUI'></div>

      <!-- Botão de envio do formulário -->
      <input type='submit'/>
    </form>

    <!-- Carregando o JavaScript do reCAPTCHA -->
    <script src='https://www.google.com/recaptcha/api.js'></script>
  </body>
</html>
```

**Isto fará exibir o reCAPTCHA na página, mas e como saber se o reCAPTCHA foi
resolvido?**

Basta obter o *reCAPTCHA Response*, para obter usamos o PHP:

```
<?php
    // Caso haja parâmetros POST recebidos do formulário.
    if($_POST){
      //////////////////////////////////////////////////////////
      // Preparando os dados que serão enviados na requisição //
      //////////////////////////////////////////////////////////

      // Obtendo o reCAPTCHA Response (Nota: 'g-recaptcha-response' é o nome do parâmetro POST que veio do reCAPTCHA).
      $gresponse = $_POST['g-recaptcha-response']

      // Armazenando a chave secreta.
      $recaptcha_secret_key = "SUA-CHAVE-SECRETA"

      // URL da API que irá verificar o reCAPTCHA Response.
      $gverify_url = "https://www.google.com/recaptcha/api/siteverify";

      // Definindo parâmetros POST que serão enviados em ArrayDict e convertendo para formato de query.
      $request_postfields = http_build_query(
        array(
          "secret" => $recaptcha_secret_key,
          "response" => $gresponse
        );
      );

      //////////////////////////////////////////////////////
      // Realizando a requisição para a API do reCAPTCHA. //
      //////////////////////////////////////////////////////

      // Inicializando cURL.
      $ch = curl_init();

      // Definindo dados para a requisição.
      curl_setopt_array(
        // Definindo URL da requisição.
        CURLOPT_URL => $gverify_url,

        // Definindo que será método POST.
        CURLOPT_POST => true,

        // Passando os parâmetros POST.
        CURLOPT_POSTFIELDS => $request_postfields,

        // Informando ao cURL que queremos que ele retorne a resposta ao invés de printar diretamente na página.
        CURLOPT_RETURNTRANSFER => true
      );

      // Executando a requisição, armazenando a resposta (JSON) na variável e convertendo o JSON para ArrayDict.
      $api_response = json_decode(curl_exec($ch), true);

      // Fechando o cURL.
      curl_close($ch);

      // Caso o reCAPTCHA Response seja válido.
      if($api_response['success']){
        echo "Você não é um robô!";
      }
      else {
        echo "Código de resposta do reCAPTCHA inválido.";
      }
    }
?>
```

**Ok! Agora temos a solução, porém eu não faço ideia de como implementar este projeto num scraping específico. Como implementar?**

###### Solução usando somente Selenium

Embora seja uma solução lenta por conta do browser, é a mais fácil de fazer.
Basta simplesmente manipular o WebDriver que foi usado para quebrar o
*Google Response* e pronto! Você terá conseguido o que queria.

###### Solução usando requisições sem o browser

Uma solução bem mais rápida por não haver interface gráfica nem carregamento de
mídias, folhas de estilo ou scripts, porém a mais complicadinha. A solução é
enviar a requisição **POST** passando os cookies na requisição e o
*reCAPTCHA Response* no parâmetro `g-recaptcha-response` e pronto! Você também
irá conseguir.
