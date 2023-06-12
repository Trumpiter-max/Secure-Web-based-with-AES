# Secure Web based with AES

## Table of contents

- [Secure Web based with AES](#secure-web-based-with-aes)
  - [Table of contents](#table-of-contents)
  - [Get started](#get-started)
    - [Requirements](#requirements)
      - [Libraries](#libraries)
    - [How to use](#how-to-use)
  - [Self sign certificate](#self-sign-certificate)
  - [References](#references)

---

## Get started

### Requirements

- Python version: 3.7.x
- OS environment: Ubuntu 18.04 LTS linux
- Database engine: MongoDB latest
- Webserver: Nginx latest

#### Libraries

- PBC version 0.5.14
- GMP version 5.1.3
- OpenSSL version 1.1.1t
- Charm Dev version

### How to use

Run container

```sh
  docker-compose up 
```

Close docker-compose

```sh
  docker-compose down 
```

## Self sign certificate

```sh
  openssl ecparam -genkey -name prime256v1 -out private_key.pem
  openssl ec -in private_key.pem -pubout -out public_key.pem
  openssl req -new -key private_key.pem -out csr.pem
  openssl x509 -req -days 365 -in csr.pem -signkey private_key.pem -out certificate.crt
  openssl dgst -sha256 -sign private_key.pem -out signature.sig data.txt
  openssl dgst -sha256 -verify public_key.pem -signature signature.sig data.txt
```

Certificates will be stored at `nginx` directory

## References
