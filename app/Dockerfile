FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y apt-transport-https build-essential gcc make wget curl\
    musl-dev libffi-dev binutils openssl subversion m4 libssl-dev libgmp-dev libgmp3-dev flex bison\
    python3 python3-dev python3-pip python3-setuptools python3-wheel python-openssl

# Basic setup
ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/
ADD . /var/www/

# Copy certificates
RUN mkdir -p /var/www/certificates
COPY ../certificates/* /var/www/certificates/

# Install PBC from source 
RUN cd /var/www/lib/pbc-0.5.14 && ./configure LDFLAGS="-lgmp" && make && make install && ldconfig

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
