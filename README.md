# Git Repository Analyzer

A Program to analyze a Git Repository and collect Information about its commits, test classes and test methods.

## Requirements
* Python 3.x
* Cloned git repository

## Usage
* python software_repository.py [repo_path]
* git clone https://github.com/username/repository.git

Where **'[repo_path]'** is the file path to the Git repository you want to analyze. Replace **'username'** with the username of the repository owner, and **'repository'** with the name of repository you want to clone. 
First you need to clone Git Repository to your computer

## Output
The Program will produce a file named **'output,json'** in the same directory as the program, containing the following information:

* Location of the repository
* Total number of commits
* Information about each commits:
  * Commits
  * Number of test classes
  * Number of test methods
  * List of test classes
  * List of test methods

# Assumptions 

1. The program assumes that the Git repository is valid and that required softwares **'(Python,)'** is installed on your system
2. We assumes that the person  writing test classes and methods follows best code practices meaning, they will always includes the string "Test" in the java filename which contains Test classes
3. We also assumes that the person writing classes and methods follows recommanded style because we are searching for strings and matching them to classes and methods name

# Note
* Make sure that a file path to the repository is correctly specified. If path is incorrect or the repository does not exist, program will produce an error
* This scripte requires Python 3 and **'argparse'** module. No additional libraries are needed.
