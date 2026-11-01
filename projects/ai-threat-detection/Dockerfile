FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY models/ models/
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "-c", "import sys; sys.path.insert(0, 'src'); import api; api.app.run(host='0.0.0.0', port=5000)"]
