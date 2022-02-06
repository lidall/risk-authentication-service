from aiohttp import web
from risk_authentication import Handler

def main():
    handler = Handler()
    app = web.Application()
    app.add_routes([web.get('/risk/isuserknown', handler.handle_user_check),
                    web.get('/risk/isipknown', handler.handle_ip_check),
                    web.get('/risk/isdeviceknown', handler.handle_device_check),
                    web.get('/risk/isipinternal', handler.handle_internal_check),
                    web.get('/risk/lastsuccessfullogindate', handler.handle_succ_logindate),
                    web.get('/risk/lastfailedlogindate', handler.handle_fail_logindate),
                    web.get('/risk/failedlogincountlastweek', handler.handle_fail_logincount),
                    web.post('/log', handler.handle_log)])
    web.run_app(app)


if __name__ == "__main__":
    main()
