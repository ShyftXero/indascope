the_date := $(shell date +%Y.%m.%d)

clean:
	rm -rf dist build

develop:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt 

build:
	#indascope.py 
	pyinstaller indascope.spec --distpath='dist'

release:
	sed -i "s/__UNRELEASED_VERSION__/${the_date}/g" indascope.py
	# make build
	sed -i "s/${the_date}/__UNRELEASED_VERSION__/g" indascope.py
	gh release create -n '' -t indascope_${the_date} ${the_date} dist/indascope 

install: 
	sudo rm -rf /usr/bin/indascope
	sudo cp dist/indascope /usr/bin/indascope

	
.PHONY: build
