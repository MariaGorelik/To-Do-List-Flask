# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR D:/Web/ToDoList

# Copy only the necessary files to the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Flask app will run
EXPOSE 5000

# Define the command to run your application
CMD ["python", "app.py"]