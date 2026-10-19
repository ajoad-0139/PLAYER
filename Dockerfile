# The tag must match the playwright version in requirements.txt.
FROM mcr.microsoft.com/playwright/python:v1.64.0-noble

WORKDIR /app

# Copy requirements first so Docker caches the install layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# pytest.ini already holds all report and artifact options
CMD ["pytest"]