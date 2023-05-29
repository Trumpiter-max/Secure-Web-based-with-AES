FROM ubuntu:20.04

# Install dependencies
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata 
RUN apt-get install -y apt-transport-https build-essential gcc make wget curl libglib2.0-0
RUN apt-get install -y musl-dev libffi-dev binutils openssl subversion m4 libssl-dev libgmp-dev libgmp3-dev flex bison
RUN apt-get install -y python3 python3-dev python3-pip python3-setuptools python3-wheel python-openssl

# Basic setup
ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/
ADD . /var/www/

# Install PBC from source 
RUN cd /var/www/lib/pbc-0.5.14 && ./configure LDFLAGS="-lgmp" && make && make install && ldconfig
# Install libssl
RUN chmod +x /var/www/lib/libssl1.0.0_1.0.2n-1ubuntu5.12_amd64.deb && dpkg -i /var/www/lib/libssl1.0.0_1.0.2n-1ubuntu5.12_amd64.deb
# Install cpabe from source
RUN cd /var/www/lib/cpabe && ./cpabe-setup

# Set some require packages
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pip setuptools wheel
RUN pip install -r requirements.txt

RUN groupadd -g $GROUP_ID www
RUN adduser --system --uid $USER_ID --group www --shell /bin/sh 
USER www

EXPOSE 5000

# Run without nginx
# CMD ["python3", "app.py"] 

# Run with nginx
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "wsgi:app"]
