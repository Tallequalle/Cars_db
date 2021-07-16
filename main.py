import os
import configparser
from bson.objectid import ObjectId
import pymongo
import jinja2
import aiohttp_jinja2
from aiohttp import web

# creating configuration, routes and application objects
config = configparser.ConfigParser()
config.read("config.ini")
routes = web.RouteTableDef()
app = web.Application()

# setting the template directory
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)


# database connection function
def connect_db():
    con = pymongo.MongoClient(config['Database']['URL_database'])
    col = con[config['Database']['db_name']][config['Database']['collection']]
    return col


# checking the uniqueness of vin in the database
def vin_uniqueness_check(vin):
    col = connect_db()
    record_by_vin = col.find({'vin': vin})
    # if there is an error when accessing the cursor field, then there is no record with this vin
    try:
        record_vin = record_by_vin[0]['vin']
        return False
    except Exception:
        return True


# processing a data update request
@routes.post('/update')
async def update(request):
    data = await request.post()
    # getting data from a request
    id_record = data['id']
    field = data['field']
    value = data['value']
    col = connect_db()
    # vin uniqueness check
    if field == 'vin' and not vin_uniqueness_check(value):
        location = request.app.router['last_record'].url_for()
        return web.HTTPFound(location=location)
    # updating data in the database
    col.update_one({"_id": ObjectId(id_record)}, {"$set": {field: value}})
    location = request.app.router['last_record'].url_for()
    return web.HTTPFound(location=location)


# data update processing
@routes.post('/submit_handling')
async def handling_form_page(request):
    data = await request.post()
    # getting data from a request
    manufacturer = data['manufacturer']
    model = data['model']
    year = data['year']
    color = data['color']
    vin = data['vin']
    col = connect_db()
    # vin uniqueness check
    if vin_uniqueness_check(vin):
        qry = {'manufacturer': f'{manufacturer}', 'model': f'{model}',
           'year': f'{year}', 'color': f'{color}', 'vin': f'{vin}'}
        # adding to the database
        col.insert_one(qry)
    location = request.app.router['insert'].url_for()
    return web.HTTPFound(location=location)


# displaying a template for adding a user
@aiohttp_jinja2.template('users_data.html')
async def insert(request):
    return {}


# deleting a record from the database
@routes.post('/delete_record')
async def delete_record(request):
    col = connect_db()
    # search for the last entry
    record = col.find_one(sort=[('_id', pymongo.DESCENDING)])
    col.delete_one({"_id": record['_id']})
    location = request.app.router['last_record'].url_for()
    return web.HTTPFound(location=location)


# display of the last record from the database
@aiohttp_jinja2.template('last_record.html')
async def last_record(request):
    col = connect_db()
    record = [col.find_one(sort=[('_id', pymongo.DESCENDING)])]
    html = open('templates/last_record.html').read()
    template = jinja2.Template(html)
    # Render HTML Template String
    html_template_string = template.render(userslist=record)
    return web.Response(text=html_template_string, content_type='text/html')


# displaying all data from the database
@aiohttp_jinja2.template('all_data.html')
async def all_data(request):
    col = connect_db()
    data = [row for row in col.find()]
    html = open('templates/all_data.html').read()
    template = jinja2.Template(html)
    # Render HTML Template String
    html_template_string = template.render(userslist=data)
    return web.Response(text=html_template_string, content_type='text/html')


# adding app routes
app.router.add_get('/insert', insert, name='insert')
app.router.add_get('/all_data', all_data, name='all_data')
app.router.add_get('/last_record', last_record, name='last_record')
app.add_routes(routes)
# application launch
web.run_app(app)
