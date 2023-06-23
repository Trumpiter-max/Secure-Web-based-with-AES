# Secure Web based with AES

## Table of contents

- [Secure Web based with AES](#secure-web-based-with-aes)
  - [Table of contents](#table-of-contents)
  - [Get started](#get-started)
    - [Requirements](#requirements)
      - [Libraries](#libraries)
    - [How to use](#how-to-use)
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

Certificates will be stored at `nginx` directory

## References

- Charm: [1](https://github.com/JHUISI/charm), [2](https://jhuisi.github.io/charm/charm/schemes/abenc/bsw07.html)


