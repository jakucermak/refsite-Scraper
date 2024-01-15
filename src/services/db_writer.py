from sqlalchemy.orm import Session

from src.models.post import Post
from src.models.tag import Tag


def create_post(id: int, q: str, a: str) -> Post:
    post = Post(id=id, question=q, answer=a)
    return post


def create_tag(db: Session, name: str) -> Tag:
    tag = Tag.get_by_name(db, name)
    if 0 == tag.count():
        tag = Tag(name=name)
        return tag
    else:
        return tag


def create_tag_and_post(db: Session, tags: [Tag], post: Post):
    for tag in tags:
        post.tags.append(tag)
        tag.posts.append(post)

    nested_list = [tags, post]

    flattened = flat_list(nested_list)

    db.add_all(flattened)
    db.commit()


def flat_list(nested_list):
    flatten_list = []
    for item in nested_list:
        if isinstance(item, list):
            for subitem in item:
                flatten_list.append(subitem)
        else:
            flatten_list.append(item)

    return flatten_list
