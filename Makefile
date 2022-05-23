
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
	DATE=$(shell date +%Y.%m.%d)
	sed -i "s/__UNRELEASED_VERSION__/$(DATE)/g" indascope.py
	# make build
	sed -i "s/$(DATE)/__UNRELEASED_VERSION__1/g" indascope.py
	gh release create -n '' -t indascope_$(DATE) $(DATE) dist/indascope 

install: 
	sudo rm -rf /usr/bin/indascope
	sudo cp dist/indascope /usr/bin/indascope

	
.PHONY: build
