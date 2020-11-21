---
title: "[Docker-compose] Local php environment with nginx, mysql and phpMyAdmin"
date: "2020-08-24"
draft: false
---

# Docker-compose: Local PHP environment with nginx, mysql and phpMyAdmin

This tutorial is going to guide you throught the process of mounting, using docker-compose, a local php development environment with nginx, mysql and phpMyAdmin step by step.

The tutorial will have the following steps:
* Setup nginx
* Setup ngninx with PHP
* Adding mysql and phpMyAdmin

Start by creating the file `docker-compose.yaml` where it is going to have all docker configurations.

## Setup nginx 

First we need a simple webserver, for that we use a `nginx` image. In the `docker-compose.yaml` put the following code:
```
version: "3"
services:
    nginx:
        image: nginx
        ports:
            - "8080:80"
        restart: always
```

The `ports` option maps the localhost port to the inside container port, this means when you reach de `8080` port in localhost it will map the connection to port `80` inside the container.

To try this setup run `docker-compose up -d`, the `-d` flag means detach mode, if you run this command without this flag you would end up being inside the nginx container. To test the installation go to the broswser and type int th url `127.0.0.1:8080`, you should see the nginx welcome webpage. To stop the container run `docker-compose down`

## Setup nginx wih PHP

First create in the root directory the `default.conf` file for nginx to integrate it with PHP. For this setup this is our `default.conf`:

```
server {
	root /code;
	index index.php;

	server_name _;
    location / {
        index index.html;
    }
	location ~ \.php$ {
        try_files $uri /index.php =404;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        fastcgi_buffers 16 16k;
        fastcgi_buffer_size 32k;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

To copy this file inside the nginx container put the following lines under the `nginx` part of  `docker-compose.yaml`:

```
volumes:
    - ./default.conf:/etc/nginx/conf.d/default.conf
```
`volumes` maps the files in you computer to the inside of the container.

We can see that `fastcgi_pass` is fowarding the requests to `php:9000`, the `php` hostname will correspond to the php container (services names are the hostname of the corresponding containers). By default containers do not have access to each other, it is needed to say explicit that a container should have access to other container with `link` directive:

Until now out `docker-compose.yaml` should have the following content:

```
version: "3"
services:
    nginx:
        restart: always
        image: nginx
        ports:
            - "8080:80"
        volumes:
            - ./code:/code
            - ./default.conf:/etc/nginx/conf.d/default.conf
        links:
            - php
    php:
        restart: always
        image: php:fpm
        volumes:
            - ./code:/code
            - ./php.ini:/usr/local/etc/php/php.ini
```

This `docker-compose.yaml` has already two more `volumes` directives. You should put the PHP code inside `code` folder in the root directory, note that the paths containing the code inside the containers should be the same, other alternative could be `./code:/var/www/html`, you could put this in the `volumes` directive of both containers. This `docker-compose.yaml` has also an example where you can put a custom `php.ini` inside the PHP container.

Put an `index.php` file inside `code` folder with the following content:
```
<?php
phpinfo();
```
Now if you access `127.0.0.1:8080/index.php` you can see the PHP info.

## Adding mysql and phpMyAdmin

This is the final `docker-compose-yaml`:

```
version: "3"
services:
    nginx:
        restart: always
        image: nginx
        ports:
            - "8080:80"
        volumes:
            - ./code:/code
            - ./default.conf:/etc/nginx/conf.d/default.conf
    php:
        restart: always
        image: php:fpm
        volumes:
            - ./code:/code
            - ./php.ini:/usr/local/etc/php/php.ini
    mysql:
        image: mysql
        environment:
            MYSQL_ROOT_PASSWORD: root
        restart: always
        volumes:
            - ./database:/var/lib/mysql
        ports:
            - "3306:3306"
    phpmyadmin:
        image: phpmyadmin/phpmyadmin
        environment:
            PMA_HOST: mysql
            PMA_USER: root
            PMA_PASSWORD: root
        ports:
            - "8081:80"
        restart: always
        volumes:
            - ./php.ini:/usr/local/etc/php/php.ini
```

In `mysql` it is need to create the environment variable `MYSQL_ROOT_PASSWORD` to define the mysql password for user `root`. To make the database persistent you can mount `./database:/var/lib/mysql`, this will put all database files inside the `database` folder in the root directory and save the data even if you unmount the containers.

In `phpMyAdmin` these 3 enviroment variables `PMA_HOST`, `PMA_USER`, `PMA_PASSWORD` define the host to the `mysql` database, in this case the hostname is also `mysql`, the database username and the password for it.

Now you have a simple local php with mysql and phpMyAdmin development environment which can be mounted with `docker-compose up -d` and unmounted with `docker-compose down`.