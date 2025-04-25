import traceback
import requests
import json
from flask import jsonify, Blueprint, request
from lib.Stech import Logger

main_ejemplo = Blueprint('main_ejemplo', __name__)

@main_ejemplo.route('/', methods=['GET'])
def ejemplo():
    try:
        return jsonify({'message': 'Hello World', 'success': True}), 200
    
    except Exception as e:
        Logger.error(traceback.format_exc()) 
        return jsonify({'message': 'Error en el servidor', 'success': False}), 500