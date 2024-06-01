FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the command to fetch data and then start the application
CMD ["bash", "-c", "python data/fetch_data.py && python scripts/train_tokenizer.py && python scripts/tokenize_data.py && python scripts/train_model.py && python scripts/evaluate_model.py && python scripts/deploy_model.py"]
