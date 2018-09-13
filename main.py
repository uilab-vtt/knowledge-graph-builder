from knowledge_graph_builder.knowledge_graph import KnowledgeGraph
from knowledge_graph_builder.models import Item, Property

kg = KnowledgeGraph()

ross = Item(
    id_str='ross_geller',
    classname='person',
    value='{"label":"Ross Geller"}',
    time_start=0.5,
    time_end=0.5,
    x_start=114.8,
    x_end=116.8,
    y_start=125.12,
    y_end=300.7
)

kg.session.add(ross)
kg.session.commit()

items = kg.session.query(Item).all()
for item in items:
    print(item.value)
