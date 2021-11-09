# axie_breed

createdb.py : Creates database instance and table with schema ||
fetch&load.py : Fetches data from API, sanitizes and loads into db table

## Development

Python build setup for creating python modules to be installed in a conda environment.

This setup uses Miniconda for creating conda environment. You can download an oppropriate version from here: https://docs.conda.io/en/latest/miniconda.html

Development Requirements are in the environment_dev.yml file for environment setup in miniconda.

## Versioning 

Versioning is handled by using the python package `pbr`. When starting a development feature/hotfix branch be sure to update the git tag version by using `git tag -a v*.*.* -m "tagging message"`, have to change `*` for the correct version in github. you can also add a lightweight tag by not using the -a or -m options like `git tag v.*.*.*`. Also there are options for tagging older commits with git if needed. 