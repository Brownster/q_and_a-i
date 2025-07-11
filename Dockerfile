FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .
COPY . .
ENTRYPOINT ["python", "generate_dataset.py"]
CMD ["objectives.txt", "exam.json"]
