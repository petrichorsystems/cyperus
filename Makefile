all: check-and-reinit-submodules modules/cyperus-server/build/cyperus-server env/pyvenv/bin/activate

check-and-reinit-submodules:
	@if git submodule status | egrep -q '^[-+]' ; then \
		echo "INFO: Need to reinitialize git submodules"; \
		git submodule update --init; \
	fi

modules/cyperus-server/build/cyperus-server: check-and-reinit-submodules
	cd modules/cyperus-server && make

env/pyvenv/bin/activate: check-and-reinit-submodules
	mkdir -p env/ && python -m venv env/pyvenv && source env/pyvenv/bin/activate && pip3 install --upgrade pip && pip3 install -r modules/baton/requirements.txt && pip3 install -r modules/pycyperus/requirements.txt

pycyperus.egg-info: env/pyvenv/bin/activate:
source env/pyvenv/bin/activate && cd modules/pycyperus/ && python3 setup.py install 

clean:
	rm -rf env
	cd modules/cyperus-server && make clean
