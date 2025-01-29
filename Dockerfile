# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Git (needed for some dependencies)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set Git user details using environment variables
ARG GIT_USER
ARG GIT_EMAIL
RUN echo "Git User: $GIT_USER" && echo "Git Email: $GIT_EMAIL"  # Print the variables
RUN git config --global user.name "$GIT_USER" \
    && git config --global user.email "$GIT_EMAIL"

# Copy the current directory contents into the container
COPY . /app

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt || true

# Command to run the script (replace script.py with your actual file)
CMD ["python", "make-commits.py"]