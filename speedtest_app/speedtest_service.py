import speedtest as st
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("SpeedTest")

class SpeedTestService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)

    def run_speedtest(self):
        """
        Runs the speedtest in a separate thread and returns download, upload, and ping (in Mbps, ms).
        """
        future = self.executor.submit(self._run)
        return future

    def _run(self):
        try:
            speedtest = st.Speedtest()
            speedtest.get_best_server()
            download_speed = speedtest.download() / 1_000_000  # Мбит/с
            upload_speed = speedtest.upload() / 1_000_000      # Мбит/с
            ping = speedtest.results.ping                      # мс
            return {
                'download': download_speed,
                'upload': upload_speed,
                'ping': ping
            }
        except Exception as e:
            logger.error(f"Speedtest error: {e}", exc_info=True)
            return {'error': str(e)} 