FROM python:3.10-slim

WORKDIR /app

COPY extract_outline.py /app/
RUN pip install --no-cache-dir pdfminer.six


COPY . .

CMD ["python", "extract_outline.py"]
