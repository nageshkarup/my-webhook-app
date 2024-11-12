from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy bearer token for webhook testing
BEARER_TOKEN = "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"

last_three_webhook_data = []


@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header == f"Bearer {BEARER_TOKEN}":

            data = request.get_json()

            # Store the data (keep only the last 3 records)
            if len(last_three_webhook_data) >= 3:
                last_three_webhook_data.pop(0)

            last_three_webhook_data.append(data)

            print("Received webhook data:", data)
            return jsonify({"message": "Webhook received successfully"}), 200
        else:
            return jsonify({"error": "Unauthorized"}), 401

    # Handle GET request
    elif request.method == 'GET':
        if last_three_webhook_data:
            return jsonify({
                "webhook_data": last_three_webhook_data
            }), 200
        else:
            return jsonify({"message": "No webhook data available"}), 200

    elif request.method == 'HEAD':
        return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
