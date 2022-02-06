from io import BytesIO
from .risk_database import RiskDB
from .parse_file import ParseFile
from aiohttp import web

class Handler:
    def __init__(self):
        self.db = RiskDB()
        self.parsefunc = ParseFile(self.db)

    async def handle_user_check(self, request):
        username = request.rel_url.query['username']
        if username in self.db.knownUserList:
            return web.Response(text="true")
        else:
            return web.Response(text="false")

    async def handle_ip_check(self, request):
        ip = request.rel_url.query['ip']
        if ip in self.db.knownIPList:
            return web.Response(text="true")
        else:
            return web.Response(text="false")

    async def handle_device_check(self, request):
        device = request.rel_url.query['device']
        if ip in self.db.knownDeviceList:
            return web.Response(text="true")
        else:
            return web.Response(text="false")

    async def handle_internal_check(self, request):
        ip = request.rel_url.query['ip']
        if "10.97.2." in ip:
            return web.Response(text="true")
        else:
            return web.Response(text="false")

    async def handle_succ_logindate(self, request):
        username = request.rel_url.query['username']
        if username in self.db.successfulLoginDict.keys():
            timestamp = self.parsefunc.parse_unixtime(self.db.successfulLoginDict[username])
            return web.Response(text=str(timestamp))
        else:
            return web.Response(text="No record for this user!")

    async def handle_fail_logindate(self, request):
        username = request.rel_url.query['username']
        if username in self.db.failedLoginDict.keys():
            timestamp = self.parsefunc.parse_unixtime(self.db.failedLoginDict[username])
            return web.Response(text=str(timestamp))
        else:
            return web.Response(text="No record for this user!")

    async def handle_fail_logincount(self, request):
        count = self.db.failedLoginCount
        return web.Response(text=str(count))

    async def handle_log(self, request):
        async for obj in (await request.multipart()):
            if obj.filename is not None:  # To pass non-files
                file = BytesIO(await obj.read())
                file_content = file.getvalue().decode('utf-8')
                self.parsefunc.parse_content(file_content.split('\n'))
        return web.Response(text='Log uploaded!', content_type="text/html")
