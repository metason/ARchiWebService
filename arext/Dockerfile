# Create our image based on Python 3.8
FROM python:3.6

# Expose ports
EXPOSE 5000

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering
ENV PYTHONUNBUFFERED 1

# Install Gunicorn
RUN apt-get update
RUN apt-get install -y virtualenv
## Install pip3 and update

#create virtual env
RUN virtualenv ve
ENV PATH="/ve/bin:$PATH"



# Update pip
#Install requirements using pip
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Set working directory and addour Flask API files
WORKDIR /arext
ADD . /arext

ENV FLASK_APP controllers.py
