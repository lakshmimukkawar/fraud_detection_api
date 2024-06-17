from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/ping")
async def get_item():
    try:
        return JSONResponse(status_code=200, content={"message": "Service is up!"})
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"error": "Internal Server Error"}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
