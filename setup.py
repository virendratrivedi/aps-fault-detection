from setuptools import find_packages,setup

def get_requirements():
    pass


setup(
    name="sensor",
    version="0.0.1",
    author="Arpit Trivedi",
    author_email="trivedi.virendra2685mmi@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)