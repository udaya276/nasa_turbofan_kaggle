import os
from nasa.logger import logging
class S3Sync:


    def sync_folder_to_s3(self,folder,aws_buket_url):
        logging.info("line 1")
        command = f"aws s3 sync {folder} {aws_buket_url} "
        logging.info("line 2")
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        logging.info("line 3")
        command = f"aws s3 sync {aws_bucket_url} {folder} "
        logging.info("line 4")
        os.system(command)