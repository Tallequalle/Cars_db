from aiohttp import web
import pymongo
import configparser
import aiohttp_jinja2
import jinja2
import os
from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read("config.ini")
routes = web.RouteTableDef()
app = web.Application()


aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)


def connect_db():
    con = pymongo.MongoClient('mongodb://localhost:27017')
    col = con['test_db']['user']
    return col


@routes.post('/update')
async def update(request):
    data = await request.post()
    id_record = data['id']
    field = data['field']
    value = data['value']
    col = connect_db()
    col.update_one({"_id": ObjectId(id_record)}, {"$set": {field: value}})
    location = request.app.router['last_record'].url_for()
    return web.HTTPFound(location=location)


@routes.post('/my-handling-form-page')
async def handling_form_page(request):
    data = await request.post()
    manufacturer = data['manufacturer']
    model = data['model']
    year = data['year']
    color = data['color']
    vin = data['vin']
    col = connect_db()
    qry = {'manufacturer': f'{manufacturer}', 'model': f'{model}',
           'year': f'{year}', 'color': f'{color}', 'vin': f'{vin}'}
    col.insert_one(qry)
    location = request.app.router['insert'].url_for()
    return web.HTTPFound(location=location)


@aiohttp_jinja2.template('users_data.html')
async def insert():
    return {}


@routes.post('/delete_record')
async def delete_record(request):
    col = connect_db()
    record = col.find_one(sort=[('_id', pymongo.DESCENDING)])
    col.delete_one({"_id": record['_id']})
    location = request.app.router['last_record'].url_for()
    return web.HTTPFound(location=location)


@aiohttp_jinja2.template('last_record.html')
async def last_record(request):
    col = connect_db()
    record = [col.find_one(sort=[('_id', pymongo.DESCENDING)])]
    html = open('templates/last_record.html').read()
    template = jinja2.Template(html)
    # Render HTML Template String
    html_template_string = template.render(userslist=record)
    return web.Response(text=html_template_string, content_type='text/html')


@aiohttp_jinja2.template('index.html')
async def all_data(request):
    col = connect_db()
    data = [row for row in col.find()]
    html = open('templates/index.html').read()
    template = jinja2.Template(html)
    # Render HTML Template String
    html_template_string = template.render(userslist=data)
    return web.Response(text=html_template_string, content_type='text/html')


app.router.add_get('/insert', insert, name='insert')
app.router.add_get('/all_data', all_data, name='all_data')
app.router.add_get('/last_record', last_record, name='last_record')
app.add_routes(routes)
web.run_app(app)
