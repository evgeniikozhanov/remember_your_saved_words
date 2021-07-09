import json

import pytest

from aiohttp import ClientSession


@pytest.mark.asyncio
async def test_upload_file():
    data = {'filename': 'saved_translations_test.csv'}
    async with ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/upload/", data=json.dumps(data).encode()) as resp:
            assert resp.status == 200, str(resp.status)
            response = await resp.json()
            assert response.get('ok')
            assert not response.get('errors', [])
