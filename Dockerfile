# STEP 1: Use official Python slim image (small, clean)
FROM python:3.11-slim

# STEP 2: Set working directory inside the container
WORKDIR /app

# STEP 3: Install system dependencies needed for MySQL client and building
RUN apt-get update && apt-get install -y \
    libmariadb-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# STEP 4: Copy requirements first for better caching
COPY requirements.txt .

# STEP 5: Upgrade pip and install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# STEP 6: Copy the rest of your Django project files
COPY . .

# STEP 7: Collect static files (makes Django static assets ready)
RUN python manage.py collectstatic --noinput

# STEP 8: Expose port 8000 for the app
EXPOSE 8000

# STEP 9: Run your app with Gunicorn (production-ready WSGI server)
CMD ["gunicorn", "bharathi_project.wsgi:application", "--bind", "0.0.0.0:8000"]
