# Use the official Python image as the base image
FROM python:3.12-slim


# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U streamlit

# Copy the rest of the application code to the container
COPY . .

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports for Flask and Streamlit
EXPOSE 8000 8501

#ENV vars
ENV GOOGLE_API_KEY=

# Command to run the supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
