## Generation of the Argumentative Knowledge Graph (CORD19-AKG)


#### Preprocessing:
Processes a directory with JSON files and selects documents which contain an abstract. The selected files are merged in multiple batch files to be able to run the pipeline in parallel. To run the preprocessing execute the following command:

```
$ python3 preprocessing.py
```

Adjust the path to the data folder if needed (default: "./data/v7/").

#### ACTA pipeline:

Install the requirements in a Python 3.7 environment:

```
$ pip install -r requirements.txt
```

Download and extract the models into the model directory. You can download the pre-trained models[here](https://covid19.i3s.unice.fr/~team/acta_models.zip).


Run the pipeline:

```
$ ./run_pipeline.sh
```
