# trading_bot

# erstellen eines virtuellen environments für deine pakete:
python3 -m venv venv_name

# deaktivieren von dem virtuellen env
deactivate


# benutzen / aktivieren
source venv_name/bin/activate

"requirements.txt" erstellen

# dotenv install
pip install python-dotenv

# Um pakete backupen
pip freeze > requirements.txt

# Um pakete dann von dort zu installieren
pip install -r requirements.txt

# Pakete runterladen
python3 -m pip install python-binance

# http Server erstellen
ngrok http 80

# Funktion mit payload in localhost probieren:
gunicorn app:app



