import os
from locust import HttpLocust, between, seq_task, TaskSequence
from mpegdash.parser import MPEGDASHParser
from load_generator.common import dash

MANIFEST_FILE = os.getenv('MANIFEST_FILE')


class UserBehaviour(TaskSequence):
    """
    Example task sequences with global values
    """
    base_url = None
    mpd_body = None
    mpd_object = None

    @seq_task(1)
    def get_manifest(self):
        base_url = f"{self.locust.host}/{MANIFEST_FILE}"
        self.base_url = base_url
        print(f"Requesting manifest: {base_url}/.mpd")

        response_mpd = self.client.get(f"{base_url}/.mpd")
        self.mpd_body = response_mpd.text
        print(f"Obtained MPD body with: {response_mpd.status_code} ")
        if response_mpd.status_code is 0:
            print("Make sure your Manifest URI is reachable")
            raise KeyboardInterrupt

    @seq_task(2)
    def dash_parse(self):
        print("Obtained MPD body ")
        self.mpd_object = MPEGDASHParser.parse(self.mpd_body)

    @seq_task(3)
    def dash_playback(self):
        all_reprs, period_segments = dash.prepare_playlist(
            self.base_url, self.mpd_object
        )
        selected_representation = dash.select_representation(
            period_segments["abr"],
            0  # 1 -> highest bitrate, 0 ->lowest bitrate
        )
        # dash.simple_playback(
        #     self,
        #     period_segments,
        #     selected_representation[1],
        #     selected_representation[0]
        # )
        dash.playback_w_buffer(
            self,
            period_segments,
            selected_representation[1],
            selected_representation[0],
            10  # buffer size in seconds
        )


class MyLocust(HttpLocust):
    host = os.getenv('HOST_URL', "http://localhost")
    task_set = UserBehaviour
    wait_time = between(0, 0)
