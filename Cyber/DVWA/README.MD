# Tool to BruteForce the LoginPage of DVWA

## a) Installation

```
git clone https://github.com/RedZNouggy/PyProjects.git
mv PyProjects/Cyber/DVWA/ ./
sudo rm -r PyProjects/
cd DVWA/
pip install -r requirements.txt
```

## b) Launch the script

```
main.py -ip "<IP>" -f <PATH-TO-PASSWORD-LIST> --http --php-session-id <PHPSESSID> --verbose
```
