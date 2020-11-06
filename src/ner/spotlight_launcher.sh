#!/bin/bash
# install DBpedia Spotlight nightly build https://sourceforge.net/projects/dbpedia-spotlight/files/spotlight/dbpedia-spotlight-nightly-build.ja$

# path to DBpedia Spotlight
cd $1

# check if second argument is true to install th different models
if [[ $2 = true ]] ;
then
    wget https://downloads.dbpedia.org/repo/dbpedia/spotlight/spotlight-model/2020.03.11/spotlight-model_lang%3den.tar.gz
    wget https://downloads.dbpedia.org/repo/dbpedia/spotlight/spotlight-model/2020.03.11/spotlight-model_lang%3dde.tar.gz
    wget https://downloads.dbpedia.org/repo/dbpedia/spotlight/spotlight-model/2020.03.11/spotlight-model_lang%3dfr.tar.gz
    wget https://downloads.dbpedia.org/repo/dbpedia/spotlight/spotlight-model/2020.03.11/spotlight-model_lang%3des.tar.gz
    wget https://downloads.dbpedia.org/repo/dbpedia/spotlight/spotlight-model/2020.03.11/spotlight-model_lang%3dit.tar.gz

    tar -zxvf spotlight-model_lang=en.tar.gz
    tar -zxvf spotlight-model_lang=de.tar.gz
    tar -zxvf spotlight-model_lang=fr.tar.gz
    tar -zxvf spotlight-model_lang=es.tar.gz
    tar -zxvf spotlight-model_lang=it.tar.gz

    rm -zxvf spotlight-model_lang=en.tar.gz
    rm -zxvf spotlight-model_lang=de.tar.gz
    rm -zxvf spotlight-model_lang=fr.tar.gz
    rm -zxvf spotlight-model_lang=es.tar.gz
    rm -zxvf spotlight-model_lang=it.tar.gz
fi

java -Xmx20G -jar dbpedia-spotlight-nightly-build.jar en http://localhost:2222/rest &
java -Xmx10G -jar dbpedia-spotlight-nightly-build.jar de http://localhost:2223/rest &
java -Xmx10G -jar dbpedia-spotlight-nightly-build.jar fr http://localhost:2224/rest &
java -Xmx10G -jar dbpedia-spotlight-nightly-build.jar es http://localhost:2225/rest &
java -Xmx10G -jar dbpedia-spotlight-nightly-build.jar it http://localhost:2226/rest &
