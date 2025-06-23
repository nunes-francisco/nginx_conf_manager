import re
import subprocess
from fastapi import HTTPException
from typing import List, Optional
from app.models.requests import LocationBlock
from app.utils.file_utils import read_file_lines
from app.utils.logger_utils import logger

class NginxService:
    @staticmethod
    def get_default_config_path() -> str:
        return "/etc/nginx/nginx.conf"

    @staticmethod
    def update_upstream_server(file_path: str, upstream_name: str, old_ip: str, new_ip: str) -> List[str]:
        lines = read_file_lines(file_path)
        updated_lines = []
        inside_upstream_block = False
        upstream_block_pattern = re.compile(r"^\s*upstream\s+{}\s*\{{".format(re.escape(upstream_name)))
        server_line_pattern = re.compile(r"^\s*server\s+{}(:\d+)?;".format(re.escape(old_ip)))
        found_server = False
        found_upstream = False

        for line in lines:
            if upstream_block_pattern.match(line):
                inside_upstream_block = True
                found_upstream = True
                logger.info(f"Upstream block found: {upstream_name}")

            if inside_upstream_block and server_line_pattern.match(line):
                updated_line = re.sub(r"\b{}\b".format(re.escape(old_ip)), new_ip, line)
                updated_lines.append(updated_line)
                found_server = True
                logger.info(f"Server line updated: {line.strip()} -> {updated_line.strip()}")
            else:
                updated_lines.append(line)

            if inside_upstream_block and line.strip() == "}":
                inside_upstream_block = False

        if not found_upstream:
            logger.warning(f"Upstream block {upstream_name} not found.")
            raise HTTPException(status_code=404, detail=f"Upstream block {upstream_name} not found.")

        if found_upstream and not found_server:
            logger.warning(f"Server with IP {old_ip} not found in upstream block {upstream_name}.")

        return updated_lines

    @staticmethod
    def add_location_blocks(lines: List[str], locations: Optional[List[LocationBlock]]) -> List[str]:
        if locations:
            inside_http_block = False
            updated_lines = []

            for line in lines:
                updated_lines.append(line)
                if line.strip() == "http {":
                    inside_http_block = True

                if inside_http_block and line.strip() == "}":
                    inside_http_block = False
                    for location in locations:
                        location_block = f"""
        location {location.path} {{
            proxy_pass {location.proxy_pass};
        }}
    """
                        updated_lines.append(location_block)
                        logger.info(f"Location block added: {location_block.strip()}")

            return updated_lines
        return lines

    @staticmethod
    def test_nginx_configuration() -> str:
        try:
            result = subprocess.run(["nginx", "-t"], capture_output=True, text=True, check=True)
            logger.info("Nginx configuration tested successfully.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error testing Nginx configuration: {e.stderr}")
            raise HTTPException(status_code=500, detail=f"Error testing Nginx configuration: {e.stderr}")

    @staticmethod
    def restart_nginx_service() -> bool:
        try:
            subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
            logger.info("Nginx restarted successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error restarting Nginx: {e}")
            return False

    @staticmethod
    def get_nginx_process_info() -> str:
        try:
            result = subprocess.run(["ps", "-C", "nginx", "-o", "pid,cmd"], capture_output=True, text=True, check=True)
            logger.info("Nginx process info retrieved successfully.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error retrieving Nginx process info: {e}")
            return f"Error retrieving Nginx process info: {e.stderr}"
