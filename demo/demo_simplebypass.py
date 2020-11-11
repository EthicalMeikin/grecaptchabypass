"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

import colorama
import grecaptchabypass
colorama.init()

if __name__ == '__main__':
    # Iniciando browser, se headless for True o browser rodará em background.
    browser = grecaptchabypass.getBrowserFirefox(headless=False)

    # Instanciando classe Bypass.
    bypass = grecaptchabypass.Bypass(webdriver=browser)

    # Barras ou espaçador de linhas.
    bars = colorama.Fore.CYAN + (57 * "=") + colorama.Fore.RESET

    # Título da demonstração.
    title = (
        f" {colorama.Fore.CYAN}[Demo] {colorama.Fore.WHITE}Simples Quebra "
        "de um ReCAPTCHA"
    )

    # Descrição da demonstração.
    description = (
        f"{colorama.Fore.WHITE}"
        " Esta demonstração irá apresentar uma simples quebra de "
        "\n um Google ReCAPTCHA."
    )

    # Exibindo informações da demonstração.
    print(f"{bars}\n{title}\n{bars}\n{description}\n{bars}")

    # Entrando na página onde o recaptcha está sendo exibido.
    browser.get("https://google.com/recaptcha/api2/demo")

    # Obtendo todos os reCAPTCHAs que foram encontrados.
    recaptchas = bypass.getRecaptchas()

    # Assert para interromper o programa caso não houver resultados.
    assert recaptchas, "Não foram encontrados nenhum ReCAPTCHA."

    # Obtendo primeiro ReCAPTCHA da lista.
    recaptcha = recaptchas[0]

    # Quebrando o recaptcha.
    grecaptcha_response, grecaptcha_cookies = recaptcha.solve()

    print(
        "ReCAPTCHA quebrado!\n\n"
        f" Response: {grecaptcha_response}\n\n"
        f" Cookies: {grecaptcha_cookies}"
    )
