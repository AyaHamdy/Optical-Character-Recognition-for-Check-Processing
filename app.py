from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import ocrengine

app = Flask(__name__)

ocr_engine = ocrengine.create_ocr()

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}),400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}),400

    if file:
        file.save(file.filename)
        ocr_result=ocr_engine(file.filename)
        return jsonify({'ocr_result': ocr_result}),200

    return jsonify({'error': 'An error occurred during file processing'}),404

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "OCR API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
