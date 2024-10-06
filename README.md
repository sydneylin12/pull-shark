# pull-shark
Pulling shark do-do-do-do-do-do!

This project will help you boost Github achievements. There are two scripts:
1. `pull-shark.py` - Creates an automated PR and merges it.
2. `issues.py` - Creates and answers an issue across 2 different GH accounts.

# Setup
1. Install python 3 and `pip`.
    - Note: I need to use `pip3` on the command line to install.
2. Create a github API token with read/write access.
3. Create a python virtual environment.
```
$ python3 -m venv ./
```
4. Install requirements.
```
$ pip3 install -r requirements.txt
```
5. Add env variables to `~/.zshrc`.
```
export GITHUB_TOKEN="<GH TOKEN FOR ACCOUNT 1>"
export SECOND_GITHUB_TOKEN="<GH TOKEN FOR ACCOUNT 2>"
```
6. Run scripts.
```
$ python3 pull-shark.py
$ python3 issues.py
```