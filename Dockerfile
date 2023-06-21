FROM python
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /
# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
# Copy project
COPY . /