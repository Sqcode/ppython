from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def Hello():
    return 'Hello'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)  # 将5000替换为您想要使用的端口号

