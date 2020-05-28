import logging
from aiohttp import web, ClientSession





logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
routes = web.RouteTableDef()


# test route
# curl -X POST http://localhost:8080/plants/v1/test_post
@routes.post("/plants/v1/test_post")
async def test_post(request):
	logging.info("test post")
	return web.Response()

# test route
# curl -X GET http://localhost:8080/plants/v1/test_get
@routes.get("/plants/v1/test_get")
async def test_post(request):
	logging.info("test get")
	return web.Response()


def main():

	app = web.Application()
	app.add_routes(routes)
	logging.info("server initialized")
	print('server bh')
	web.run_app(app)




if __name__ == "__main__":
	print('here1')
	main()
