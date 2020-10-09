"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

from .main import (
    Bypass, getBrowserFirefox, ReCAPTCHA, States
)


# Lista de objetos que serão escondidos.
__exclude__ = [
    "lib", "main", "utils", "cache", "exceptions"
]


# Escondendo alguns objetos do dir() para não causar confusão na leitura.
def __dir__():
    return [x for x in list(globals().keys()) if x not in __exclude__]
