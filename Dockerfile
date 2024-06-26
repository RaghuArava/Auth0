FROM python:3.9

# Set the working directory in the container
WORKDIR /app


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run ./auth0_crud.py when the container launches
ENTRYPOINT ["python3", "./auth0_crud.py"]
