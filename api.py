import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# Original API details
ORIGINAL_API_URL = "https://sbsakib.eu.cc/apis/num_info_v1"
ORIGINAL_KEY = "Adarsh_Aman-paid"

# 🔥 API Expiry Date (4 din — aaj included)
API_EXPIRY = "2092-11-25"

def is_expired():
    try:
        expiry = datetime.strptime(API_EXPIRY, "%Y-%m-%d")
        return datetime.utcnow() > expiry
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "Number Info API is working! (X-TRACE Edition)",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "expires_on": API_EXPIRY,
        "status": "Active" if not is_expired() else "Expired",
        "endpoints": {
            "info": "/apis/num_info_v1?key=YOUR_KEY&num=PHONE_NUMBER"
        },
        "example": "/apis/num_info_v1?key=@x_TRACEOWNER&num=9006640786"
    })

@app.route('/apis/num_info_v1')
def num_info():
    # 🔥 Check if API is expired
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}! Please contact support.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    # Get parameters
    key = request.args.get('key')
    num = request.args.get('num')
    
    # 🔐 Key verify
    if not key:
        return jsonify({
            "status": False,
            "error": "Missing API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
        
    if key != VALID_KEY:
        return jsonify({
            "status": False,
            "error": "Invalid API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 401
    
    if not num:
        return jsonify({
            "status": False,
            "error": "Enter Mobile Number",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Validate phone number (10 digits)
    if not num.isdigit() or len(num) != 10:
        return jsonify({
            "status": False,
            "error": "Invalid phone number! Must be 10 digits.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Forward to original API
    params = {
        'key': ORIGINAL_KEY,
        'num': num
    }
    
    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            # Check if total_results is 0 (no data found)
            if data.get('total_results') == 0:
                return jsonify({
                    "status": False,
                    "message": "No data found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
            
            # Remove original developer
            data.pop('developer', None)
            
            # Add our branding
            data['developer'] = '@x_TRACEOWNER'
            data['credit'] = '@x_TRACEOWNER'
            data['api_expires_on'] = API_EXPIRY
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "message": "Request timeout. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404

@app.route('/apis/num_info_v1/<path:path>')
def catch_all(path):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))