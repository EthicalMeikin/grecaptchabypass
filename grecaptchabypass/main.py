"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

from .lib import (
    _collections, _io, _os, _parsel, _PIL, _pydub, _re, _requests, _selenium,
    _speech_recognition, _subprocess, _time
)

from .exceptions import (
    InvalidRecaptchaException, RecaptchaNotFoundException, TimeoutException
)

from typing import (
    Callable, Tuple, List, Dict, BinaryIO
)

from .cache import ReCAPTCHACache
from .utils import SeleniumUtils


class ProjectVersion:
    def _extractVersionFlags(version: str):
        # Retornando as flags da versão.
        return map(int, _re.compile(r"[0-9]+").findall(version))

    def _updatedLocalVersion(last_version: List[int],
                             local_version: List[int]) -> bool:
        # Iterando cada fragmento da versão.
        for la, lo in zip(last_version, local_version):
            # Se a flag da versão local não for menor que o da ultima versão
            if not lo <= la:
                # Se verdadeiro, retorna True.
                return True

        # Senão, retorna False.
        return False

    @classmethod
    def verifyModuleVersion(cls):
        # Obtendo o nome do projeto/diretório.
        project_name = _os.basename(_os.dirname(__file__)).split("-")[0]

        # Enviando comando no shell e extraindo a versão usando regex.
        local_version = _re.compile(r"Version: ([^\n]+)")\
            .findall(_subprocess.getoutput(
                f"python -m pip show {project_name}"
            ))

        # Realizando requisição para o projeto no pypi e extraindo a versão.
        last_version = _parsel.Selector(
            _requests.get(
                url=f"https://pypi.org/project/{project_name}"
            ).text
        ).xpath('//p[@class="release__version"]/text()').get().strip()

        # Se as versões foram obtidas.
        if all([bool(local_version), bool(last_version)]):
            # Obtendo se a versão local está desatualizada.
            _outdated_local_version = not cls._updatedLocalVersion(
                *map(
                    cls._extractVersionFlags,
                    [last_version, local_version[0]]
                )
            )

            if _outdated_local_version:
                # Printa se a versão estiver desatualizada.
                print(
                    f"[{project_name}] Versão {last_version} "
                    "está disponível!"
                )


def getBrowserFirefox(headless=True, *args, **kwargs) -> object:
    # Instanciando opções do firefox.
    options = _selenium.webdriver.FirefoxOptions()

    # Definindo preferência para remover detecção de webdriver via DOM.
    options.set_preference("dom.webdriver.enabled", False)

    # Se {headless=True}, o browser rodará em segundo plano.
    if headless:
        options.add_argument("--headless")

    # Criando instância do webdriver.
    webdriver = _selenium.webdriver.Firefox(
        options=options,
        *args,
        **kwargs
    )

    # Adicionando na instância funções úteis que não há no _selenium.
    setattr(
        webdriver, "_selenium_utils",
        SeleniumUtils(webdriver=webdriver)
    )

    # Retornando a instância de comunição com WebDriver.
    return webdriver


class States:
    RECAPTCHA_UNCHECKED = "recaptcha_unchecked"
    RECAPTCHA_CHECKED = "recaptcha_checked"
    RECAPTCHA_EXPIRED = "recaptcha_expired"
    RECAPTCHA_IMAGE_CHALLENGE = "recaptcha_image_challenge"
    RECAPTCHA_AUDIO_CHALLENGE = "recaptcha_audio_challenge"
    RECAPTCHA_LOADING = "recaptcha_loading"


