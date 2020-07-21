import logging
from flask import request, jsonify

from led_api.models import Color, ColorSchema
from led_api import app,db
log = logging.getLogger(__name__)


#GET: return array of colors
#POST: Add new color or update if existing
#DELETE: Delete color from database
@app.route('/colors', methods = ['GET', 'POST', 'DELETE'])
def res_colors():
    #add or update new color
    if request.method == 'POST':
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return ('failed: Content-type must be application/json', 401)
        data = request.get_json()
        item_name = data.get('name')
        item_value = data.get('value')
        id = 0
        if not item_name or not item_value:
            return ('failed: Name or value attribute not found', 400)
        #insert new record in database or update if exists
        try:
            col=db.session.query(Color).filter_by(name=item_name).first()
            if col:
                col.value = item_value
            else:
                db.session.add(Color(name=item_name, value=item_value))
            col=db.session.query(Color).filter_by(name=item_name).first()
            id = col.id
            db.session.commit()
        except:
            log.error('Could not insert new color into database')
            return ('failed: Could not insert or update color', 500)
        if (id == 0):
            return ('failed: Could not insert or update color', 500)
        return jsonify(id)
    #delete color
    if request.method == 'DELETE':
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return ('failed: Content-type must be application/json', 401)
        data=request.get_json()
        item_name = data.get('name')
        item_id = data.get('id')
        id = 0
        if not item_name and not item_id:
            return ('failed: No name or id attribute found', 400)
        #delete record from database
        try:
            if item_id:
                c = db.session.query(Color).get(item_id)
            elif item_name:
                c = db.session.query(Color).filter_by(name=item_name).first()
            if c:
                db.session.delete(c)
                db.session.commit()
                id = c.id
            else:
                log.error("Could not delete color from database: Color didn't exist")
                return ('failed: Color not existing in data base', 410)
        except:
            log.error('Could not delete color from database')
            return ('failed: Could not delete color', 500)
        if (id == 0):
            return ('failed: Could not delete color', 500)
        return jsonify(id)
    #list existing colors
    else:
        dictc = []
        recs = db.session.query(Color).all()
        #Convert Records class from Color to dictionaries
        dictc = ColorSchema(many=True).dump(recs)
        return jsonify(dictc)
