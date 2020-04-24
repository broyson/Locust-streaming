import os
import sys
from locust import HttpLocust, between, seq_task, TaskSequence
from mpegdash.parser import MPEGDASHParser
from load_generator.common import dash
from load_generator.config import default  # ENV configuration
import logging


logger = logging.getLogger(__name__)
MANIFEST_FILE = os.getenv('MANIFEST_FILE')

logger = logging.getLogger(__name__)


class UserBehaviour(TaskSequence):
    """
    Example task sequences with global values
    """
    base_url = None
    mpd_body = None
    mpd_object = None

    @seq_task(1)
    def get_manifest(self):
        """
        Retrieve the MPD manifest file
        """
        # mode = os.environ.get("mode")
        base_url = f"{self.locust.host}/{MANIFEST_FILE}"
        self.base_url = base_url
        logger.info(f"Requesting manifest: {base_url}/.mpd")
        response_mpd = self.client.get(f"{base_url}/.mpd")
        self.mpd_body = response_mpd.text
        # Exit the program if the Manifest file is not reachable
        if response_mpd.status_code == 0:
            logger.error(
                f"Make sure your Manifest URI is reachable: {base_url}"
            )
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    @seq_task(2)
    def dash_parse(self):
        """
        Parse Manifest file to MPEGDASHParser
        """
        self.mpd_object = MPEGDASHParser.parse(self.mpd_body)

    @seq_task(3)
    def dash_playback(self):
        """
        Create a list of the avaialble segment URIs with
        its specific media representation
        """
        all_reprs, period_segments = dash.prepare_playlist(
            self.base_url, self.mpd_object
        )
        bitrate = os.environ.get("bitrate")
        selected_representation = dash.select_representation(
            period_segments["abr"],
            bitrate  # highest_bitrate, lowest_bitrate, random_bitrate
        )
        buffer_size = int(os.environ.get("buffer_size"))
        if buffer_size == 0:
            dash.simple_playback(
                self,
                period_segments,
                selected_representation[1],
                selected_representation[0],
                False
            )
        else:
            dash.playback_w_buffer(
                self,
                period_segments,
                selected_representation[1],
                selected_representation[0],
                buffer_size
            )


class MyLocust(HttpLocust):
    host = os.getenv('HOST_URL', "http://localhost")
    task_set = UserBehaviour
    wait_time = between(0, 0)
