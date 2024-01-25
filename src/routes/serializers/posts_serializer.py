from pydantic import BaseModel


class PostsSerializer(BaseModel):
    post_ids: [str]
