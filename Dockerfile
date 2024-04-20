FROM python:3.11
# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application contents
COPY weatherapp/ ./weatherapp/
# Switch to a non-root user
RUN useradd --uid 1000 weather && chown -R weather /app
USER weather
# Run the service
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "weatherapp:app"]