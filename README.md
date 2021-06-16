# ObsidianNLPScript
Memex II - Knowledge Creation Through Association
Personal knowledge bases have been a topic of discussion amongst researchers for decades. Creating a consultable and dynamic tool for knowledge creation has been a goal of many researchers throughout the last century. Through the advent of newer technologies I believe a proper interface for a knowledge base is finally possible. This repo attempts to integrate Natural language processing through NLTK and Gensim ptyon libraries and a third party app "Obsidian" to create a Memex, as coined by Vannevar Bush in 1945.

These instructions will get you a copy of the project up and running on your local machine for testing and research purposes.

Prerequisites:
The latest stable versions of the following:
Obsidian - https://obsidian.md/
Obsidian lives and works within a folder of exclusively markdown files. You can check out their documentation, but as a pre-requisite your files will also need to be in proper markdown format. 
Python - https://www.python.org/downloads/
I think you can get this from the windows store if you're running windows, but I always have a bad time with anything related to the windows store. I recommend installing it manually. 

The following Python Libraries installed:

use the following command to install each of the libraries:

python -m pip install (packageName)

nltk
gensim
pickle
spacy

Here is a complete list of all libraries that are used, in case you run into any troubles:
os, nltk, gensim, random, pickle, spacy, shutil

in the 'StableScriptBackup' folder of the repo, there will be a python script labelled
"MarkDownTagger.py"

Open this file using the rich text editor of your choice. Notepad++ will do fine, but I prefer Visual Studio Code.
Once you are in the file, set the path variable to the path of your obsidian file folder. 
Now, before running the python script, ensure you back up your obsidian file folder. 
The python script will attempt to read and edit every file in the folder structure. 

I recommend keeping the python script in a file of it's own, as it spawns a few support files in whatever file it lives in.

Now, navigate to the folder in the command line interface of your choice, and use the command 'py MarkDownTagger.py' to have the script find tags and associations automatically for your files.  

Congratulations! You now have a functioning prototype of a Memex as I have written about in my paper
"Memex II - Knowledge Creation Through Association"

Authors
Dustin Smith

