from pydantic import BaseModel
from typing import Optional

class UpdateServerResponse(BaseModel):
    message: str
    success: bool
    detail: Optional[str] = None
    config_test_output: Optional[str] = None
    nginx_restart_success: Optional[bool] = None
    nginx_process_info: Optional[str] = None
