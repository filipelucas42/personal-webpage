---
title: "Setting Up a MongoDB database"
date: 2020-04-06
draft: false
---

# Setting up a MongoDB database

In this article I will explain how to set up a MongoDB database. This article will be split in two main steps:

* Install MongoDB
* Run MongoDB and set up authentication
* Make a simple NodeJS connection

## Install MongoDB

Most of the repositories have MongoDB however I do not recommend install it this way because usually the repositories do not have the most recent stable version.

Instead of installing with the repository you should download it from the [MongoDB website](https://www.mongodb.com/download-center/community). There you can select the version, OS and package, in package you should choose the `TGZ` option.

After download the tar file extract it with:
```
tar xf <file>
```

After extract go inside it and copy all the binaries that are in the folder `bin` to a folder of your choice. If you are the only user I would recommend to copy these file to: `~/.local/bin/mongodb`

After copy the files you should add the path to your PATH variable, you can do this by copying the following line to `/etc/environment` or `~/.bashrc`:
```
export PATH=$PATH:~/.local/bin/mongodb
```

## Run MongoDB and set up authentication

To run MongoDB open a terminal and type:
```
mongod --dbpath <path_to_database>
```
The <path_to_database> can be any path of your choice, all the files of database will be stored in this path. Note that the path/folders need to be created before running the command. Example:

```
mongod --dbpath ~/mongodb
```

After start MongoDB is time to create authentication credentials, to enter the database open a new terminal and type the command:
```
mongo
```

This command will open a console to interact with the database. Note that for localhost connections you do not need authentication.

To set up authentication credentials you need to create a database to store them. To create a database simply type in the console `use admin`, this will create a database inside MongoDB called *admin*.

In the console to create the credentials type the command:
```
db.createUser({user:"username", pwd:passwordPrompt(), roles:["userAdminAnyDatabase"]})
```

This create a user for the database called *username*, the `passwordPrompt()` will ask for a password, the database stores the hash and not the password itself.

## Make a simple NodeJS connection

First install the MogoDB drivers with npm, then follow the next code example to make a connection:
```javascript
const MongoClient = require('mongodb').MongoClient;
MongoClient.connect("mongodb://username:passwordn@localhost:27017/v2?authMechanism=DEFAULT&authSource=admin", function(err, db) {
  if(err) { return console.dir(err); }

  const collection = db.collection('test');
  const doc1 = {'hello':'doc1'};

  collection.insert(doc1);

});
```

Substitute username and password with the ones used to create the MongoDB user in the process of create the authentication credentials.

