# Augmentation of the data related to the CovidOnTheWeb dataset

To configure the paths, endpoints and API keys edit the file:
- covidontheweb_aug/utils/config.py

To create a virtual environment under Anaconda 3 and run it:
- conda create -n {envname}
- conda activate {envname}

To build and install the package:
- python3 setup.py install
- or python3 setup.py develop

Then run the command to retrieve the links associated to the named entities and PICO elements:
- python3 covidontheweb_aug/script/main.py


# Due to the limitations of Wikidata and DBpedia SPARQL endpoints, it is recommended to launch your own endpoint of these two knowledge bases

Install DBpedia :
- You first need to install docker and docker-compose.
- Then clone and install https://github.com/dbpedia/Dockerized-DBpedia.
- Modify virtuoso.ini according to the capabilities of your system, file virtuoso.ini (path Dockerized-DBpedia/virtuoso-db/virtuoso.ini).
- Adapt the resources you need from the DBpedia Databus by modifying the file docker-compose.yml, section COLLECTION_URI (depending on your needs you will have to create a collection first, we prepared a light version of DBpedia available at https://databus.dbpedia.org/rgazzott/collections/dbpedia-linksets).

Install Wikidata :
- Follow the instructions on https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#Standalone_service to download and prepare the resources from Wikidata (https://dumps.wikimedia.org/wikidatawiki/entities/).
- The preparation of the resources with the munge.sh script may require that you modify the paths.
- Then, instead of launching a Blazegraph database, put your different .gz files in the downloads folder of the Dockerized-DBpedia project (a Virtuoso database loads triplets much faster than a Blazegraph database).

Once this is done, you will just have to run the script dockerized-dbpedia.sh, the process of setting up the local endpoints takes several days.

After that you will probably want to execute your SPARQL queries in parallel. To do this, modify the PARALLELISM option (Boolean) in covidontheweb_aug/utils/config.py
