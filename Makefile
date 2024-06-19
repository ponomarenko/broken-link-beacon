# define the name of the virtual environment directory
VENV := venv

ifeq ($(OS),Windows_NT)
	WIN		:= true
	PYTHON	:= py
	PIP		:= $(VENV)/Scripts/pip
else
	PYTHON 	:= python3
	PIP		:= $(VENV)/bin/pip
endif


# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = setup clean

# Defining an array variable
FILES = input output

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = setup

setup: 
	${PYTHON} -m venv $(VENV)	
	$(PIP) install -r requirements.txt

clean:
ifdef WIN
	rmdir /S /Q $(VENV)
else
	rm -rf $(VENV)
endif
