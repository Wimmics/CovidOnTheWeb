# Augmentation of the data related to the CovidOnTheWeb dataset

Command to launch Corese-server ([documentation](https://github.com/Wimmics/corese/wiki/CORESE-server) and [compiled versions](https://project.inria.fr/corese/download/)):
- java -Xmx{size}m -jar corese-server-{version}.jar -p 2500

To configure the paths and endpoints, edit the file:
- covidontheweb_aug/utils/config.py

To create a virtual environment under Anaconda 3 and run it:
- conda create -n {envname}
- conda activate {envname}

To build and install the package:
- python3 setup.py install
- or python3 setup.py develop

Then run the command to retrieve the links associated to the named entities and PICO elements:
- python3 covidontheweb_aug/script/main.py
