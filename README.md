# prmt


### Description

Simple and robust command line prompts for most of the values.
The formatting of the questions and prompts is completely customizable.
This lib has no dependencies and no magic.

**Features:**

* Prompt bool from user. (`prmt.confirm`)
* Prompt string from user. (`prmt.string`)
* Prompt string from user, opening an editor window. (`prmt.string_from_editor`)
* Prompt integer from user. (`prmt.integer`)
* Prompt list of strings from user. (`prmt.list_of_str`) 
* Prompt user to select an item from a list/dict of items. (`prmt.select`)

**Optional features:**

* Set default values.
* Customize formatting for each prompt. 
* Customize formatting for all prompts via the `prmt.Prompt()` class.
* Open default Text Editor for the user to enter text.
* Blacklist values. (If the user enters blacklisted values she will be prompted again)


### Requirements

Python `>=3.7`


### Install

    pip install prmt

or

    poetry install prmt


### Examples

Look into the `tests` folder for code examples.

To see it in action on the command line, run:

    pipenv run python make.py test



### Development

    git clone https://github.com/feluxe/prmt.git

    cd prmt

    pipenv install --dev --pre

    pipenv run python make.py --help

