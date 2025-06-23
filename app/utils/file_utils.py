import shutil
from fastapi import HTTPException
from app.utils.logger_utils import logger

def create_backup(file_path: str) -> None:
    try:
        backup_path = f"{file_path}.bak"
        shutil.copyfile(file_path, backup_path)
        logger.info(f"Backup created successfully: {backup_path}")
    except Exception as e:
        logger.error(f"Error creating backup of file {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Error creating backup")

def read_file_lines(file_path: str) -> List[str]:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        logger.info(f"File {file_path} read successfully.")
        return lines
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Error reading file")

def write_file_lines(file_path: str, lines: List[str]) -> None:
    try:
        with open(file_path, "w") as file:
            file.writelines(lines)
        logger.info(f"File {file_path} updated successfully.")
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Error writing to file")
