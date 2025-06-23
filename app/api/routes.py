from fastapi import APIRouter, HTTPException
from typing import List
from app.models.requests import UpdateServerRequest
from app.models.responses import UpdateServerResponse
from app.services.update_service import UpdateService
from app.utils.logger_utils import logger

router = APIRouter()

@router.put("/update-servers/", response_model=List[UpdateServerResponse])
def update_servers(requests: List[UpdateServerRequest]) -> List[UpdateServerResponse]:
    logger.info(f"Request received: {requests}")
    try:
        responses = UpdateService.update_servers(requests)
        return responses
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during server updates: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred during server updates")
