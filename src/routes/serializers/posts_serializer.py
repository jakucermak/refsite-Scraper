from pydantic import BaseModel


class PostsSerializer(BaseModel):
    post_ids: list[str]


class PostsModelSerializer(BaseModel):
    current_post: str
    current_page: str
    dropped_posts: list[str] | None = None
