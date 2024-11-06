all: modules/cyperus-server/build/cyperus-server env/pyvenv/bin/activate

modules/cyperus-server/build/cyperus-server:
	cd modules/cyperus-server && make

env/pyvenv/bin/activate:
	mkdir -p env/ && python -m venv env/pyvenv && source env/pyvenv/bin/activate && pip3 install --upgrade pip && pip3 install -r modules/baton/requirements.txt && pip3 install -r modules/pycyperus/requirements.txt

clean:
	rm -rf env
	cd modules/cyperus-server && make clean
