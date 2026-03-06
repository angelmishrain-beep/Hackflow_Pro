FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 8501

CMD ["sh", "-c", "uvicorn h_backend:app --host 0.0.0.0 --port 8000 & streamlit run h_frontend.py --server.port 8501 --server.address 0.0.0.0"]