https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe
extract and copy in H:\Program Files (x86)\Python
add H:\Program Files (x86)\Python\python-3.6.0-embed-amd64 in PATH


# Windows
# You can also use py -3 -m venv .venv
py -m venv .venv
.venv\scripts\activate

# This shell command will export the dependencies as a file named requirements.txt:
pip freeze > requirements.txt
pip install -r requirements.txt