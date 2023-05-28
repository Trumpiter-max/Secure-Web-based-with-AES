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

- Python version: 3.8
- OS environment: Ubuntu 20.04 LTS linux
- Docker environment: in progress
- Database engine: MongoDB 4.0.8

#### Libraries

### How to use

Run container

```
  docker-compose up 
```

Close docker-compose

```
  docker-compose down 
```

## Self sign certificate

```sh
  openssl ecparam -name secp384r1 -genkey -noout -out $HOME/private_key.pem 
  openssl req -new -x509 -nodes -sha384 -key private_key.pem -out certificate.pem -days 365 
```

## References

---

