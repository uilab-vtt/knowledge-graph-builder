Knowledge Graph Builder
=======================

This is a Python application that allows users to create 
and manage Knowledge Graph for a video file. 

## How to use

Before following the instruction below, 
please make sure to install Python 3 on your environment. 

### Set up

#### Setting up virtual environment

Set up Python3 virtual environment to install dependencies.

```bash
knowledge-graph-builder$ python3 -m venv ./env
```

#### Activate the virtual environment

Activate your virtual environment for Python.

```bash
knowledge-graph-builder$ source ./env/bin/activate
```

#### Install dependencies

Install Python dependencies.

```bash
(env)knowledge-graph-builder$ pip install -r requirements.txt
```

### Build knowledge graph

#### Initialize the database

Initialize your database with the script.

```bash
(env)knowledge-graph-builder$ python init_db.py
```

#### Add label data

Provide label data as lines of JSON objects 
via standard input to `add_data.py` script.

Input data should follow the rules denoted in the [knowledge-graph-input](https://github.com/uilab-vtt/knowledge-graph-input) repository.

```bash
(env)knowledge-graph-builder$ python add_data.py < input_data.jsonl
```

#### Process the similar items

Process similar items by running `merge_items` script.

```bash
(env)knowledge-graph-builder$ python merge_items.py
```

#### Extract the knowledge graph

Extract the knowledge graph as lines of JSON objects using 
`dump.py` script.

```bash
(env)knowledge-graph-builder$ python dump.py > output_graph.jsonl
```

# Acknowledgements

This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2017-0-01780, The technology development for event recognition/relational reasoning and learning knowledge based system for video understanding)
 