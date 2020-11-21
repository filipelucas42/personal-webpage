---
title: "NGINX HTTP Configuration"
date: 2020-02-17
draft: false
---

# NGINX HTTP Configuration

In this post I will explain and give examples how to configure NGINX in three cases:

* Serve simple files like html, images, etc...
* Redirect requests
* Serve PHP file


A NGINX config file has multiple configurations although I will only show the relevant parts for the scope of this post. In the end I will show my NGINX config file with all the options that I use.


## NGINX basic commands

In linux system the NGINX config file is located at */etc/nginx/nginx.conf*

After change the config file you should run this command to check if config file has any error:
```
sudo nginx -t
```

After change the config file you should reload the NGINX:
```
sudo systemctl reload nginx
```

## Serve simple files
```
http {
    server {
        listen 80;
        listen [::]:80;

        server_name example1.com;

        #root points to the folder that has the files
        root /var/www/html/public;

        location / {
            #configuration to get the index.html as default
            index index.html
        }
    }
}
```

## Redirect requests
```
http {
    server {
        listen 80;
        listen [::]:80;

        server_name example2.com;

        #root points to the folder that has the files
        root /var/www/html/public;

        location / {
            #substitute <url> for the url you want to redirect the request
            proxy_pass <url>
        }
    }
}
```

## Serve PHP files
```
http {
    server {
        listen 80;
        listen [::]:80;

        server_name example3.com;

        #root points to the folder that has the PHP files
        root /var/www/html/phpfiles;

        location / {
            index index.php;
        }

        location ~* \.php$ {
            fastcgi_pass unix:/run/php/php7.2-fpm.sock;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        }
    }
}
```

## Example of NGINX config file

This is my NGINX config file
```
http {
    ##
    # Basic Settings
    ##
 
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;
 
    server_names_hash_bucket_size 64;
    # server_name_in_redirect off;
 
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
 
    ##
    # SSL Settings
    ##
 
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;
 
    ##
    # Logging Settings
    ##
 
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    gzip on;
    include /etc/nginx/conf.d/*.conf;
    server {
         listen 80;
         listen [::]:80;
         server_name mercedez.filipelucas.com;
         
         root /var/www/html/mercedez;
         
         location / {
             index index.html;
         }
     }

     server {
         listen 80;
         listen [::]:80;
         server_name pics.filipelucas.com;
 
         root /var/www/html/portofolio;
 
         location / {
             index index.php;
         }
         location ~* \.php$ {
             fastcgi_pass unix:/run/php/php7.2-fpm.sock;
             include fastcgi_params;
             fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
             fastcgi_param SCRIPT_NAME $fastcgi_script_name;
         }
 
     }
 
     server {
         listen 80;
         listen [::]:80;
         server_name filipelucas.com www.filipelucas.com;
         root /var/www/html/personal;
 
         location / {
             index index.html;
         }
     }
 
     server {
         listen 80;
         listen [::]:80;
         server_name blog.filipelucas.com www.blog.filipelucas.com;
         location / {
             proxy_pass http://127.0.0.1:8081;
         }
     }
}
```