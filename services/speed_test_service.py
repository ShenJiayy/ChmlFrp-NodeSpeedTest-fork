import socket
import time
import requests
import threading
from typing import Dict, Optional, Callable, List
from dataclasses import dataclass

@dataclass
class SpeedTestResult:
    success: bool
    latency: Optional[float] = None
    download_speed: Optional[float] = None
    error: Optional[str] = None

@dataclass
class LogEntry:
    timestamp: float
    message: str
    type: str  # "info", "error", "success", "warning"

@dataclass
class SpeedTestProgress:
    stage: str  # "idle", "testing_latency", "testing_speed", etc.
    message: str
    progress: Optional[float] = None
    logs: List[LogEntry] = None

class SpeedTestService:
    def __init__(self):
        self.abort_controller = None
        self.logs: List[LogEntry] = []
        self.is_running = False

    def add_log(self, message: str, log_type: str = "info"):
        entry = LogEntry(
            timestamp=time.time(),
            message=message,
            type=log_type
        )
        self.logs.append(entry)
        print(f"[SpeedTest][{log_type.upper()}] {message}")

    def test_latency(self, host: str, port: int = 80, timeout: float = 5.0) -> SpeedTestResult:
        """Test latency by connecting to TCP port"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.close()
            latency = (time.time() - start_time) * 1000  # ms
            return SpeedTestResult(success=True, latency=latency)
        except Exception as e:
            return SpeedTestResult(success=False, error=str(e))

    def test_download_speed(self, url: str, test_size: int = 1024*1024) -> SpeedTestResult:
        """Test download speed by downloading a file"""
        try:
            start_time = time.time()
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    downloaded += len(chunk)
                    if downloaded >= test_size:
                        break

            duration = time.time() - start_time
            if duration > 0:
                speed_bps = downloaded / duration
                speed_mbps = speed_bps * 8 / (1024 * 1024)  # Mbps
                return SpeedTestResult(success=True, download_speed=speed_mbps)
            else:
                return SpeedTestResult(success=False, error="测试时间太短")
        except Exception as e:
            return SpeedTestResult(success=False, error=str(e))

    def test_node(self, node: Dict, callback: Optional[Callable] = None) -> SpeedTestResult:
        """Test a single node"""
        self.is_running = True
        self.logs = []

        try:
            # Test latency
            if callback:
                progress = SpeedTestProgress(
                    stage="testing_latency",
                    message="测试延迟...",
                    logs=self.logs.copy()
                )
                callback(progress)

            latency_result = self.test_latency(node.get('host', ''), node.get('port', 80))

            if not latency_result.success:
                return latency_result

            # Test download speed
            if callback:
                progress = SpeedTestProgress(
                    stage="testing_speed",
                    message="测试下载速度...",
                    logs=self.logs.copy()
                )
                callback(progress)

            # Use a test file URL - this would need to be configured per node
            test_url = f"http://{node.get('host')}:{node.get('port')}/testfile"  # Placeholder
            speed_result = self.test_download_speed(test_url)

            # Combine results
            result = SpeedTestResult(
                success=True,
                latency=latency_result.latency,
                download_speed=speed_result.download_speed
            )

            if callback:
                progress = SpeedTestProgress(
                    stage="completed",
                    message="测试完成",
                    logs=self.logs.copy()
                )
                callback(progress)

            return result

        except Exception as e:
            return SpeedTestResult(success=False, error=str(e))
        finally:
            self.is_running = False

    def abort(self):
        """Abort current test"""
        self.is_running = False