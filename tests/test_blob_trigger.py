import io
import logging
from function_app import BlobTrigger

class FakeInputStream:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data
        self.length = len(data)

    def read(self):
        return self._data


def test_blob_trigger_logs_blob_info(caplog):
    fake_blob = FakeInputStream(
        name="victorcontainer/test.txt",
        data=b"hello blob"
    )

    with caplog.at_level(logging.INFO):
        BlobTrigger(fake_blob)

    assert "Python blob trigger function processed blob" in caplog.text
    assert "test.txt" in caplog.text
    assert "bytes" in caplog.text
