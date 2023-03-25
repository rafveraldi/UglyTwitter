from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_api():
    return [{'username': 'Admin'}]
