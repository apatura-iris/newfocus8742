import pytest
import asyncio

from newfocus8742.tcp8743 import NewFocus8743TCP

loop = asyncio.new_event_loop()

async def test_connect():
    conn = await NewFocus8743TCP.connect("192.168.1.101")
    with conn:
        identity = await conn.identify()
        manufacturer, model, version, date, serial = identity.split()
        print(manufacturer, model, version, date, serial)
        print(await conn.get_acceleration(1))
        print(await conn.position_search_done(1))


loop.run_until_complete(test_connect())
#pytest.main()