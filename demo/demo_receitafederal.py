"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

# Bibliotecas nativas.
import json
import os
import time
from typing import Callable, Dict, List, NamedTuple

# Bibliotecas externas.
import parsel
import requests
from selenium.webdriver.support.wait import WebDriverWait
import grecaptchabypass


class ReceitaFederal:
    def _verifyMethodHasExecuted(target: Callable) -> Callable:
        """
        Decorador responsável por verificar se a classe
        ja foi utilizada.
        """
        def _(instance: object, *args, **kwargs) -> any:
            if not instance._executed:
                instance._executed = True
                return target(instance, *args, **kwargs)
            else:
                raise Exception(
                    'Você já utilizou esta classe, solucione outro '
                    'reCAPTCHA e instancie esta mesma classe novamente.'
                )
        return _

    def __init__(self, document: str, birthdate: str) -> None:
        # Documento do CPF.
        self.document = document

        # Data de nascimento.
        self.birthdate = birthdate

        # Atributo determinado para impedir futuras execuções.
        self._executed = False

    def _getCadastralDataFromHtml(self, html_response: str) -> Dict[str, str]:
        # Obtendo todos elementos dos dados cadastrais da página.
        cadastral_values = parsel.Selector(html_response)\
            .xpath('//span[contains(@class, "clConteudo")]').getall()

        # Extraindo dados dos elementos.
        cadastral_values = [
            ' '.join(parsel.Selector(x).xpath("//b/text()").getall())
            for x in cadastral_values if "<b>" in x
        ]

        # Chaves ou nomes pertencentes aos dados.
        cadastral_keys = [
            'CPF', 'nome', 'data_nascimento', 'situacao', 'data_inscricao',
            'digito_verificador', 'hora_comprovante', 'codigo_controle'
        ]

        # Retorna um dicionário com os dados obtidos.
        return dict(zip(
            cadastral_keys,
            list(map(lambda x: x.strip(), cadastral_values))
        ))

    @_verifyMethodHasExecuted
    def with_requests(self, cookies: List[NamedTuple],
                      gr_response: str) -> Dict[str, str]:
        """
        Método que fará a consulta utilizando apenas requisições, a forma
        mais rápida porém a mais conceitual.

        :args:
            cookies (List[NamedTuple]) -> São os cookies que vem do Selenium.

        :returns:
            Dict[str, str] -> Retorna um dicionário com os dados cadastrais
            obtidos.
        """
        # Cookies da sessão.
        cookies = '; '.join(
            f'{cookie["name"]}={cookie["value"]}'
            for cookie in cookies
        )

        # URL da requisição.
        URL = (
            'https://servicos.receita.fazenda.gov.br/servicos/cpf/'
            'consultasituacao/ConsultaPublicaExibir.asp'
        )

        # Headers que serão passados na requisição.
        HEADERS = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'servicos.receita.fazenda.gov.br',
            'Origin': 'https://servicos.receita.fazenda.gov.br',
            'Referer': (
                'https://servicos.receita.fazenda.gov.br/servicos/cpf/'
                'consultasituacao/ConsultaPublica.asp'
            ),
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) '
                'Gecko/20100101 Firefox/78.0'
            ),
            'Cookie': cookies
        }

        # Parâmetros POST que serão enviados na requisição.
        POSTDATA = {
            'idCheckedReCaptcha': 'false',
            'Enviar': 'Consultar',
            'txtCPF': self.document,
            'txtDataNascimento': self.birthdate,
            'g-recaptcha-response': gr_response
        }

        # Realizando a requisição POST.
        REQUEST = requests.post(
            url=URL,
            data=POSTDATA,
            headers=HEADERS
        )

        # Retornando os dados num dicionário.
        return self._getCadastralDataFromHtml(REQUEST.text)

    @_verifyMethodHasExecuted
    def with_selenium(self, webdriver: object) -> Dict[str, str]:
        """
        Método que fará a consulta utilizando Selenium, a forma
        mais lenta porém a mais simples de produzir.

        :args:
            webdriver (object) -> Especifique sua instância do WebDriver.

        :returns:
            Dict[str, str] -> Retorna um dicionário com os dados cadastrais
            obtidos.
        """
        # Digitando CPF.
        webdriver.find_element_by_id("txtCPF").send_keys(self.document)

        # Obtendo elemento input para digitar data de nascimento.
        input_birthdate = webdriver.find_element_by_id("txtDataNascimento")

        # Digitando data de nascimento.
        input_birthdate.send_keys(self.birthdate)

        # Realizando a consulta.
        input_birthdate.submit()

        # Congelando o programa até carregar a outra página.
        while "ConsultaPublicaExibir.asp" not in webdriver.current_url:
            time.sleep(0.01)

        # Aguardando a presença dos dados na página.
        WebDriverWait(
            driver=webdriver,
            timeout=30
        ).until(
            method=lambda x: x.find_element_by_class_name("clConteudoComp"),
            message="Sua conexão está lenta ou houve um erro."
        )

        # Retornando os dados num dicionário.
        return self._getCadastralDataFromHtml(webdriver.page_source)


