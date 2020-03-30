## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed.
2. Install [pipenv](https://github.com/kennethreitz/pipenv).

```
$ pip install pipenv
```
3. Install requirements  
```
$ pipenv install
```

4. Run the server:
    * `$ pipenv run python api.py -p 5000 -a 5000`
    * `$ pipenv run python api.py -p 5001 -a 5000`
    * `$ pipenv run python api.py -p 5002 -a 5000`
```    
5.Run the cli:
    * $ pipenv run python cli.py {port}`
