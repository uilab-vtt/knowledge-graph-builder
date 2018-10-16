import json
import sys
from knowledge_graph_builder import KnowledgeGraph, logger


def get_labels_iter():
    for line in sys.stdin:
        try:
            yield json.loads(line)
        except json.decoder.JSONDecodeError:
            logger.warn('Failed to decode JSON line: %s' % line.strip())

def main():
    graph = KnowledgeGraph()

    for label in get_labels_iter():
        graph.add_label(label)

if __name__ == '__main__':
    main()
