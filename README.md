# download

git clone git@github.com:ClemGRob/pyrebaseIAScan.git
or
git clone https://github.com/ClemGRob/pyrebaseIAScan.git
cd pyrebaseIAScan


# setup env

python3.8 -m venv .venv
on linux : 
    source .venv/bin/activate
on windows : 
    activate .venv/bin/activate
pip install --upgrade pip wheel setuptools requests
pip install -r requirements.txt
pip uninstall pycryptodome -y
pip install -U pycryptodome

# configuraton
get your project config and put it inside config/Pyrebase_config.py (replace pirebaseConfig variable content with yours)
