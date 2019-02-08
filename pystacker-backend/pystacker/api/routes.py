from .views import preview_stack, graphql_query, graphql_subscribe
import aiohttp.web


def init_routes(app: aiohttp.web.Application):
    app.router.add_post('/template_yml', preview_stack)

    app.router.add_get('/query', graphql_query)
    app.router.add_post('/query', graphql_query)
    app.router.add_get('/subscribe', graphql_subscribe)