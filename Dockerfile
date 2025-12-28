FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir google-api-python-client google-auth
CMD ["python","cloud_entrypoint.py"]
