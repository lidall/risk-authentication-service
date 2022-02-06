import pytest
from risk_authentication.server_handler import Handler
from aiohttp import web

handler = Handler()
handler.db.knownIPList = ['10.192.2.2']
handler.db.knownUserList = ['Bob']
handler.db.knownDeviceList = ['3deakcskae4cmsk']
handler.db.successfulLoginDict = {'Bob': 1644151100.012}
handler.db.failedLoginDict = {'Bob': 1644151199.341}
handler.db.failedLoginCount = 5


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
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


async def test_handle_user_check(cli):
    resp = await cli.get('/risk/isuserknown?username=Bob')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isuserknown?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'false'


async def test_handle_device_check(cli):
    resp = await cli.get('/risk/isdeviceknown?device=3deakcskae4cmsk')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isdeviceknown?device=K3deakcskae4')
    assert resp.status == 200
    assert await resp.text() == 'false'


async def test_handle_ip_check(cli):
    resp = await cli.get('/risk/isipknown?ip=10.192.2.2')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isipknown?ip=10.192.4.10')
    assert resp.status == 200
    assert await resp.text() == 'false'


async def test_handle_succ_logindate(cli):
    resp = await cli.get('/risk/lastsuccessfullogindate?username=Bob')
    assert resp.status == 200
    assert await resp.text() == '2022-02-06T12:38:20.012000Z'

    resp = await cli.get('/risk/lastsuccessfullogindate?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'No record for this user!'


async def test_handle_fail_logindate(cli):
    resp = await cli.get('/risk/lastfailedlogindate?username=Bob')
    assert resp.status == 200
    assert await resp.text() == '2022-02-06T12:39:59.341000Z'

    resp = await cli.get('/risk/lastfailedlogindate?username=Kevin')
    assert resp.status == 200
    assert await resp.text() == 'No record for this user!'


async def test_handle_fail_logincount(cli):
    resp = await cli.get('/risk/failedlogincountlastweek')
    assert resp.status == 200
    assert await resp.text() == '5'


async def test_handle_internal_check(cli):
    resp = await cli.get('/risk/isipinternal?ip=10.97.2.10')
    assert resp.status == 200
    assert await resp.text() == 'true'

    resp = await cli.get('/risk/isipinternal?ip=10.97.4.50')
    assert resp.status == 200
    assert await resp.text() == 'false'
