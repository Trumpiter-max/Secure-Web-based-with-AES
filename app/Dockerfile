FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y apt-transport-https build-essential gcc make tar\
    musl-dev libffi-dev openssl subversion m4 libssl-dev libgmp-dev libgmp3-dev flex bison\
    python3 python3-dev python3-pip python3-setuptools python3-wheel 

# Basic setup
ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/
ADD . /var/www/

# Copy some libraries

# Set some require packages
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel 
RUN pip install -r requirements.txt

RUN groupadd -g $GROUP_ID www
RUN adduser --system --uid $USER_ID --group www --shell /bin/sh 
USER www

EXPOSE 5000

CMD ["python3", "app.py"]
