---
title: "[TypeScript] - Quick start guide"
date: 2020-10-05T23:39:02+01:00
draft: false
---

# [TypeScript] - Quick start guide

TypeScript is a programming language created by Microsoft that transpiles to JavaScript, it is a strongly-typed superset of JavaScript and is widely adopted by providing multiple advantages like check for some errors at compile time that otherwise would accour in runtime.

This article will show the basics steps to get started with TypeScript:

* Install TypeScript
* Compile files
* Create a tsconfig.json
  
## Install TypeScript

One way to install TypeScript is trought `npm`, `npm install -g typescript`. Check the installed version with `tsc -v`.

## Compile files

Create the file `index.ts` with the following content:
```
function hello(str: string){
    console.log(str);
}

hello("Hello World");
```

Compile `index.ts` with the command `tsc index.ts`. The file `index.js` will be generated and you can run it with nodejs or inside a browser. Notice that the signature of `hello` function is expecting a string as argument if you change `hello("Hello World")` to `hello(1)` and compile it will give you an error.

In this example the compile output (`index.js`) is along side the `index.ts` in the root directory, this is not optimal for a project organization, this setup can be rearranged by putting `ts` files inside a `src` folder and the output in a `dist` folder. To compile with this setup write the command:
`tsc src/**.ts --outDir dist`.

To compile on save append the flag `-w`, `tsc src/**.ts -outDir dist -w`.

## Create tsconfig.json

The `tsconfig.json` contains all the compile options of the project, here is a example of a `tsconfig.json` for this setup:
```
{
    "compilerOptions": {
        "esModuleInterop": true,
        "target": "ES2018",
        "moduleResolution": "node",
        "module": "commonjs",
        "strict": true,
        "rootDir": "src",
        "outDir": "dist",
        "skipLibCheck": true,
        "incremental": true,
        "sourceMap": true,
        "inlineSources": true,
        "sourceRoot": "/",
        "resolveJsonModule": true
    },
    "include": ["src/**/*.ts"]
}
``` 

To use it just run `tsc` or `tsc -w` to watch for changes and compile on save.