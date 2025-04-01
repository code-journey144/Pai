from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# List of supported domains
SUPPORTED_DOMAINS = [
    "codex", "relzhub", "mediafire", "pastebin", "pastedrop", "justpaste", 
    "pastecanyon", "mboost", "rekonise", "socialwolvez", "sub2get", 
    "sub2unlock.com", "sub2unlock.net", "sub4unlock.com", "adfoc.us", 
    "unlocknow.net", "ldnesfspublic.org", "link.rbscripts.net"
]

# Route to get supported domains
@app.route('/supported', methods=['GET'])
def supported_domains():
    return jsonify({
        "supported_domains": SUPPORTED_DOMAINS
    })

@app.route('/bypass', methods=['GET'])
def api_bypass():
    # Get the URL parameter from the query string
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    start_time = time.time()

    try:
        # Check if the URL matches any of the supported domains
        if any(domain in url for domain in SUPPORTED_DOMAINS):
            # Request to Solar-X API (or any other bypass API you want to use)
            response = requests.get(f'https://api.solar-x.top/api/v3/bypass?url={url}', timeout=10)
            response.raise_for_status()  # Raise error for non-2xx status codes
            data = response.json()

            # Extract 'result' and 'time', and add 'credit'
            result = data.get("result")
            time_value = data.get("time")

            return jsonify({
                "result": result,
                "time": time_value,
                "credit": "Made by MysticMoth"
            })
        else:
            return jsonify({
                "error": "URL domain not supported. Please use supported domains."
            }), 400

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 408

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to bypass URL: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
