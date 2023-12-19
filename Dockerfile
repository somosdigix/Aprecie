# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /aprecie

# Copy the current directory contents into the container at /app
COPY . /aprecie

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /aprecie/requirements.txt \
    pip install pymsteams

# Expose port 8000 for the Django development server
EXPOSE 8080

# Define environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED 1

# CMD specifies the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
