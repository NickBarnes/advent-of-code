.PHONY: py
py: $(foreach day,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),py-$(day)-run)

.PHONY: pypy
pypy: $(foreach day,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),pypy-$(day))

.PHONY: py-time
py-time: $(foreach day,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),py-$(day)-time)

.PHONY: pypy-time
pypy-time: $(foreach day,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),pypy-$(day)-time)

.PHONY: py-%
py-%: python/run.py python/%/go.py test/%*.txt input/%.txt
	/usr/bin/time python3 python/run.py -t $*
	/usr/bin/time python3 python/run.py $*

.PHONY: py-%-run
py-%-run: python/run.py python/%/go.py input/%.txt
	python3 python/run.py $*

.PHONY: pypy-%
pypy-%: python/run.py python/%/go.py input/%.txt
	pypy3 python/run.py $*

.PHONY: py-%-time
py-%-time: python/run.py python/%/go.py input/%.txt
	/usr/bin/time python3 python/run.py $*

.PHONY: pypy-%-time
pypy-%-time: python/run.py python/%/go.py input/%.txt
	/usr/bin/time pypy3 python/run.py $*

.PHONY: clean
clean:
	rm -rf *~ */*~ */*/*~ */__pycache__ */*/__pycache__


