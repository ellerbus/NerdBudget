# Nerd Budget

## Setup Notes for Development Initialization

```ps1
# cd to highlander-console
py -m venv ./env

# Start/Active virtual environment
./env/scripts/activate.ps1

# upgrade pip
py -m pip install --upgrade pip

# install dependencies
pip install -r requirements.txt

# run the server
py .\nerdbudget\manage.py runserver

# dev notes - create fixture files
py .\nerdbudget\manage.py dumpdata --exclude auth > data.json
py .\nerdbudget\manage.py loaddata data.json

```

## Setup Notes for django

```ps1
cd ./nerdbudget/

py ./manage.py makemigrations

py ./manage.py migrate

```


If VS Code needs a nudge `ctrl+shift+P` Python Discover Tests