class ReCAPTCHA:
    def _updateRecaptchaFrames(target):
        def _(instance, *args, **kwargs):
            # Obtendo o frame atual.
            current_frame = (
                instance._webdriver._selenium_utils.getCurrentFrame()
            )

            # Dando foco pra a página inicial.
            instance._webdriver.switch_to.default_content()

            #########################################
            # Obtendo o frame da caixa do reCAPTCHA #
            #########################################

            # Lista de Google reCAPCTHAs que foram encontrados.
            _frame_box = instance._webdriver.find_elements_by_xpath(
                f"{Bypass._recaptcha_box_element_xpath}"
                f"[@name='a-{instance._frame_name}']"
            )

            # Verificando se o reCAPTCHA foi localizado na página.
            if _frame_box:
                instance._frame_box = _frame_box[0]
            else:
                raise RecaptchaNotFoundException(
                    "Isn't possible to locate the reCAPTCHA in current page."
                )

            ###########################################
            # Obtendo o frame de desafio do reCAPTCHA #
            ###########################################

            # Lista de desafios de Google reCAPCTHAs que foram encontrados.
            _all_challenges_for_this_recaptcha = instance\
                ._webdriver.find_elements_by_xpath(
                    f"{Bypass._recaptcha_challenge_element_xpath}"
                    f"[@name='c-{instance._frame_name}']"
                )

            # verificando se há algum desafio para este reCAPTCHA.
            if _all_challenges_for_this_recaptcha:
                # Obtendo último elemento da lista.
                instance._frame_challenge = (
                    _all_challenges_for_this_recaptcha[-1]
                )

                # Dando foco para o frame anterior.
                if current_frame:
                    instance._webdriver._selenium_utils.switchToFrame(
                        current_frame
                    )

                return target(instance, *args, **kwargs)
            else:
                # Mensagem de erro do ReCAPTCHA.
                message_error = instance._getAnchorErrorMessage()

                # Caso não houver mensagem de erro.
                if not message_error:
                    message_error = 'Algo deu errado com o ReCAPTCHA.'

                raise InvalidRecaptchaException(
                    f"This reCAPTCHA is invalid "
                    f"({message_error})."
                )

        return _

    def __init__(self, webdriver: object, frame_name: str):
        # Definindo atributo com o WebDriver.
        self._webdriver = webdriver

        # Frames do Google reCAPTCHA.
        self._frame_name = frame_name

        # Dicionário com ID de elementos do reCAPTCHA.
        self._id = {
            # ID do elemento de botão de desafio por modo audio.
            "getAudioModeButton": "recaptcha-audio-button",

            # ID do elemento que contém o link do audio.
            "getAudioDownloadLink": "audio-source",

            # ID do elemento input para digitar a resposta do desafio.
            "getAudioInput": "audio-response",

            # ID do elemento âncora do reCAPTCHA que resolve o reCAPTCHA.
            "getAnchorButton": "recaptcha-anchor",

            # ID do elemento do botão que enviará a resposta do desafio.
            "getAudioInputSubmit": "recaptcha-verify-button"
        }

        self._class_name = {
            # Classe do elemento de botão que recarrega o audio do desafio.
            "reloadAudioLink": "reload-button-holder",

            # Classe para identificar se o reCAPTCHA está checkado.
            "recaptchaChecked": "recaptcha-checkbox-checked",

            # Classe para identificar se o reCAPTCHA está desmarcado.
            "recaptchaUnchecked": "recaptcha-checkbox-unchecked",

            # Classe para identificar se o reCAPTCHA está expirado.
            "recaptchaExpired": "recaptcha-checkbox-expired",

            # Classe para identificar se o reCAPTCHA está carregando.
            "recaptchaLoading": "recaptcha-checkbox-loading",

            # Classe pra identificar se está em desafio por imagem.
            "imageChallenge": "rc-imageselect-tabloop-begin",

            # Classe para identificar se está em desafio por audio.
            "audioChallenge": "rc-audiochallenge-tabloop-begin",

            # Classe para obter a mensagem de erro do desafio por audio.
            "getAudioErrorMessage": "rc-audiochallenge-error-message",

            # Classe para obter a mensagem de erro da caixa do reCAPTCHA.
            "getAnchorErrorMessage": "rc-anchor-error-message"
        }

        # Frequência de validação.
        self._poll_frequency = 0.01

        # Atributo que irá armazenar o reCAPTCHA Response obtido.
        self._recaptcha_response = ""

        # Escondendo a borda do ReCAPTCHA.
        self.hide()

    def _getAnchorErrorMessage(self):
        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        # Dando foco para a caixa do reCAPTCHA.
        self._webdriver._selenium_utils.switchToFrame(self._frame_box)

        # Obtendo o erro.
        _error_message = self._webdriver.find_elements_by_class_name(
            self._class_name["getAnchorErrorMessage"]
        )

        # Voltando para o frame anterior.
        if current_frame:
            self._webdriver._selenium_utils.switchToFrame(current_frame)

        return _error_message[-1].text.strip() if _error_message else ''

    @_updateRecaptchaFrames
    def __repr__(self):
        # Obtendo as posições do reCAPTCHA.
        posx, posy = self._frame_box.location.values()

        # Obtendo estado do reCAPTCHA.
        state = self.getState()

        # Retornando representação do objeto.
        return (
            f"{self.__class__.__name__}"
            f"(state={ascii(state)}, positionX={posx}, positionY={posy})"
        )

    @_updateRecaptchaFrames
    def _checkRecaptchaIsChecked(self):
        # Verificando se o reCAPTCHA está checkado.
        if self.getState() == States.RECAPTCHA_CHECKED:
            return True

    @_updateRecaptchaFrames
    def _getRecaptchaResponse(self) -> Tuple[str, list]:
        # Caso não haja um reCAPTCHA Response armazenado.
        if not self._recaptcha_response:
            # Dando foco para a página principal.
            self._webdriver.switch_to.default_content()

            # Tupla nomeada para o resultado da quebra do reCAPTCHA.
            nt_grecaptcha_result = _collections.namedtuple(
                typename="gRecaptchaResult",
                field_names=["response", "cookies"]
            )

            # Obtendo cookies do site atual.
            _grecaptcha_cookies = list(filter(
                lambda x: x["domain"] in self._webdriver.current_url,
                self._webdriver.get_cookies()
            ))

            # Obtendo reCAPTCHA response.
            _grecaptcha_response = self._webdriver.execute_script(
                "return window.grecaptcha.getResponse()"
            )

            # Armazenando a resposta do reCAPTCHA.
            self._recaptcha_response = nt_grecaptcha_result(
                _grecaptcha_response, _grecaptcha_cookies
            )

        # Retornando resposta do recaptcha.
        return self._recaptcha_response

    @_updateRecaptchaFrames
    def _waitFor(self, state: str):
        # Esperando o estado especificado aparecer.
        while self.getState() != state:
            _time.sleep(self._poll_frequency)

    @_updateRecaptchaFrames
    def _noWaitFor(self, state: str, timeout=20):
        # TImestamp inicial.
        initial_timestamp = _time.time()

        # Esperando o estado especificado não aparecer.
        while self.getState() == state:
            _time.sleep(self._poll_frequency)
            if (_time.time() - initial_timestamp) > timeout:
                raise TimeoutException("State expected has timeout.")

    @_updateRecaptchaFrames
    def _waitRecaptchaSpinner(self):
        # Enquanto o spiiner do reCAPTCHA estiver rodando.
        while self.getState() == States.RECAPTCHA_LOADING:
            _time.sleep(self._poll_frequency)

    @_updateRecaptchaFrames
    def _getTextFromAudioFile(self, audio_file: BinaryIO) -> str:
        # Convertendo o arquivo mp3 para wav.
        audio_file = _io.BytesIO(
            _pydub.AudioSegment.from_file(audio_file).export(
                audio_file, format="wav"
            ).getvalue()
        )

        # Abrindo audio wav para realizar o reconhecimento de voz.
        with _speech_recognition.AudioFile(audio_file) as _audio_file:
            # Instanciando classe de reconhecimento de fala.
            recognizer = _speech_recognition.Recognizer()

            # Realizando o reconhecimento de fala.
            return recognizer.recognize_google(
                recognizer.record(_audio_file)
            )

    @_updateRecaptchaFrames
    def _downloadAudioFile(self, audio_url: str) -> None:
        # Headers que serão passados na requisição.
        audio_request_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) "
                "Gecko/20100101 Firefox/78.0"
            ),
            "Host": "www.google.com",
            "Referer": "https://www.google.com/recaptcha/api2/bframe"
        }

        # Realizando requisição para url do audio e obtendo conteúdo.
        audio_content = _requests.get(
            url=audio_url,
            headers=audio_request_headers
        ).content

        # Retornando IO com o conteúdo binário que foi obtido.
        return _io.BytesIO(audio_content)

    @_updateRecaptchaFrames
    def _humanClickInRecaptchaAnchor(self):
        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        # Dando foco para a página principal.
        self._webdriver.switch_to.default_content()

        # Dando scroll até o elemento.
        self._webdriver._selenium_utils.scrollToElement(self._frame_box)

        # Dando foco para a caixa do reCAPTCHA.
        self._webdriver._selenium_utils.switchToFrame(
            frame_element=self._frame_box
        )

        # Clicando no botão de âncora do reCAPTCHA para tentar resolver.
        self._webdriver._selenium_utils.humanClick(
            element=self._webdriver.find_element_by_id(
                self._id["getAnchorButton"]
            )
        )

        if current_frame:
            self._webdriver._selenium_utils.switchToFrame(
                frame_element=current_frame
            )

    @_updateRecaptchaFrames
    def _recaptchaChallengeIsDisplayed(self):
        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        # Dando foco para a página inicial.
        self._webdriver.switch_to.default_content()

        # Obtendo se o elemento está sendo exibido.
        _is_displayed = self._webdriver.find_element_by_xpath(
            f'//div[div/iframe[@name="c-{self._frame_name}"]]'
        ).is_displayed()

        if current_frame:
            self._webdriver._selenium_utils.switchToFrame(
                frame_element=current_frame
            )

        return _is_displayed

    @_updateRecaptchaFrames
    def getState(self):
        # Definindo variável padrão caso nenhum IF executar.
        state = None

        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        ######################################################################
        # Definindo XPATHs para não exceder limites da PEP8 dentro do if/elif.
        ######################################################################
        _recaptcha_anchor_xpath = (
            f"//span[@id='{self._id['getAnchorButton']}']"
        )

        _recaptcha_expired_xpath = (
            f"{_recaptcha_anchor_xpath}"
            f"[contains(@class, '{self._class_name['recaptchaExpired']}')]"
        )

        _recaptcha_checked_xpath = (
            f"{_recaptcha_anchor_xpath}"
            f"[contains(@class, '{self._class_name['recaptchaChecked']}')]"
        )

        _recaptcha_unchecked_xpath = (
            f"{_recaptcha_anchor_xpath}"
            f"[contains(@class, '{self._class_name['recaptchaUnchecked']}')]"
        )

        _recaptcha_loading_xpath = (
            f"{_recaptcha_anchor_xpath}"
            f"[contains(@class, '{self._class_name['recaptchaLoading']}')]"
        )

        ######################################################################
        # Encurtando os métodos de pesquisa por elemento.
        ######################################################################
        _find_by_class_name = self._webdriver.find_elements_by_class_name
        _find_by_xpath = self._webdriver.find_elements_by_xpath

        # Enquanto o reCAPTCHA não houver algum estado.
        while not state:
            # Dando foco para o frame de desafios.
            self._webdriver._selenium_utils.switchToFrame(
                self._frame_challenge
            )

            # Se houver o desafio por imagem.
            if _find_by_class_name(self._class_name["imageChallenge"]):
                state = States.RECAPTCHA_IMAGE_CHALLENGE
            # Se houver o desafio por audio.
            elif _find_by_class_name(self._class_name["audioChallenge"]):
                state = States.RECAPTCHA_AUDIO_CHALLENGE

            # Dando foco para o frame da caixa do reCAPTCHA.
            self._webdriver._selenium_utils.switchToFrame(self._frame_box)

            # Se o reCAPTCHA estiver expirado.
            if _find_by_xpath(_recaptcha_expired_xpath):
                state = States.RECAPTCHA_EXPIRED
            # Se o reCAPTCHA estiver checkado.
            elif _find_by_xpath(_recaptcha_loading_xpath):
                state = States.RECAPTCHA_LOADING
            # Se o reCAPTCHA estiver checkado.
            elif _find_by_xpath(_recaptcha_checked_xpath):
                state = States.RECAPTCHA_CHECKED
            # Se o reCAPTCHA não estiver checkado.
            elif _find_by_xpath(_recaptcha_unchecked_xpath) and not state:
                state = States.RECAPTCHA_UNCHECKED

            # Dando foco para a página padrão.
            if current_frame:
                self._webdriver._selenium_utils.switchToFrame(current_frame)
            else:
                self._webdriver.switch_to.default_content()

        # Retornando estado do reCAPTCHA.
        return state

    @_updateRecaptchaFrames
    def hide(self):
        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        # Dando foco para a página principal.
        self._webdriver.switch_to.default_content()

        # Obtendo o reCAPTCHA atual pelo atributo 'name' e estilizando.
        self._webdriver.execute_script(
            f"document.getElementsByName('a-{self._frame_name}')[0].style."
            f"border = ''"
        )

        if current_frame:
            self._webdriver._selenium_utils.switchToFrame(current_frame)

    @_updateRecaptchaFrames
    def show(self):
        # Obtendo o frame atual.
        current_frame = self._webdriver._selenium_utils.getCurrentFrame()

        # Dando foco para a página principal.
        self._webdriver.switch_to.default_content()

        # Obtendo o reCAPTCHA atual pelo atributo 'name' e estilizando.
        self._webdriver.execute_script(
            f"document.getElementsByName('a-{self._frame_name}')[0].style."
            f"border = 'solid 2px #0f0'"
        )

        # Dando scroll para o elemento do reCAPTCHA.
        self._webdriver._selenium_utils.scrollToElement(self._frame_box)

        if current_frame:
            self._webdriver._selenium_utils.switchToFrame(current_frame)

    @_updateRecaptchaFrames
    def solve(self) -> Tuple[str, list]:
        # Verificando se o reCAPTCHA está solucionado.
        if self._checkRecaptchaIsChecked():
            # Retornando a resposta do reCAPTCHA.
            return self._getRecaptchaResponse()

        # Caso o reCAPTCHA esteja expirado ou não solucionado.
        _case_recaptcha_unchecked_or_expired = (
            (self.getState() == States.RECAPTCHA_UNCHECKED) or
            (self.getState() == States.RECAPTCHA_EXPIRED)
        )

        # Se o reCAPTCHA estiver expirado ou não solucionado.
        if (_case_recaptcha_unchecked_or_expired):
            # Dando foco para a acaixa do reCAPTCHA.
            self._webdriver._selenium_utils.switchToFrame(
                frame_element=self._frame_box
            )

            # Clicando no botão de âncora do reCAPTCHA.
            self._humanClickInRecaptchaAnchor()

            # Aguardando o modo desafio por imagem reCAPTCHA.
            self._waitFor(States.RECAPTCHA_IMAGE_CHALLENGE)

        # Se o reCAPTCHA estiver no modo de desafio por imagem.
        elif self.getState() == States.RECAPTCHA_IMAGE_CHALLENGE:
            # Dando foco para o frame de modo desafio.
            self._webdriver._selenium_utils.switchToFrame(
                frame_element=self._frame_challenge
            )

            # Se o modo desafio do reCAPTCHA estiver exibindo.
            if not self._recaptchaChallengeIsDisplayed():
                # Clicando no botão de âncora do reCAPTCHA.
                self._humanClickInRecaptchaAnchor()

            # Clicando no botão de desafio por audio para mudar o modo.
            self._webdriver._selenium_utils.humanClick(
                element=self._webdriver.find_element_by_id(
                    self._id["getAudioModeButton"]
                )
            )

            # Esperando o desafio por audio aparecer.
            self._waitFor(States.RECAPTCHA_AUDIO_CHALLENGE)

        # Se o reCAPTCHA estiver no modo de desafio por audio.
        elif self.getState() == States.RECAPTCHA_AUDIO_CHALLENGE:
            # Dando foco para o frame de modo desafio.
            self._webdriver._selenium_utils.switchToFrame(
                frame_element=self._frame_challenge
            )

            # Se o modo desafio do reCAPTCHA estiver exibindo.
            if not self._recaptchaChallengeIsDisplayed():
                # Clicando no botão de âncora do reCAPTCHA.
                self._humanClickInRecaptchaAnchor()

            try:
                # Realizando o download do audio do reCAPTCHA.
                audio_file = self._downloadAudioFile(
                    audio_url=self._webdriver.find_element_by_id(
                        self._id["getAudioDownloadLink"]
                    ).get_attribute("src")
                )

                # Realizando reconhecimento de voz e obtendo texto.
                recognited_text = self._getTextFromAudioFile(
                    audio_file=audio_file
                )

                # Obtendo o input do desafio do reCAPTCHA.
                audio_response_input = self._webdriver.find_element_by_id(
                    self._id["getAudioInput"]
                )

                # Clicando no input do desafio do reCAPTCHA.
                self._webdriver._selenium_utils.humanClick(
                    element=audio_response_input
                )

                # Digitando a resposta no input do desafio do reCAPTCHA.
                audio_response_input.send_keys(recognited_text)

                # Enviando a resposta.
                self._webdriver._selenium_utils.humanClick(
                    element=self._webdriver.find_element_by_id(
                        self._id["getAudioInputSubmit"]
                    )
                )

                # Esperando o estado do reCAPTCHA não ser mais modo audio.
                self._noWaitFor(
                    state=States.RECAPTCHA_AUDIO_CHALLENGE,
                    timeout=2
                )
            except (TimeoutException, _speech_recognition.UnknownValueError):
                self._webdriver._selenium_utils.humanClick(
                    element=self._webdriver.find_element_by_class_name(
                        self._class_name["reloadAudioLink"]
                    )
                )

        # Aguardando o Spinner do reCAPTCHA.
        self._waitRecaptchaSpinner()

        # Verificando se o reCAPTCHA está solucionado.
        if self._checkRecaptchaIsChecked():
            # Retornando a resposta do reCAPTCHA.
            return self._getRecaptchaResponse()
        else:
            # Retornando o foco para a página inicial.
            self._webdriver.switch_to.default_content()

            # Chamando este mesmo método para tentar solucionar.
            return self.solve()


