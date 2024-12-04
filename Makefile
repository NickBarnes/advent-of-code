.PHONY: py-all
py-all: $(foreach dir,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),py-day-$(dir)-run)

.PHONY: pypy
pypy: $(foreach dir,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),py-day-$(dir)-pypy)

.PHONY: py-time
py-time: $(foreach dir,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),py-day-$(dir)-time)

.PHONY: pypy-time
pypy-time: $(foreach dir,$(sort $(patsubst python/%,%,$(wildcard python/[012]*))),pypy-day-$(dir)-time)

.PHONY: py-day-%
py-day-%: python/run.py python/%/go.py python/%/test*.txt input/%.txt
	/usr/bin/time python3 python/run.py -t $*
	/usr/bin/time python3 python/run.py $*

.PHONY: py-day-%-run
py-day-%-run: python/run.py python/%/go.py input/%.txt
	python3 python/run.py $*

.PHONY: pypy-day-%
pypy-day-%: python/run.py python/%/go.py input/%.txt
	pypy3 python/run.py $*

.PHONY: py-day-%-time
py-day-%-time: python/run.py python/%/go.py input/%.txt
	/usr/bin/time python3 python/run.py $*

.PHONY: pypy-day-%-time
pypy-day-%-time: python/run.py python/%/go.py input/%.txt
	/usr/bin/time pypy3 python/run.py $*

.PHONY: clean
clean:
	rm -rf *~ */*~ */*/*~ */__pycache__ */*/__pycache__


