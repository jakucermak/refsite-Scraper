from fastapi import APIRouter

router = APIRouter()


@router.get("/posts")
def post_pages_parsed_posts():
    return {
        "current_page_parsing": "hello"
    }