if __name__ == '__main__':
    # Iniciando browser, se headless for True o browser rodará em background.
    browser = grecaptchabypass.getBrowserFirefox(headless=False)

    # Instanciando classe Bypass.
    bypass = grecaptchabypass.Bypass(webdriver=browser)

    print(
        " Aguarde a página carregar para a demonstração funcionar "
        "corretamente."
    )

    # Entrando na página onde o recaptcha está sendo exibido.
    browser.get(
        'https://servicos.receita.fazenda.gov.br/servicos/cpf/'
        'consultasituacao/ConsultaPublica.asp'
    )

    input('> Pressione ENTER para quebrar o recaptcha.')

    # Obtendo todos os reCAPTCHAs que foram encontrados.
    recaptchas = bypass.getRecaptchas()

    # Assert para interromper o programa caso não houver resultados.
    assert recaptchas, "Não foram encontrados nenhum ReCAPTCHA."

    # Obtendo primeiro ReCAPTCHA da lista.
    recaptcha = recaptchas[0]

    # Quebrando o recaptcha.
    grecaptcha_response, grecaptcha_cookies = recaptcha.solve()

    print(
        "\n[!] Não demore muito para preencher estes dados, ou o reCAPTCHA "
        "irá expirar.\n"
    )

    # Instanciando a classe ReceitaFederal.
    receitafederal = ReceitaFederal(
        document=input('>  (1/2) Insira o CPF (xxx.xxx.xxx-xx): '),
        birthdate=input('>  (2/2) Insira a Data de Nascimento (dd/mm/aaaa): ')
    )

    while True:
        # Pedindo para escolher um método.
        method_name = input(
            '\n'
            ' [1] Consultar com Requests (Mais rápido)\n'
            ' [2] Consultar com Selenium (Mais lento)\n\n'
            '> Escolha o método para consultar: '
        )

        # Dicionário com os métodos.
        methods = {
            "1": lambda: receitafederal.with_requests(
                cookies=grecaptcha_cookies,
                gr_response=grecaptcha_response
            ),
            "2": lambda: receitafederal.with_selenium(
                webdriver=browser
            )
        }

        # Caso o método pedido não estiver no dicionário.
        if method_name in methods:
            # Executando método escolhido.
            cadastral_data = methods[method_name]()

            # Se os dados foram pegos com èxito.
            if cadastral_data:
                if len(cadastral_data) > 1:
                    print("JSON:", json.dumps(cadastral_data, indent=2))
                else:
                    print("Data de nascimento incorreta.")
            else:
                print(
                    "A consulta não houve retorno, você preencheu os dados "
                    "corretamente?"
                )
            break
        else:
            print("\n Opção inexistente, tente de novo!")
