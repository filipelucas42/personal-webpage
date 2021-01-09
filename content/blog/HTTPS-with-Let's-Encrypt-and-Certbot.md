---
title: "HTTPS with Let's Encrypt and Certbot"
date: 2020-03-13
draft: false
---

## HTTPS with Let's Encrypt and Certbot

HTTPS allows secure connections between browsers and web servers and if you transit sensitive information (like passwords for login) between your website and it's users having HTTPS is a must.

Nowdays due to [Let's Encrypt](https://letsencrypt.org/) it's possible to obtain free certificates and enable HTTPS for your websites with no costs.

I will explain in two parts how to enable HTTPS for your websites:
* Obtain certificate
* Install certificate (in this case it will be explain with nginx)

## Obtain certificate

It will be used *certbot* tool to make this process easier. If you are using linux it's likely that *certbot* is in your package manager, for Ubuntu and Debian distributions you can install with *sudo apt install certbot*

After installation you can get a free certificate by running the following command:
```
sudo certbot certonly --standalone -d example.com
```

Note if you have a webserver running (for example nginx) you need to disable it before running that command or you can run the following:
```
sudo certbot certonly --standalone -d example.com --pre-hook "systemctl stop nginx.service" --post-hook "systemctl start nginx.service"
```

After you run the command you should get a free certificate that it is stored in the following directory `/etc/letsencrypt/live/example.com`. In this directory there are two files you will need to install: *fullchain.pem* and *privkey.pem*. 

In my case I got two certificates for each one of my two websites and so I run the following commands:
```
sudo certbot certonly --standalone -d www.filipelucas.com --pre-hook "systemctl stop nginx.service" --post-hook "systemctl start nginx.service"
sudo certbot certonly --standalone -d blog.filipelucas.com --pre-hook "systemctl stop nginx.service" --post-hook "systemctl start nginx.service"
```

My two certificates are in `/etc/letsencrypt/live/www.filipelucas.com` and `/etc/letsencrypt/live/blog.filipelucas.com`.

Note that you **should** do a backup of `/etc/letsencrypt/` folder.

Now that we have the certificate for the website we should use it with our webserver software that in my case is nginx.

## Install certificate with nginx

To install the certificate you need to change the config of the nginx that are in `/etc/nginx/nginx.conf`, to know what to put there go to the following website [https://ssl-config.mozilla.org/](https://ssl-config.mozilla.org/), this site is done by Mozilla and it provides the right configuration for the HTTPS for you server, just select you webserver software (for instance nginx) and it's right version. To check the version of nginx run the following command `sudo nginx -v`

As an example I will show my nginx config for HTTPS:

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/www.filipelucas.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.filipelucas.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
    ssl_session_tickets off;

    # curl https://ssl-config.mozilla.org/ffdhe2048.txt > /path/to/dhparam.pem
    #ssl_dhparam /path/to/dhparam.pem;

    # intermediate configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS (ngx_http_headers_module is required) (63072000 seconds)
    add_header Strict-Transport-Security "max-age=63072000" always;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # verify chain of trust of OCSP response using Root CA and Intermediate certs
    #ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;

    # replace with the IP address of your resolver
    #resolver 127.0.0.1;
    server_name filipelucas.com www.filipelucas.com;
    root /var/www/html/personal;

    location / {
        index index.html;
    }
}
```

<br>

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/blog.filipelucas.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/blog.filipelucas.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
    ssl_session_tickets off;

    # curl https://ssl-config.mozilla.org/ffdhe2048.txt > /path/to/dhparam.pem
    #ssl_dhparam /path/to/dhparam.pem;

    # intermediate configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS (ngx_http_headers_module is required) (63072000 seconds)
    add_header Strict-Transport-Security "max-age=63072000" always;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # verify chain of trust of OCSP response using Root CA and Intermediate certs
    #ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;

    # replace with the IP address of your resolver
    #resolver 127.0.0.1;
    server_name blog.filipelucas.com www.blog.filipelucas.com;
    location / {
        proxy_pass http://127.0.0.1:8081;
    }
}
```

To check it configs are right run `sudo nginx -t` and then reload the configs `sudo systemctl reload nginx`.

Note that the certificates are only valide for 90 days, after that time you can renew again.