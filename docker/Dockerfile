FROM supervisely/import-export:6.73.504

WORKDIR /app

COPY dev_requirements.txt ./dev_requirements.txt
RUN pip install --no-cache-dir -r dev_requirements.txt

CMD ["python3", "src/main.py"]