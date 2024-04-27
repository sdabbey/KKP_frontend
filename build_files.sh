python3.8 -m pip install -r requirements.txt
python3.8 manage.py collectstatic 
python3.8 manage.py makemigrations 
python3.8 manage.py migrate 