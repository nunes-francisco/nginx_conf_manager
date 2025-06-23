from typing import List
from fastapi import HTTPException
from app.models.requests import UpdateServerRequest
from app.models.responses import UpdateServerResponse
from app.utils.file_utils import create_backup, read_file_lines, write_file_lines
from app.services.nginx_service import NginxService
from app.utils.logger_utils import logger

class UpdateService:
    @staticmethod
    def update_servers(requests: List[UpdateServerRequest]) -> List[UpdateServerResponse]:
        responses = []

        for request in requests:
            try:
                if request.file_path is None:
                    request.file_path = NginxService.get_default_config_path()
                create_backup(request.file_path)
                updated_lines = NginxService.update_upstream_server(
                    request.file_path, request.upstream_name, request.old_ip, request.new_ip
                )
                updated_lines = NginxService.add_location_blocks(updated_lines, request.locations)
                write_file_lines(request.file_path, updated_lines)
                response = UpdateServerResponse(
                    message=f"Server IP updated successfully for upstream {request.upstream_name}",
                    success=True
                )
            except HTTPException as e:
                response = UpdateServerResponse(message=e.detail, success=False)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                response = UpdateServerResponse(message="Unexpected error occurred", success=False, detail=str(e))
            responses.append(response)

        try:
            config_test_output = NginxService.test_nginx_configuration()
            nginx_restart_success = False
            if "successful" in config_test_output:
                nginx_restart_success = NginxService.restart_nginx_service()
            nginx_process_info = NginxService.get_nginx_process_info()
            for response in responses:
                response.config_test_output = config_test_output
                response.nginx_restart_success = nginx_restart_success
                response.nginx_process_info = nginx_process_info
        except HTTPException as e:
            for response in responses:
                response.config_test_output = e.detail
                response.nginx_restart_success = False
                response.nginx_process_info = NginxService.get_nginx_process_info()
            return responses

        logger.info("All updates applied and Nginx restarted successfully.")
        return responses
