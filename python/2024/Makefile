.PHONY: all
all: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-run)

.PHONY: pypy
pypy: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-pypy)

.PHONY: time
time: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-time)

.PHONY: pypy-time
pypy-time: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-pypy-time)

.PHONY: day-%
day-%: run.py %/go.py %/test*.txt ../inputs/%.txt
	/usr/bin/time python3 run.py -t $*
	/usr/bin/time python3 run.py $*

.PHONY: day-%-run
day-%-run: run.py %/go.py ../inputs/%.txt
	python3 run.py $*

.PHONY: day-%-pypy
day-%-pypy: run.py %/go.py ../inputs/%.txt
	pypy3 run.py $*

.PHONY: day-%-time
day-%-time: run.py %/go.py ../inputs/%.txt
	/usr/bin/time python3 run.py $*

.PHONY: day-%-pypy-time
day-%-pypy-time: run.py %/go.py ../inputs/%.txt
	/usr/bin/time pypy3 run.py $*

.PHONY: clean
clean:
	rm -rf *~ */*~ */__pycache__


