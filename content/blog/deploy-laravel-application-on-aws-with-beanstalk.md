---
title: "Deploy Laravel Application on AWS With Beanstalk"
date: 2020-12-01T11:32:57Z
draft: false
---
# Deploy Laravel Application on AWS With Beanstalk

Beanstalk is an easy way to deploy web applications on AWS, the ideia of this product is to manage the instance, server configuration, etc for you so you just need to upload the code application.

When deploying a Laravel application with Beanstalk you need to be in attention two details:
* Redirect all the traffic to `public` folder and `index.php`
* Make a fix to `storage:link` command to use the `public/storage` folder

## Create a Beanstalk application

When creating a Beanstalk application you need to choose the language and the plataform branch, this option gives the possibility to choose between `Amazon Linux` and `Amazon Linux 2`. The difference between this two options is that one uses Apache and another uses Nginx, this article is made for the Nginx option so choose the `Amazon Linux 2`.

## Which files you should upload to the application

These are the folders and files you should upload:
* app
* artisan
* bootstrap
* config
* database
* public
* resources
* routes
* server.php
* storage
* vendor or composer.json

If there is a `composer.json` file present and no `vendor` folder the Beanstalk application will download the composer dependencies, otherwise if there is a `vendor` folder the application will use those files.

## Redirect all the traffic to public folder and `index.php`

Besides the previous files you also need to create the following file `.plataform/nginx/conf.d/elasticbeanstalk/laravel.conf`. The `.plataform` folder contain files to extends the application environment, in this case it is used to tweak the nginx config to deploy a Laravel application.

The contents of `.plataform/nginx/conf.d/elasticbeanstalk/laravel.conf` should be the following:
```
location / {
	try_files $uri $uri/ /index.php?query_string;
	gzip_static on;
}
```

This will redirect the traffic to the right files.

## Make a fix to `storage:link` command to use the `storage` folder

In a Laravel application when you run `php artisan storage:link` a `storage` link to `storage/app/public` will be created, however this link will have the full path, something like this `/Users/user/path-to-laravel-application/storage/app/public`. The full path will not work inside the Beanstalk application, you need to change the link with a relative path so you need to run the following command:
```
ln -s ../storage/app/public public/storage
```

The last detail you need to have in attention is when creating the Beanstalk application put in `Root directory` option the `public` folder.