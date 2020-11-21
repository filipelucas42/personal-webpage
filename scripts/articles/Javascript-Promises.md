---
title: "Javascript Promises"
date: 2020-02-02
draft: false
---

# Javascript Promises

Javascript is an asynchronous language, this means that contrary to most of the languages the instructions do not run sequentially in some cases.

The code above shows an example of asynchronous Javascript execution:

```javascript
let test = 0;

setTimeout(()=>{
    test = 10;
}, 10);


console.log(test);
// Output: 0
```

Because of the asynchronous behaviour the output is *0* instead of *10*, in a synchronous execution it was expected to the *setTimeout* function wait for 10 milliseconds, change the value *test* to 10 and then print it on the console. But as you can see if your run the code the *console.log* function runs before the setTimeout ends.

Another examples of asynchronous behaviour are *ajax* calls and *fetch*.

There are some techeniques to get around this asynchronous behaviours like *callbacks* but in some cases this is not the best aproach.

Another aproach is to use *Promise*. Above is the code modified to get the synchronous beahviour:

```javascript

let test = 0;

function timeout(){
    return new Promise((resolve, reject)=>{
        setTimeout(()=>{
            let error = false;
            if(!error){
                test = 10;
                resolve(test);
            } else {
                reject();
            }
        }, 10)
    })
};

timeout().then(console.log);
// Output: 10
```

As you can see if you run the code now it has synchronous behaviour. It is easy to see that the *console.log* runs after the *timeout* function using the method *then*.

The *Promise* receives two arguments, *resolve* and *reject*, the *resolve* should be called after the insctructions that are supposed to be executed before the next instrunction, in our case we should call it after the *test=10* because when this instruction is done the *console.log* can print it.

The *reject* should be called if some error occurs and catch it with the *catch* method.