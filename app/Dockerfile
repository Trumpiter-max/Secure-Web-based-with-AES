FROM ubuntu:18.04

# Install dependencies
RUN apt-get update -y
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata 
RUN apt-get install -y build-essential gcc git make wget curl libglib2.0-0 zlib1g-dev libncurses5-dev libnss3-dev libreadline-dev python3.7
RUN apt-get install -y musl-dev libffi-dev binutils openssl subversion m4 libssl-dev libgmp-dev libgmp3-dev flex bison libsqlite3-dev libffi-dev    
# Install Python package
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN apt-get install -y python3-pip python3-sphinx python3.7-dev python3-openssl

# Basic setup
ENV GROUP_ID=1000 \
    USER_ID=1000 

# Create working directory 
WORKDIR /var/www/
ADD . /var/www/

# Set some require packages
RUN pip3 install --upgrade pip
RUN pip3 install -r /var/www/requirements.txt

# Install GMP
RUN cd /var/www/resources/gmp-5.1.3 && ./configure --prefix="/usr/local" && make && make install && make check && ldconfig

# Install PBC
RUN cd /var/www/resources/pbc-0.5.14 && ./configure --prefix="/usr/local" CFLAGS="-I/usr/include" LDFLAGS="-L/usr/lib" && make && make install && ldconfig

# Install OpenSSL library
RUN cd /var/www/resources/openssl-1.1.1t && ./config --prefix="/usr/local" enable-ec_nistp_64_gcc_128\
    && make -j 8 && make install && ldconfig

# Install Charm Crypto
RUN cd /var/www/resources/charm-dev && ./configure.sh --python="/usr/bin/python3.7" --prefix="/usr/local" --enable-docs --static --extra-ldflags="-L/usr/lib" --extra-cflags="-I/usr/include"\
	&& make && make install && ldconfig && make test --include-dir="/usr/include" LD_LIBRARY_PATH="/usr/lib"

# Set user
RUN groupadd -g $GROUP_ID www
RUN adduser --system --uid $USER_ID --group www --shell /bin/sh 
USER www

EXPOSE 5000

# Start web service

# Run without nginx
# CMD ["python3", "wsgi.py"]

# Run with nginx
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "wsgi:app"]


