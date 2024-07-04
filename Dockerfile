# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim


# Install python packagres
RUN apt-get -y update
RUN apt-get -y install git

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN mkdir /app_data
#COPY . /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /workspaces/DentalClinicCalculator/app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app_data
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "/workspaces/DentalClinicCalculator/app/run.py "]
