import os
import shutil
from datetime import datetime

from logs.logger import logger


class BackupManager:

    @staticmethod
    def create_backup(source_path):

        if not os.path.exists(source_path):

            logger.warning(
                f"Backup failed. Source not found: {source_path}"
            )

            print(
                f"Source not found: {source_path}"
            )

            return None

        backup_folder = "data/backups"

        os.makedirs(
            backup_folder,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        name = os.path.basename(source_path)

        backup_name = f"{timestamp}_{name}"

        backup_path = os.path.join(
            backup_folder,
            backup_name
        )

        if os.path.isdir(source_path):

            shutil.copytree(
                source_path,
                backup_path
            )

        else:

            shutil.copy2(
                source_path,
                backup_path
            )

        logger.info(
            f"Backup created: {backup_path}"
        )

        print(
            f"Backup created: {backup_path}"
        )

        return backup_path