import logging

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.async_iterator import AsyncListIterator
from src.models.post import Post
from src.models.tag import Tag

logger = logging.getLogger(__name__)


async def create_post(db: AsyncSession, id: int, q: str, a: str) -> Post:
    post_exists = await Post.check_for_post_exists(db, id)

    if not post_exists:
        post = Post(id=id, question=q, answer=a)
        logger.info(f"Created post with id: {post.id}")
        return post
    logger.info(f"Post with id: {id} already exists")


async def create_tag_obj(db: AsyncSession, name) -> Tag:
    tag = await Tag.get_by_name(db, name)
    if None is tag:
        tag = Tag(name=name)
        db.add(tag)
        await db.commit()
        return await Tag.get_by_name(db, name)
    else:
        return tag


async def write_tag_and_post(db: AsyncSession, tags: [Tag], post: Post):
    logger.info("Writing tag and post with id: " + str(post.id))
    async for tag in AsyncListIterator(tags):
        post.tags.append(tag)

    nested_list = [tags, post]

    flattened = await flat_list(nested_list)

    db.add_all(flattened)
    await db.commit()


async def flat_list(nested_list: list):
    logger.info("Flattening list")
    flatten_list = []
    async for item in AsyncListIterator(nested_list):
        if isinstance(item, list):
            for subitem in item:
                flatten_list.append(subitem)
        else:
            flatten_list.append(item)

    return flatten_list
