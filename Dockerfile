# Use official Python image as the base
FROM python:3.11

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Create and activate a virtual environment inside Docker
RUN python -m venv /app/venv
RUN /bin/bash -c "source /app/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the Streamlit app within the virtual environment
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
