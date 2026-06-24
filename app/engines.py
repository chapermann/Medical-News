from fastapi import APIRouter

router = APIRouter()

@router.post("/engine/run")
def run_engine_endpoint(engine_id: int):

    return {
        "status": "executed",
        "engine_id": engine_id
    }
