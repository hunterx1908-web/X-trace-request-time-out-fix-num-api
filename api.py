import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime
import time

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# 🔥 Original API details
ORIGINAL_API_URL = "https://sbsakib.eu.cc/apis/num_info_v1"
ORIGINAL_KEY = "Adarsh_Aman-paid"

# 🔥 API Expiry Date (14 December 2099)
API_EXPIRY = "2099-12-14"

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
            "error": f"API expired on {API_EXPIRY}!",
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
    
    # 🔥 3 attempts with 8 sec timeout
    max_attempts = 3
    timeout_occurred = False
    
    for attempt in range(max_attempts):
        try:
            params = {
                'key': ORIGINAL_KEY,
                'num': num
            }
            response = requests.get(ORIGINAL_API_URL, params=params, timeout=8)
            
            # Agar rate limit (429) ya server error (5xx) ho toh retry
            if response.status_code == 429 or response.status_code >= 500:
                time.sleep(2)
                continue
            
            response.raise_for_status()
            data = response.json()
            
            # 🔥 Data mila ya nahi check karo
            if isinstance(data, dict):
                if data.get('total_results') == 0:
                    # 🔥 Number valid hai lekin data nahi hai
                    return jsonify({
                        "status": False,
                        "message": "No data found",
                        "developer": "@x_TRACEOWNER",
                        "credit": "@x_TRACEOWNER"
                    }), 404
                
                # Data mil gaya — clean response
                data.pop('developer', None)
                data['developer'] = '@x_TRACEOWNER'
                data['credit'] = '@x_TRACEOWNER'
                data['api_expires_on'] = API_EXPIRY
                
                return jsonify(data)
            
            # Agar data dict nahi hai toh bhi no data found
            return jsonify({
                "status": False,
                "message": "No data found",
                "developer": "@x_TRACEOWNER",
                "credit": "@x_TRACEOWNER"
            }), 404
            
        except requests.exceptions.Timeout:
            timeout_occurred = True
            if attempt < max_attempts - 1:
                time.sleep(2)
                continue
            # 🔥 Timeout ke baad bhi "No data found" nahi, "Request timeout" bhejo
            return jsonify({
                "status": False,
                "message": "Request timeout. Please try again later.",
                "developer": "@x_TRACEOWNER",
                "credit": "@x_TRACEOWNER"
            }), 504
            
        except requests.exceptions.ConnectionError:
            if attempt < max_attempts - 1:
                time.sleep(2)
                continue
            return jsonify({
                "status": False,
                "message": "Request timeout. Please try again later.",
                "developer": "@x_TRACEOWNER",
                "credit": "@x_TRACEOWNER"
            }), 504
            
        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(2)
                continue
            return jsonify({
                "status": False,
                "message": "No data found",
                "developer": "@x_TRACEOWNER",
                "credit": "@x_TRACEOWNER"
            }), 404
    
    # Agar 3 attempts ke baad bhi kuch nahi mila
    return jsonify({
        "status": False,
        "message": "Request timeout. Please try again later.",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 504

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
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))