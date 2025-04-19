# Use a Python 3.12 runtime
FROM python:3.12-slim

# Setting the working directory in the container
WORKDIR /app

# Copying the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size, --upgrade pip is good practice to make sure everything is up to date.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
# Note please be careful of what port you expose.
# This is the port Flask is running on in app.py
EXPOSE 5000

# Define environment variables. This step is optional.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application when the container launches
# Use gunicorn for production later, but flask run is fine for now
# Use CMD ["flask", "run"] or directly python app.py
CMD ["python", "app.py"]