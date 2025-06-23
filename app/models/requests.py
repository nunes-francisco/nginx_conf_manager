from pydantic import BaseModel
from typing import Optional, List

class LocationBlock(BaseModel):
    path: str
    proxy_pass: str

class UpdateServerRequest(BaseModel):
    file_path: Optional[str] = None
    upstream_name: str
    old_ip: str
    new_ip: str
    locations: Optional[List[LocationBlock]] = None
