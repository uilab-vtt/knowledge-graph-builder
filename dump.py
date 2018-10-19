import json
import sys
from knowledge_graph_builder import KnowledgeGraph, logger


def main():
    graph = KnowledgeGraph()
    for json_string in graph.dump_to_json_iter():
        sys.stdout.write(json_string + '\n')

if __name__ == '__main__':
    main()
