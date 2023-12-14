# Tool to BruteForce the LoginPage of DVWA

## a) Installation

```
git clone https://github.com/RedZNouggy/PyProjects.git
mv PyProjects/Cyber/DVWA/ ./
sudo rm -r PyProjects/
cd DVWA/
pip install -r requirements.txt
chmod +x ./main.py
```
![image](https://github.com/RedZNouggy/PyProjects/assets/81537743/82fcfada-3280-4af7-b1c5-33fd758051f2)
## b) Launch the script

```
# For a classic utilisation on http :
main.py --web-ip "<IP>" --file-path <PATH-TO-PASSWORD-LIST> --php-session-id <PHPSESSID> --http

# For classic utilisation on https : 
main.py --web-ip "<IP>" --file-path <PATH-TO-PASSWORD-LIST> --php-session-id <PHPSESSID> --https

# For more info (on http) :
main.py --web-ip "<IP>" --file-path <PATH-TO-PASSWORD-LIST> --php-session-id <PHPSESSID> --http --verbose

For all info (on http) :
main.py --web-ip "<IP>" --file-path <PATH-TO-PASSWORD-LIST> --php-session-id <PHPSESSID> --http --vverbose

```
