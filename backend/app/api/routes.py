# backend/app/api/routes.py
from flask import Blueprint, jsonify
from app.services import ocr, normalizer, swudb

api = Blueprint('api', __name__)

@api.route('/scan', methods=['POST'])
def scan_card():
    # Your existing scanning logic here
    pass
