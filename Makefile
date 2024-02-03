run:
	python3 test.py

venv:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

run: venv
	python test.py