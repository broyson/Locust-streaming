import sys
import os
from locust import HttpLocust, between, TaskSequence
# seq_task
# from load_generator.common.dash_emulation import class_dash_player
from load_generator.common.dash_emulation import  class_dash_player
from load_generator.common.hls_emulation import class_hls_player
import logging

logger = logging.getLogger(__name__)

MANIFEST_FILE = os.getenv('MANIFEST_FILE')


class Client(TaskSequence):
    """
    Verifies if it is a MPEG-DASH or HLS manifest
    """
    # tasks = {hello_out_task: 1}
    # @seq_task(1)
    def on_start(self):
        base_url = f"{self.locust.host}/{MANIFEST_FILE}"
        self.base_url = base_url
        if base_url.endswith(".mpd"):
            logger.info("It is a MPEG-DASH URI")
            self.schedule_task(class_dash_player)  # --> load_generator.common.dash_emulation
            # tasks = {hello_out_task: 1}
        elif base_url.endswith(".m3u8"):
            logger.info("It is a HLS URI")
            self.schedule_task(class_hls_player)  # -> load_generator.common.hls_emulation
        else:
            logger.error(
                f"The URI provided is not supported for MPEG-DASH or "
                f"HLS media endpoint. Make sure the MANIFEST_FILE "
                f"envrionment ends with '.mpd' or '.m3u8'"
            )
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

        # Check if the Manifest is available before proceeding to test
        manifest_response = self.client.get(self.base_url, name="merged")
        if manifest_response.status_code != 200:
            logger.error(
                f"The Manifest endpoint is not reachable. Verify that "
                f" you can reach the Manifest file: {self.base_url}"
            )
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


class MyLocust(HttpLocust):
    host = os.getenv(f'HOST_URL', "http://localhost")
    task_set = Client
    wait_time = between(0, 0)
