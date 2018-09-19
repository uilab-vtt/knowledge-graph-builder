from knowledge_graph_builder.knowledge_graph import KnowledgeGraph
from knowledge_graph_builder.models import Item, Property, ValidTime, Box
from sqlalchemy.orm.exc import NoResultFound

kg = KnowledgeGraph()

def insert_rows():
    ross = Item(
        id_str='ross_geller',
        classname='person',
        value='{"label":"Ross Geller"}'
    )
    kg.session.add(ross)
    # kg.session.commit()
    ross_box = Box(
        x_start=114.8,
        x_end=116.8,
        y_start=125.12,
        y_end=300.7,
        item=ross
    )
    kg.session.add(ross_box)
    # kg.session.commit()
    ross_time = ValidTime(
        time_start=0.5,
        time_end=0.5,
        item=ross
    )
    kg.session.add(ross_time)
    kg.session.commit()

def test_join():
    pass

# insert_rows()

# items = kg.session.query(Item).all()
# for item in items:
#     print(item.value)

# item = kg.session.query(Item).filter_by(id_str='ross_geller').one()
# print(item)

# try:
#     item = kg.session.query(Item).filter_by(id_str='ross_gellera').one()
#     print(item)
# except NoResultFound as e:
#     print('nrf', e)
