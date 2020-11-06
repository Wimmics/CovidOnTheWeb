# Generation of the Named Entity files used for the CORD19-NEKG dataset
**WARNINGS:** 
- **The progress bar is broken in this version, it just gives an idea of when a task is finished.**
- **Some files are not processed by DBpedia Spotlight, we need to investigate the problem that is not encountered by other annotators.**
- **We rely on the [pycld2 package](https://github.com/aboSamoor/pycld2) for language detection which currently excludes Windows support.**

****

Command to launch DBpedia Spotlight ([jar available](https://sourceforge.net/projects/dbpedia-spotlight/files/)):
- To install the models and launch Spotlight (you need to install DBpedia Spotlight first): spotlight_launcher.sh path true
- To just launch spotlight: spotlight_launcher.sh

Command to launch Entity-fishing ([installation guide](https://nerd.readthedocs.io/en/latest/build.html)):
- ./gradlew appRun

Download and unzip the [CORD-19 corpus](https://www.semanticscholar.org/cord19).

To configure the paths, endpoints and API keys, options (True or False), edit the file:
- cord19_ner/utils/config.py

To create a virtual environment under Anaconda 3 and run it:
- conda create -n {envname}
- conda activate {envname}

To build and install the package (Python >= 3.6):
- python3 setup.py install
- or python3 setup.py develop

Then run the command to extract the named entities:
- python3 cord19_ner/script/main_threading.py