class Bypass:
    # XPATH do elemento da caixa do recaptcha.
    _recaptcha_box_element_xpath = (
        "//iframe[contains(@src, 'recaptcha/api2/anchor')]")

    # XPATH do elemento dos desafios do recaptcha.
    _recaptcha_challenge_element_xpath = (
        "//iframe[contains(@src, 'recaptcha/api2/bframe')]"
    )

    def __init__(self, webdriver: object) -> None:
        # Definindo atributo privado com o WebDriver inserido.
        self._webdriver = webdriver

    def getRecaptchas(self):
        # Aguardando a página carregar.
        self._webdriver._selenium_utils.waitLoadPage()

        # Lista de caixas de Google reCAPCTHAs que foram encontrados.
        recaptcha_box_list = self._webdriver.find_elements_by_xpath(
            Bypass._recaptcha_box_element_xpath
        )

        # Obtendo o 'name' das caixas do reCAPTCHA.
        recaptcha_names = [
            e.get_attribute("name")[2:]
            for e in recaptcha_box_list
        ]

        # Container que armazenará as instâncias da classe ReCAPTCHA.
        container_recaptcha_instances = []

        # Iterando informações dos reCAPTCHAs.
        for recaptcha_name in recaptcha_names:
            # Criando instância de ReCAPTCHA para todos reCAPTCHAs da página.
            recaptcha_instance = ReCAPTCHA(self._webdriver, recaptcha_name)

            # Adicionando as informações do reCAPTCHA ao cache container.
            _cache_addition = ReCAPTCHACache.add_to_cache(
                (recaptcha_name, recaptcha_instance)
            )

            # Adicionando a instância ao container de instâncias.
            container_recaptcha_instances.append(
                _cache_addition if _cache_addition else recaptcha_instance
            )

        return container_recaptcha_instances


# Verificando se o projeto local está desatualizado.
# ProjectVersion.verifyModuleVersion()
