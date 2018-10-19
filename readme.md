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

```bash
(env)knowledge-graph-builder$ python add_data.py < input_data.jsonl
```

#### Extract the knowledge graph

Extract the knowledge graph as lines of JSON objects using 
`dump.py` script.

```bash
(env)knowledge-graph-builder$ python dump.py > output_graph.jsonl
```