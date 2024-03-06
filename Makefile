run:
	python3 data_cleaning.py

venv:
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

run: venv
	python data_cleaning.py