"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

from ..lib import (
    _selenium, _time
)

from typing import Tuple
import PIL.Image


class _KeepCurrentFrame:
    def __init__(self, utils: object):
        self.utils = utils

    def __enter__(self):
        # Salvando o frame atual.
        self.current_frame = self.utils.getCurrentFrame()

    def __exit__(self, *others):
        # Voltando para o frame anterior (ex-atual).
        if self.current_frame:
            self.utils.switchToFrame(self.current_frame)
        else:
            self.utils._webdriver.switch_to.default_content()


class SeleniumUtils:
    def __init__(self, webdriver: object):
        # Definindo atributo privado com o WebDriver passado.
        self._webdriver = webdriver

        # Atributo que irá armazenar os frames e seus nomes.
        self._frames_database = {}

    def addFrameToDatabase(self, frame_element: object):
        # Adicionando o frame atual no banco de dados.
        self._frames_database[self.getFrameName()] = frame_element

    def getCurrentFrame(self) -> str:
        # Obtendo o nome do frame atual.
        frame_name = self.getFrameName()

        # Verificando se o nome do frame atual existe no banco de dados.
        if frame_name in self._frames_database:
            # Retornando o elemento do frame que está no banco de dados.
            return self._frames_database[frame_name]

    def getCurrentViewportSize(self) -> Tuple[int, int]:
        # Obtendo tamanho do viewport com JavaScript.
        return tuple(self._webdriver.execute_script(
            "return [window.innerWidth, window.innerHeight]"
        ))

    def getElementCenterPosition(self, element: object) -> Tuple[float, float]:
        # Obtendo o tamanho do viewport.
        viewport_width, viewport_height = self.getCurrentViewportSize()

        # Obtendo posição do elemento.
        element_posy, element_posx = element.location.values()

        # Tamanho do elemento divido pela metade (width/2 & height/2).
        element_height, element_width = map(
            lambda x: x / 2, element.size.values()
        )

        # Somando posições do elemento com a metade do tamanho do elemento.
        element_posy += element_width\
            if element_width < viewport_width else viewport_width

        element_posx += element_height\
            if element_height < viewport_height else viewport_height

        # Retornando a posição do centro do elemento.
        return element_posx, element_posy

    def getFrameName(self) -> str:
        # Retornando o nome do frame atual utilizando JavaScript.
        return self._webdriver.execute_script("return window.name")

    def getReadyState(self):
        # Retornando o estado da página.
        return self._webdriver.execute_script("return document.readyState")

    def humanClick(self, element: object, additional_x=0, additional_y=0):
        # Definindo cadeia de ações.
        action_chains = _selenium.webdriver.common.action_chains.ActionChains(
            driver=self._webdriver
        )

        with self.keepCurrentFrame():
            # Obtendo a posição do centro do elemento.
            element_posx, element_posy = self.getElementCenterPosition(
                element=element
            )

            element_posx += additional_x
            element_posy += additional_y

            # Dando foco para a página principal.
            self._webdriver.switch_to.default_content()

            # Ações que farão o mouse se mover na tela.
            action_chains.move_by_offset(element_posy, element_posx)
            action_chains.move_by_offset(0, 0)

            # Executando as ações armazenadas.
            action_chains.perform()

            # Resetando as ações da cadeia de ações.
            action_chains.reset_actions()

        # Clicando no elemento.
        element.click()

    def scrollTo(self, posx: float, posy: float):
        # Executando JavaScript na página para rolar.
        self._webdriver.execute_script(
            f"window.scrollTo({posx}, {posy})"
        )

        # Pequeno delay para esperar a página rolar.
        _time.sleep(0.1)

    def scrollToElement(self, element: object):
        posx, posy = element.location.values()
        self.scrollTo(posx, posy-(self.getCurrentViewportSize()[1]//2))

    def switchToFrame(self, frame_element: object,
                      from_initial_content=True):
        # Se {from_initial_content=True}.
        if from_initial_content:
            # Dando foco para o documento inicial da página.
            self._webdriver.switch_to.default_content()

        # Dando foco para o frame especificado.
        self._webdriver.switch_to.frame(frame_element)

        # Adiciona no banco de dados o elemento frame especificado.
        self.addFrameToDatabase(frame_element)

    def keepCurrentFrame(self):
        return _KeepCurrentFrame(self)

    def waitLoadPage(self):
        # Aguardando a página carregar.
        while self._webdriver._selenium_utils.getReadyState() != "complete":
            _time.sleep(0.01)
