# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Set the maintainer label (optional)
LABEL maintainer="Francesco <francesco.decampo@andovar.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local directory into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt using pip
RUN pip install -r requirements.txt

# Expose the port that your Streamlit app runs on (e.g., 8501)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "silence-manipulator.py"]