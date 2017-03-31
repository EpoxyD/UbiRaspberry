#!/usr/bin/python

#import pifacedigitalio
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import _thread

app = Flask(__name__)
api = Api(app)

CHICKS_TOTAL = 9
CHICKS_INSIDE = 0

class Hen_House(Resource):
    def get(self, total_chicks):
        global CHICKS_TOTAL
        global CHICKS_INSIDE
        
        if total_chicks == 'add':
            CHICKS_TOTAL = CHICKS_TOTAL + 1
        elif total_chicks == 'remove':
            CHICKS_TOTAL = CHICKS_TOTAL - 1
        
        return {'total_chicks': CHICKS_TOTAL, 'total_inside': CHICKS_INSIDE}


api.add_resource(Hen_House, '/change-count/<string:total_chicks>')


if __name__ == "__main__":
    app.run()
    print('________________________hallo________________________')
