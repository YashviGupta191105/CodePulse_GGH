# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install system dependencies for C++ debugging
RUN apt update && apt install -y g++ cmake

# Create a tmp directory inside the container
RUN mkdir -p /app/tmp && chmod -R 777 /app/tmp

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
