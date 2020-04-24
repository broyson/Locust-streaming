import os
import sys
import logging
from locust import TaskSequence, seq_task, TaskSet, task
from mpegdash.parser import MPEGDASHParser
from load_generator.common import dash
from load_generator.config import default
import random



logger = logging.getLogger(__name__)

MANIFEST_FILE = os.getenv('MANIFEST_FILE')

BUFFER = "buffer_size"
PLAY_MODE = "play_mode"
BITRATE = "bitrate"


class class_dash_player(TaskSequence):
    """
    Simple MPEG-DASH emulation of a player
    Receives an MPEG-DASH /.mpd manifest
    """
    base_url = None
    mpd_body = None
    mpd_object = None

    @seq_task(1)
    def get_manifest(self):
        logger.info("MPEG-DASH child player running ...")
        base_url = f"{self.locust.host}/{MANIFEST_FILE}"
        self.base_url = base_url
        logger.info(f"Requesting manifest: {base_url}")
        response_mpd = self.client.get(f"{base_url}")
        self.mpd_body = response_mpd.text
        if response_mpd.status_code == 0 or response_mpd.status_code == 404:
            logger.error("Make sure your Manifest URI is reachable")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        else:
            pass

    @seq_task(2)
    def dash_parse(self):
        """
        Parse Manifest file to MPEGDASHParser
        """
        logger.info("Obtained MPD body ")
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
        chosen_video = selected_representation[1]
        chosen_audio = selected_representation[0]
        buffer_size = int(os.environ.get("buffer_size"))
        play_mode = os.environ.get("play_mode")
        if play_mode == "full_playback":
            if buffer_size == 0:
                dash.simple_playback(
                    self,
                    period_segments,
                    chosen_video,
                    chosen_audio,
                    False  # Delay in between every segment request
                )
            else:
                dash.playback_w_buffer(
                    self,
                    period_segments,
                    chosen_video,
                    chosen_audio,
                    buffer_size
                )
        elif play_mode == "only_manifest":
            self.get_manifest()
        else:
            # Random segments request for audio and video
            video_timeline = period_segments["repr"][chosen_video]["timeline"]
            audio_timeline = period_segments["repr"][chosen_audio]["timeline"]
            video_segment = random.choice(video_timeline)
            audio_segment = random.choice(audio_timeline)
            logger.info(video_segment["url"])
            self.client.get(video_segment["url"])
            logger.info(audio_segment["url"])
            self.client.get(audio_segment["url"])

    # @task
    # def hello_task(self):
    #     print("Hello from task")
    #     self._sleep(2)

# def hello_out_task(self):
#     print("Hello from outside task")
#     self._sleep(2)

# class dash_random_segments_dash(TaskSet):
#     """
#     Selects random segments from the MPEG-DASH playlist
#     """
#     @task
#     def on_start(self):
#         dash_player = class_dash_player()

#         return True
