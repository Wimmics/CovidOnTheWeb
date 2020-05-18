Command to launch DBpedia Spotlight (models and jar available at https://sourceforge.net/projects/dbpedia-spotlight/files/):
java -Xmx{size}m -jar dbpedia-spotlight.jar en http://localhost:2222/rest
or java -Xmx{size}m -jar dbpedia-spotlight-nightly-build.jar en http://localhost:2222/rest

Command to launch Entity-fishing (installation guide available at https://nerd.readthedocs.io/en/latest/build.html):
mvn clean jetty:run

Download and unzip the CORD-19 corpus.

To configure the paths, endpoints and api keys, edit the file:
cord19_ner/utils/config.py

Edit the options in the file (True or False):
cord19_ner/script/main_threding.py

To create a virtual environment under Anaconda 3 and run it:
conda create -n {envname}
conda activate {envname}

To build and install the package: python3 setup.py install
                                  or python3 setup.py develop

Then run the command to extract the named entities:
python3 main_threading.py
