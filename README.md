
# OCR for Check Processing API

This is a Flask Api for performing OCR on uploaded images. The application uses the EASY OCR engine to extract text information from images.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```
2. Build the Docker image:

```bash
sudo docker build -t ocrapi:latest .
```

3. Run the Docker container:

```bash
docker run -p 5000:5000 ocrapi:latest
```

The application will be accessible at http://localhost:5000. You can use any API testing tool or write a simple client to send image files to the /ocr endpoint.

## API Endpoint

- POST /ocr
  -  Accepts an image file via a POST request.
  - Parameters:
    - file: Image file to be processed.
  - Returns JSON response:
    - If successful: {'ocr_result': 'Extracted text'}
    - If an error occurs: {'error': 'Error message'}

- Access Swagger Documentation:

    The API is documented using Swagger. Once the server is running, you can access the Swagger UI documentation at [http://localhost:5000/swagger/](http://localhost:5000/swagger/). This interface provides detailed information about the API endpoints and allows for interactive testing.

# Requirements
Make sure you have Docker installed on your machine.

# Docker Configuration

The Dockerfile uses the official Python 3.8 slim-buster image. It installs the required dependencies from the requirements.txt file and the Tesseract OCR for the Turkish language.

# Dependencies
 - Flask
 - easyocr
 - flask-swagger-ui
 - Pillow
 
# Enhancements
- Improve ocr results through enhancing the checks images quality using image processing techniques.
- Test different deep learning text detection and recognition models 


 

