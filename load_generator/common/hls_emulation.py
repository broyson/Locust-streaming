import os
import m3u8
from locust import TaskSet, task
from load_generator.config import default
import logging

logger = logging.getLogger(__name__)


MANIFEST_FILE = os.getenv('MANIFEST_FILE')


class class_hls_player(TaskSet):
    """
    Simple MPEG-DASH emulation of a player
    Receives an MPEG-DASH /.mpd manifest
    """
    @task(1)
    def hls_player_child(self):
        logger.info("HLS child player running ...")
        base_url = (f"{self.locust.host}/{MANIFEST_FILE}")

        # get master HLS manifest
        master_url = f"{base_url}/.m3u8"
        master_m3u8 = self.client.get(master_url, name="merged")
        parsed_master_m3u8 = m3u8.M3U8(content=master_m3u8.text, base_uri=base_url)

        # Select highest bitrate index = 3
        variant = parsed_master_m3u8.playlists[3]

        variant_url = "{base_url}/{variant}".format(base_url=base_url, variant=variant.uri)
        variant_m3u8 = self.client.get(variant_url, name="merged")
        parsed_variant_m3u8 = m3u8.M3U8(content=variant_m3u8.text, base_uri=base_url)

        # get all the segments
        for segment in parsed_variant_m3u8.segments:
            logger.info(segment.absolute_uri)
            # seg_get = self.client.get(segment.absolute_uri, name="merged")
            seg_get = self.client.get(segment.absolute_uri)
            sleep = segment.duration - seg_get.elapsed.total_seconds()
            # self._sleep(sleep)
