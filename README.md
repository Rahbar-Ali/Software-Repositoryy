# Git Repository Analyzer

A Program to analyze a Git Repository and collect Information about its commits, test classes and test methods. It outputs the number of Test classes and Methods per commit, along with a list of the Test Classes and Methods. The Script takes in the directory of the git directory and the root folder of the Java File

# Getting Started

## Prerequises
* Python 3.x
* Git
* argparse
* Cloned git repository

## Usage
* python software_repository.py -- directory [directory] --root_folder [root_folder]
* git clone https://github.com/username/repository.git

Please Replace **'[directory]'** with the directory of the Git repository and **'[root_folder]'** with the root_folder of the Java files.
The script outputs the result to **'[output.json]'** in the current directory
First you need to clone Git Repository to your computer

## Output
The Program will produce a file named **'output,json'** in the same directory as the program, containing the following information:

* Location of the repository
* Total number of commits
* Test of Commits:
  * Commits
  * Number of test classes
  * Number of test methods
  * List of test classes
  * List of test methods
* time taken per commit

# Note
* Make sure that directory and root_folder is correctly specified.
* This scripte requires Python 3 and **'argparse'** module. 
