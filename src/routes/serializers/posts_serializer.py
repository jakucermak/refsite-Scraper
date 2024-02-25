from pydantic import BaseModel


class PostSerializer(BaseModel):
    post_id: str
    reason: str


class PostsModelSerializer(BaseModel):
    current_post: str
    current_page: str
    dropped_posts: list[str] | None = None
