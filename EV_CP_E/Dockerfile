FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "app/__init__.py"]
CMD ["5000", "127.0.0.1", "6000", "CP000"]