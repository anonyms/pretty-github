# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt || true

# Command to run the script (replace script.py with your actual file)
CMD ["python", "make-commits.py"]