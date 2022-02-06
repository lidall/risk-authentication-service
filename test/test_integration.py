import pytest
from risk_authentication.server_handler import Handler
from aiohttp import web

handler = Handler()


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_post('/log', handler.handle_log)
    app.router.add_get('/risk/isuserknown', handler.handle_user_check)
    app.router.add_get('/risk/isipknown', handler.handle_ip_check)
    app.router.add_get('/risk/isdeviceknown', handler.handle_device_check)
    app.router.add_get('/risk/lastsuccessfullogindate',
                       handler.handle_succ_logindate)
    app.router.add_get('/risk/lastfailedlogindate',
                       handler.handle_fail_logindate)
    app.router.add_get('/risk/failedlogincountlastweek',
                       handler.handle_fail_logincount)
    app.router.add_get('/risk/isipinternal', handler.handle_internal_check)
    return loop.run_until_complete(aiohttp_client(app))


async def test_integration(cli):
    with open('./test/client/data.txt', 'rb') as f:
        resp = await cli.post('/log', data={'key': f})
    assert resp.status == 200
    assert await resp.text() == 'Log uploaded!'

    resp = await cli.get('/risk/isuserknown?username=bob')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isuserknown?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'false'

    resp = await cli.get(
        '/risk/isdeviceknown?device=77bd2cb0a74e4ecc75d0e507eeb73731')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isdeviceknown?device=K3deakcskae4')
    assert resp.status == 200
    assert await resp.text() == 'false'

    resp = await cli.get('/risk/isipknown?ip=10.97.2.192')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isipknown?ip=10.192.4.10')
    assert resp.status == 200
    assert await resp.text() == 'false'

    resp = await cli.get('/risk/lastsuccessfullogindate?username=bob')
    assert resp.status == 200
    assert await resp.text() == '2021-04-27T11:10:42.198082Z'

    resp = await cli.get('/risk/lastsuccessfullogindate?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'No record for this user!'

    resp = await cli.get('/risk/lastfailedlogindate?username=bobUU')
    assert resp.status == 200
    assert await resp.text() == '2021-04-27T10:57:59.841657Z'

    resp = await cli.get('/risk/lastfailedlogindate?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'No record for this user!'

    resp = await cli.get('/risk/failedlogincountlastweek')
    assert resp.status == 200
    assert await resp.text() == '5'

    resp = await cli.get('/risk/isipinternal?ip=10.97.2.192')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isipinternal?ip=10.97.4.50')
    assert resp.status == 200
    assert await resp.text() == 'false'
