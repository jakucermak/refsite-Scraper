from sqlalchemy import select

import src.models.tag
from src.services.db_writer import flat_list
from fixtures import test_db, db_session, tags
from src.services.db_writer import create_tag
from src.models.tag import Tag


def test_nested_list():
    nested_list = [[1, 2, 3, 4], 5, 6, 7]
    expected = [1,2,3,4,5,6,7]
    act = flat_list(nested_list)

    assert act == expected


class TestDatabase:

    def test_empy_tag(self, db_session, tags):

        for tag in tags:
            db_session.add(tag)
        db_session.commit()

        result = db_session.execute(select(src.models.tag.Tag)).all()
        assert result == 2

