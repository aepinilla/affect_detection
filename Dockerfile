# 1 - set base image
FROM python:3.10.4
# 2 - set the working directory
WORKDIR /affect_detection
# 3 - copy files to the working directory
COPY . .
# 4 - install dependencies
RUN apt-get --force-yes update \
    && apt-get --assume-yes install r-base-core
RUN pip install -r requirements.txt
# 5 - command that runs when container starts
CMD ["python", "/affect_detection/main.py"]