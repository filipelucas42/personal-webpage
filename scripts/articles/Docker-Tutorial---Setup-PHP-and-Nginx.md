---
title: "Docker Tutorial - Setup PHP and Nginx"
date: 2020-05-02
draft: false
---

## Docker Tutorial - Setup PHP and Nginx

In this tutorial I will present the the basic docker commands and guide you trough a setup of PHP and Nginx as a simple exercise. Note that most of the times you will encounter this setup using docker-compose, however we will not use that as a way to practice the basics of docker cli.

Note that by default you need to use `sudo` to run a docker command.

First we need to download the two images from docker hub that will be used: nginx and php:

```
docker pull nginx
docker pull php
```

Check your available images in your local machine:

```
docker images
```

For purpose of organization lets create a folder to put all the files related with this setup:

```
mkdir ~/nginx-php
mkdir ~/nginx-php/conf.d
mkdir ~/nginx-php/code
```

We can start by running the nginx image:

```
docker run --name my-nginx -p 80:80 -d nginx
```

* -d: run in detach mode, otherwise you would get inside the running container shell
* -p: expose port 80 of container and links it to localhost port 80, if you write instead `8080:80` for example the localhost port 8080 would redirect the traffic to port 80 inside the container
* --name: gives a name to the container, if you do not give this option docker will generate a random name

You can refer the container by it's ID or name, you can check the running containers with:

```
docker container ls
```

With the nginx container running you can go to the browser and check you localport 80 by typing in the URL `localhost:80`, you can check that appears the default Nginx webpage.

Now lets stop the container and remove it so we can run it again with some more additional flags:

```
docker stop my-nginx
docker rm my-nginx
```

Lets run the nginx image again with more two additional flags:

```
docker run --name my-nginx -p 80:80 -v ~/nginx-php/conf.d:/etc/nginx/conf.d -v ~/nginx-php/code:/code -d nginx
```

* -v: it mounts a local diretory inside a container directory, is our case all files from `~/nginx-php/conf.d` are shared with the container inside /etc/nginx/conf.d

Before start serving PHP files let's just serve a simple html file to check if in fact the nginx container is working. Inside `~/nginx-php/conf.d` create the file `app.conf` with the following content:

```
server {
    index index.php index.html;
    server_name _;
    root /code;
}
```

Inside ~/nginx-php/code create the file index.html and write in it some text. Let's take this opportunity to enter inside container shell and check is the Nginx config is right. You can enter the shell container with this command:

```
docker exec -ti my-nginx bash
```

`docker exec` executes a command inside the container, in this case when need a bash shell, the `-t` option gives you a tty and `-i` puts you in interactive mode.

To check if the Nginx config is write type inside the container:
```
nginx -t
```

If it gives an ok you cant exit the container with `CTRL+d` and reload it with the command:

```
docker restart my-nginx
```

If you now go to the browser and type `localhost:80/index.html` it will show up the contents inside `~/nginx-php/code/index.html` that correspond inside the docker `/code/index.html`.

Let's now run the php container:

```
docker run --name my-php -p 9000:9000 -v ~/nginx-php/code:/code -d php:fpm
```

Now inside `~/nginx-php/code` create the file index.php and write inside:

```
<?php
echo phpinfo();
```

Before we change the Nginx config we need to check what is the php container ip:

```
docker inspect my-php
```

However this will give you a ton of information, to see just what we want run:

```
docker inspect my-php | grep IPAddress
```

In my case the php container IP is 172.17.0.3

Now inside `~/nginx-php/conf.d/app.conf` write:
```
server {
    index index.php index.html;
    server_name _;
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
    root /code;

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass 172.17.0.3:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
```

Note that instead `fastcgi_pass 172.17.0.3:9000` you should put the IP of you php container that you got `fastcgi_pass <you_php_container_ip>:9000`

Restart the Nginx container `docker restart my-nginx` and now if you go to the browser and type `localhost/index.php` it should show you the output of `phpinfo()` that you wrote in the `~/nginx-php/code/index.php` .

Besides knowing now a little bit more about docker you have now too a simple PHP development environment that supposedly you can run in any machine that has docker installed.





 




