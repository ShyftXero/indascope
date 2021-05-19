
clean:
	rm -rf dist build

develop:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt 

build:
	pyinstaller indascope.spec --distpath='dist'


install: 
	sudo ln -s ${PWD}/dist/indascope /usr/bin/indascope

	
.PHONY: build