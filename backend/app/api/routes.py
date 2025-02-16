# backend/app/api/routes.py
from flask import Blueprint, jsonify
from app.services import ocr, normalizer, swudb

api = Blueprint('api', __name__)

@api.route('/scan', methods=['POST'])
def scan_card():
    """
    scan_card endpoint
    
    This is the endpoint where you 
    
    ---
    responses:
        200:
            description: A successful response
    """
    # Your existing scanning logic here
    return dict({
        "Message": "Scan not implemented"
    })
