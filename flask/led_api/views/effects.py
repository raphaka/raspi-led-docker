import logging
from flask import request,jsonify

from led_api.models import Effect,EffectSchema
from led_api import app,db
log = logging.getLogger(__name__)

#GET: return array of effects
#POST: Add new effect or update if existing
#DELETE: Delete effect from database
@app.route('/effects', methods = ['GET', 'POST', 'DELETE'])
def res_effects():
    #add or update new effect
    if request.method == 'POST':
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return ('failed: Content-type must be application/json', 401)
        data = request.get_json()
        item_name = data.get('name')
        item_value = str(data.get('value')) #stored as a str representation of the list of json elements
        id = 0
        if not item_name or not item_value:
            return ('failed: Name or value attribute not found', 400)
        #insert new record in database or update if exists
        try:
            col=db.session.query(Effect).filter_by(name=item_name).first()
            if col:
                col.value = item_value
            else:
                db.session.add(Effect(name=item_name, value=item_value))
            col=db.session.query(Effect).filter_by(name=item_name).first()
            id = col.id
            db.session.commit()
        except:
            log.error('Could not insert new effect into database')
            return ('failed: Could not insert or update effect', 500)
        if (id == 0):
            return ('failed: Could not insert or update effect', 500)
        return jsonify(id)
    #delete effect
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
                c = db.session.query(Effect).get(item_id)
            elif item_name:
                c = db.session.query(Effect).filter_by(name=item_name).first()
            if c:
                db.session.delete(c)
                db.session.commit()
                id = c.id
            else:
                log.error("Could not delete effect from database: Effect didn't exist")
                return ('failed: Effect not existing in data base', 410)
        except:
            log.error('Could not delete effect from database')
            return ('failed: Could not delete effect', 500)
        if (id == 0):
            return ('failed: Could not delete effect', 500)
        return jsonify(id)
    #list existing effects
    else:
        dictc = []
        recs = db.session.query(Effect).all()
        #Convert Records class from Effect to dictionaries
        dictc = EffectSchema(many=True).dump(recs)
        return jsonify(dictc)
