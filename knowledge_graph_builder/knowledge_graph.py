import json
from sqlalchemy import and_, or_
from sqlalchemy.orm.exc import NoResultFound

from .models import get_sessionmaker, Item, ItemSimilarityRelation, ValidTime, Box, Property
from .logger import logger
from .word_model import WordModel
from . import config

class KnowledgeGraph:
    def __init__(self):
        self.Sessionmaker = get_sessionmaker()
        self.session = self.Sessionmaker()
        self.word_model = WordModel()

    def get_all_items(self):
        return self.session.query(Item).all()

    def get_all_valid_times(self):
        return self.session.query(ValidTime).all()

    def get_all_boxes(self):
        return self.session.query(Box).all()

    def get_all_properties(self):
        return self.session.query(Property).all()

    def get_all_similarities(self):
        return self.session.query(ItemSimilarityRelation).all()

    def set_item_similarities(self):
        rows = self.session.execute('''
            SELECT   MIN(a.id) a, a.classname a, b.id b, b.classname b
            FROM     item a JOIN item b ON a.id <> b.id AND b.ID > a.ID
            GROUP BY b.ID
        ''')
        batch_count = 0

        def sanitize(word):
            return word.lower().replace('-', ' ').replace('_', ' ')
        
        for id1, classname1, id2, classname2 in rows:
            similarity = self.word_model.get_word_similarity(
                sanitize(classname1), 
                sanitize(classname2),
            )
            if similarity is not None:
                self.session.add(ItemSimilarityRelation(
                    similarity=similarity,
                    item_id=id1,
                    another_item_id=id2,
                ))
                batch_count += 1
                if batch_count >= 100:
                    self.session.commit()
                    batch_count = 0
        self.session.commit()
    
    def get_overlapped_items_by_coordinate(self, coordinate, seconds):
        x_start, y_start, x_end, y_end = coordinate
        time_start = seconds - config.MERGE_TIME_WINDOW
        time_end = seconds + config.MERGE_TIME_WINDOW
        rows = self.session.query(Item, ValidTime, Box).filter(and_(
            Item.id == ValidTime.item_id,
            Item.id == Box.item_id,
            or_(
                and_(
                    ValidTime.time_start >= time_start,
                    ValidTime.time_start <= time_end
                ),
                and_(
                    ValidTime.time_end >= time_start,
                    ValidTime.time_end <= time_end
                )
            ),
            Box.time >= time_start,
            Box.time <= time_end,
            or_(
                and_(
                    Box.x_start >= x_start,
                    Box.x_start <= x_end
                ),
                and_(
                    Box.x_end >= x_start,
                    Box.x_end <= x_end
                )
            ),
            or_(
                and_(
                    Box.y_start >= y_start,
                    Box.y_start <= y_end
                ),
                and_(
                    Box.y_end >= y_start,
                    Box.y_end <= y_end
                )
            )
        ))
        return rows

    def is_coordinates_mergeable(self, coordinate1, coordinate2):
        c1_x_start, c1_y_start, c1_x_end, c1_y_end = coordinate1
        c2_x_start, c2_y_start, c2_x_end, c2_y_end = coordinate2
        overlap_width = max(
            0, 
            min(c1_x_end, c2_x_end) - max(c1_x_start, c2_x_start)
        )
        overlap_height = max(
            0, 
            min(c1_y_end, c2_y_end) - max(c1_y_start, c2_y_start)
        )
        c1_area = (c1_x_end - c1_x_start) * (c1_y_end - c1_y_start)
        c2_area = (c2_x_end - c2_x_start) * (c2_y_end - c2_y_start)
        overlap_area = overlap_width * overlap_height
        return (
            (overlap_area > c1_area * config.MERGE_OVERLAP_THRESHOLD) and
            (overlap_area > c2_area * config.MERGE_OVERLAP_THRESHOLD)
        )

    def get_item_by_id_str(self, id_str):
        try:
            return self.session.query(Item).filter_by(id_str=id_str).one()
        except NoResultFound:
            return None

    def get_abstract_item(self, classname, label):
        try:
            return self.session.query(Item).filter_by(
                classname=classname,
                label=label,
                is_abstract=True,
            ).one()
        except NoResultFound:
            return None

    def get_or_create_video_item(self):
        item = self.get_item_by_id_str('_video')
        if item is None:
            item = Item(
                id_str='_video',
                classname='video',
                label='video',
                is_abstract=True,
            )
            self.session.add(item)
            self.session.commit()
        return item

    def get_or_create_abstract_item(self, classname, label):
        item = self.get_abstract_item(classname, label)
        if item is None:
            item = Item(
                classname=classname,
                label=label,
                is_abstract=True
            )
            self.session.add(item)
            self.session.commit()
        return item

    def create_item_with_coordinate(self, coordinate, seconds):
        item = Item(
            classname='unknown',
            label='unknown',
        )
        self.session.add(item)
        box = Box(
            time=seconds,
            x_start=coordinate[0],
            x_end=coordinate[2],
            y_start=coordinate[1],
            y_end=coordinate[3],
            item=item,
        )
        self.session.add(box)
        valid_time = ValidTime(
            time_start=seconds,
            time_end=seconds,
            item=item,
        )
        self.session.add(valid_time)
        self.session.commit()
        return item

    def create_item_with_id_str(self, id_str, seconds):
        item = Item(
            classname='item',
            label=id_str,
            id_str=id_str,
        )
        self.session.add(item)
        valid_time = ValidTime(
            time_start=seconds,
            time_end=seconds,
            item=item,
        )
        self.session.add(valid_time)
        self.session.commit()
        return item

    def get_item_by_coordinate(self, coordinate, seconds):
        rows = self.get_overlapped_items_by_coordinate(coordinate, seconds)
        for item, valid_time, box in rows:
            box_coordinate = (
                box.x_start,
                box.y_start,
                box.x_end,
                box.y_end,
            )
            if self.is_coordinates_mergeable(coordinate, box_coordinate):
                return item
        return None

    def get_absolute_coordinate(self, coordinate):
        x, y, width, height = coordinate
        return x, y, x + width, y + height

    def get_item_by_indicator(self, indicator, seconds):
        if 'id' in indicator:
            item = self.get_item_by_id_str(indicator['id'])
            if item is None:
                item = self.create_item_with_id_str(indicator['id'], seconds)
            return item
        elif 'coordinates' in indicator:
            abs_coord = self.get_absolute_coordinate(
                indicator['coordinates']
            )
            item = self.get_item_by_coordinate(abs_coord, seconds)
            if item is None:
                item = self.create_item_with_coordinate(abs_coord, seconds)
            return item
        else:
            logger.error(
                'Failed to find an object with object indicator "%s"' 
                % json.dumps(indicator)
            )
            return None

    def get_or_create_valid_time(self, seconds, item):
        seconds_lb = seconds - config.MERGE_TIME_WINDOW
        seconds_ub = seconds + config.MERGE_TIME_WINDOW
        valid_time = self.session.query(ValidTime).filter(
            and_(
                or_(
                    and_(
                        ValidTime.time_start <= seconds,
                        ValidTime.time_end >= seconds,
                    ),
                    and_(
                        ValidTime.time_start <= seconds,
                        ValidTime.time_end >= seconds_lb,
                    ),
                    and_(
                        ValidTime.time_start <= seconds_ub,
                        ValidTime.time_end >= seconds,
                    ),
                ),
                ValidTime.item_id == item.id,
            )
        ).first()
        if valid_time is not None:
            if valid_time.time_start <= seconds and valid_time.time_end >= seconds:
                return valid_time
            elif valid_time.time_start <= seconds and valid_time.time_end >= seconds_lb:
                if valid_time.time_end < seconds:
                    valid_time.time_end = seconds  
            elif valid_time.time_start <= seconds_ub and valid_time.time_end >= seconds:
                if valid_time.time_start > seconds:
                    valid_time.time_start = seconds
            return valid_time
        else:
            return ValidTime(
                time_start=seconds,
                time_end=seconds,
                item=item,
            )

    def get_or_create_property(self, classname, seconds, source, target, relation=None, id_str=None, value=None):
        seconds_lb = seconds - config.MERGE_TIME_WINDOW
        seconds_ub = seconds + config.MERGE_TIME_WINDOW
        query_filter = and_(
            or_(
                and_(
                    Property.time_start <= seconds,
                    Property.time_end >= seconds,
                ),
                and_(
                    Property.time_start <= seconds,
                    Property.time_end >= seconds_lb,
                ),
                and_(
                    Property.time_start <= seconds_ub,
                    Property.time_end >= seconds,
                ),
            ),
            Property.classname == classname,
            Property.source_item_id == source.id,
            Property.target_item_id == target.id,
        )
        if relation is not None:
            query_filter = and_(
                query_filter,
                Property.relation_item_id == relation.id,
            )
        if value is not None:
            query_filter = and_(
                query_filter,
                Property.value == value,
            )
        if id_str is not None:
            query_filter = and_(
                query_filter,
                Property.id_str == id_str,
            )
        prop = self.session.query(Property).filter(query_filter).first()
        if prop is not None:
            if prop.time_start <= seconds and prop.time_end >= seconds:
                return prop
            elif prop.time_start <= seconds and prop.time_end >= seconds_lb:
                if prop.time_end < seconds:
                    prop.time_end = seconds
            elif prop.time_start <= seconds_ub and prop.time_end >= seconds:
                if prop.time_start > seconds:
                    prop.time_start = seconds
        else:
            prop = Property(
                id_str=id_str,
                classname=classname,
                time_start=seconds,
                time_end=seconds,
                source=source,
                target=target,
                relation=relation,
            )
        self.session.add(prop)
        self.session.commit()
        return prop

    def add_object_label(self, label):
        abs_coord = self.get_absolute_coordinate(label['coordinates'])
        item = None
        if 'id' in label:
            item = self.get_item_by_id_str(label['id']) 
        if item is None:
            item = self.get_item_by_coordinate(abs_coord, label['seconds'])
        if item is None:
            item = Item()
        item.classname = label['class']
        item.label = label['label']
        if 'id' in label and not item.id_str:
            item.id_str = label['id']
        self.session.add(item)
        valid_time = self.get_or_create_valid_time(label['seconds'], item)
        self.session.add(valid_time)
        box = Box(
            time=label['seconds'],
            x_start=abs_coord[0],
            x_end=abs_coord[2],
            y_start=abs_coord[1],
            y_end=abs_coord[3],
            item=item,
        )
        self.session.add(box)
        self.session.commit()

    def add_behavior_label(self, label):
        item = self.get_item_by_indicator(
            label['object'], 
            label['seconds'],
        )
        abstract_item = self.get_or_create_abstract_item(
            'behavior', 
            label['class'],
        )
        self.get_or_create_property('do', label['seconds'], item, abstract_item)

    def add_emotion_label(self, label):
        item = self.get_item_by_indicator(
            label['object'],
            label['seconds'],
        )
        abstract_item = self.get_or_create_abstract_item(
            'emotion',
            label['class'],
        )
        self.get_or_create_property('feel', label['seconds'], item, abstract_item)

    def add_relation_label(self, label):
        relation_item = self.get_or_create_abstract_item(
            label['class'],
            label['subclass'],
        )
        source_item = self.get_item_by_indicator(
            label['source'],
            label['seconds'],
        )
        target_item = self.get_item_by_indicator(
            label['target'],
            label['seconds'],
        )
        self.get_or_create_property(
            'related_to',
            label['seconds'],
            source_item,
            target_item,
            relation_item,
        )

    def add_location_label(self, label):
        item = self.get_or_create_abstract_item(
            'location',
            label['class'],
        )
        self.get_or_create_property(
            'location_of',
            label['seconds'],
            item,
            self.get_or_create_video_item(),
        )

    def add_sound_label(self, label):
        item = self.get_or_create_abstract_item(
            'sound',
            label['class'],
        )
        self.get_or_create_property(
            'sound_of',
            label['seconds'],
            item,
            self.get_or_create_video_item(),
        )

    def add_label(self, label):
        if label['type'] == 'object':
            self.add_object_label(label)
        elif label['type'] == 'behavior':
            self.add_behavior_label(label)
        elif label['type'] == 'emotion':
            self.add_emotion_label(label)
        elif label['type'] == 'relation':
            self.add_relation_label(label)
        elif label['type'] == 'location':
            self.add_location_label(label)
        elif label['type'] == 'sound':
            self.add_sound_label(label)

    def dump_to_dict_iter(self):
        for item in self.get_all_items():
            yield item.as_dict()
        for valid_time in self.get_all_valid_times():
            yield valid_time.as_dict()
        for box in self.get_all_boxes():
            yield box.as_dict()
        for prop in self.get_all_properties():
            yield prop.as_dict()
        for similarity in self.get_all_similarities():
            if similarity.similarity > config.ITEM_MERGE_THRESHOLD:
                yield similarity.as_dict()

    def dump_to_json_iter(self):
        for d in self.dump_to_dict_iter():
            yield json.dumps(d)
