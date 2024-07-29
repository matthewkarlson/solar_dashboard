# Use the official Python 3.8 slim image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /workspace

# Install dependencies directly
RUN pip install --no-cache-dir scikit-learn pandas numpy pyautogen
#copy testdata.csv into the workspace directory in the container
COPY test_data.csv /app/data/

# Specify the command to keep the container running
CMD ["tail", "-f", "/dev/null"]
