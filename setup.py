from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME='requirements.txt'
HYPEN_E_DOT='-e .'

def get_requirements()->List(str):
    with open(REQUIREMENT_FILE_NAME) as requirements_file:
        requirnment_list=requirements_file.readlines()
        [requirement_name.replace('\n', '') for requirement_name in requirnment_list]
        if HYPEN_E_DOT in requirnment_list:
            requirnment_list.remove(HYPEN_E_DOT)
        return requirnment_list    
    


setup(
    name="sensor",
    version="0.0.1",
    author="Arpit Trivedi",
    author_email="trivedi.virendra2685mmi@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)