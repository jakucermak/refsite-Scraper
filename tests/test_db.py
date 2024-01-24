import pytest

from conftest import db_session, stored_tags, tags, tag3, tag4, tag5, post1
from src.models.associations import association_table
from src.models.post import Post
from src.models.tag import Tag
from src.services.db_writer import flat_list, create_tag_obj, write_tag_and_post

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_nested_list():
    nested_list = [[1, 2, 3, 4], 5, 6, 7]
    expected = [1, 2, 3, 4, 5, 6, 7]
    act = await flat_list(nested_list)

    assert act == expected


class TestDatabase:

    @pytest.mark.asyncio
    def test_empy_tag(self, db_session):

        result = db_session.query(Tag).all()
        result_cnt = len(result)

        assert result_cnt == 0

    @pytest.mark.asyncio
    def test_create_tag(self, db_session, tags):
        for tag_name in tags:
            create_tag_obj(db_session, tag_name)

        expected_tags = [Tag(id=1, name="tag1"), Tag(id=2, name="tag2")]
        result = db_session.query(Tag).all()

        for exp, actual in zip(expected_tags, result):
            assert actual.name == exp.name
            assert actual.id == exp.id

    @pytest.mark.asyncio
    def test_duplicate_tag(self, db_session, stored_tags, tags):
        saved_tags = db_session.query(Tag).all()
        saved_tags_cnt = len(saved_tags)
        assert saved_tags_cnt == 2
        tags_to_write = []
        for tag in tags:
            tags_to_write.append(create_tag_obj(db_session, tag))

        for e, a in zip(saved_tags, tags_to_write):
            assert e.id == a.id

    @pytest.mark.asyncio
    def test_add_tag(self, db_session, stored_tags, tag3):
        pre_stored_tags = db_session.query(Tag).all()

        assert len(pre_stored_tags) == 2

        tag = create_tag_obj(db_session, tag3)

        db_session.add(tag)
        db_session.commit()
        assert len(db_session.query(Tag).all()) == 3

    @pytest.mark.asyncio
    def test_write_post(self, db_session, post1, tags):
        pre_post = db_session.query(Post).all()
        pre_tags = db_session.query(Tag).all()
        assert len(pre_post) == 0
        assert len(pre_tags) == 0
        tag_objs = [create_tag_obj(db_session, name) for name in tags]
        write_tag_and_post(db_session, tag_objs, post1)
        post = db_session.query(Post)
        tags = db_session.query(Tag)

        assert len(post.all()) == 1
        assert len(tags.all()) == 2

        expected_post_q = post1.question
        actual_post: Post = post.get(post1.id)

        assert actual_post.question == expected_post_q

        for e, a in zip(post1.tags, actual_post.tags):
            assert a == e

    @pytest.mark.asyncio
    def test_write_posts(self, db_session, post1, tags, tag3, post2, tag5, tag4):
        tag_objs = [create_tag_obj(db_session, tag) for tag in tags]
        tag_objs.append(create_tag_obj(db_session, tag3))

        write_tag_and_post(db_session, tag_objs, post1)

        tag_objs_2 = [create_tag_obj(db_session, tag) for tag in [tag3, tag4, tag5]]
        write_tag_and_post(db_session, tag_objs_2, post2)

        assert len(db_session.query(Post).all()) == 2
        assert len(db_session.query(Tag).all()) == 5
        assert len(db_session.query(association_table).all()) == 6
