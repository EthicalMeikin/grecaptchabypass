"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

import grecaptchabypass

if __name__ == '__main__':
    # Iniciando browser, se headless for True o browser rodará em background.
    browser = grecaptchabypass.getBrowserFirefox(headless=False)

    # Instanciando classe Bypass.
    bypass = grecaptchabypass.Bypass(webdriver=browser)

    # Entrando na página onde o recaptcha está sendo exibido.
    browser.get("http://patrickhlauke.github.io/recaptcha/")

    # Obtendo todos os reCAPTCHAs que foram encontrados.
    recaptchas = bypass.getRecaptchas()

    # Assert para interromper o programa caso não houver resultados.
    assert recaptchas, "Não foram encontrados nenhum ReCAPTCHA."

    # Obtendo primeiro ReCAPTCHA da lista.
    recaptcha = recaptchas[0]

    # Quebrando o recaptcha.
    grecaptcha_response, grecaptcha_cookies = recaptcha.solve()
