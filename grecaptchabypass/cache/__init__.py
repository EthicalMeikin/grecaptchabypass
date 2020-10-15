from typing import Tuple

"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""


class ReCAPTCHACache:
    _cache = []
    maxsize = 100

    @classmethod
    def clear_cache(cls):
        # Removendo todo itens da lista do cache.
        self.cache.clear()

    @classmethod
    def add_to_cache(cls, recaptcha_information: Tuple[Tuple, object]):
        # Removendo primeiro item caso o cache atingir o limite de tamanho.
        if len(cls._cache) > cls.maxsize:
            cache.pop(0)

        # Iterando os itens do cache.
        for cache_info in cls._cache:
            # Se a informação atual do cache for a mesma que passei.
            if cache_info[0] == recaptcha_information[0]:
                # Retornando a instância do reCAPTCHA que estava armazenada.
                return cache_info[1]

        # Senão, adicionando informação no cache.
        cls._cache.append(recaptcha_information)
