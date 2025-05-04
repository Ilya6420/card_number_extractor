from fastapi import APIRouter


router = APIRouter()


@router.get("/", summary="Health Check endpoint", description="Returns the health status of the API")
async def health_check():
    return {"status": "healthy"}
