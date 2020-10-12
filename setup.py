# Bibliotecas nativas.
import os
import re
import setuptools


def readFile(filepath: str) -> str:
    # Caminho relativo do projeto.
    RELATIVE_PATH = os.path.abspath(os.path.dirname(__file__))

    # Caminho do arquivo.
    FILE_PATH = os.path.join(RELATIVE_PATH, filepath)

    # Abrindo e lendo arquivo README.
    with open(FILE_PATH, "r", encoding="utf8") as _file:
        return re.sub("</?(link|center)[^>]*>", "", _file.read())


# Lendo arquivo README.md.
README_CONTENT = readFile("README.md")

# Abrindo {requirements.txt}, lendo e obtendo bibliotecas.
REQUIREMENTS = filter(lambda x: x, readFile("requirements.txt").splitlines())

setuptools.setup(
    name="grecaptchabypass",
    version="1.0.0",
    description="Quebre múltiplos Google reCAPTCHAs de uma página.",
    long_description=README_CONTENT,
    long_description_content_type="text/markdown",
    url="https://github.com/EthicalMeikin",
    author="EthicalMeikin",
    license="GPL-3.0",
    keywords=[
        "Google reCAPTCHA bypass",
        "Google reCAPTCHA breaker"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=list(REQUIREMENTS),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework :: Tool",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
