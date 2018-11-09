import logging
import asyncio

from .protocol8743 import NewFocus8743Protocol

logger = logging.getLogger(__name__)


class NewFocus8743TCP(NewFocus8743Protocol):
    eol_write = b"\r"
    eol_read = b"\r\n"

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    @classmethod
    async def connect(cls, host, port=23, **kwargs):
        """Connect to a Newfocus/Newport 8742 controller over Ethernet/TCP.

        Args:
            host (str): Hostname or IP address of the target device.

        Returns:
            NewFocus8742: Driver instance.
        """
        reader, writer = await asyncio.open_connection(host, port, **kwargs)
        # undocumented? garbage?
        v = await reader.read(6)
        logger.debug("identifier/serial (?): %s", v)
        return cls(reader, writer)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        self._writer.close()

    def _writeline(self, cmd):
        self._writer.write(cmd.encode() + self.eol_write)

    async def _readline(self):
        r = await self._reader.readline()
        assert r.endswith(self.eol_read)
        return r[:-2].decode()
