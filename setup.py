from setuptools import setup, find_packages

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile["packages"], r=False)
test_requirements = convert_deps_to_pip(pfile["dev-packages"], r=False)

setup(
    name="williamhammond",
    packages=find_packages(),
    version="1.0.0",
    description="A Starcraft 2 Bot",
    license="MIT",
    author="William Hammond",
    author_email="william.t.hammond@gmail.com",
    url="https://github.com/williamhammond/cheesebot",
    keywords=["StarCraft", "StarCraft 2", "StarCraft II", "AI", "Bot"],
    setup_requires=["pipenv"],
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
