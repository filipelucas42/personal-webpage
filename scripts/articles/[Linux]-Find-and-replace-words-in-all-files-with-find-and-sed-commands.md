---
title: "[Linux] Find and replace words in all files with find and sed commands"
date: 2020-07-16
draft: false
---

# Find and replace words in all files with find and sed commands

Although is essential using an IDE for programming, I believe that we should not be completely attach to it. For simple operations, UNIX tools can be used to do a lot, programmers should see linux environments as an IDE by itself and use it more to manage projects.

In this article I am going to explain how to find and replace all word occurrences in all files inside a project folder structure using `find` and `sed` commands.

Just have in mind that before doing some modification do a backup or a commit, unlike IDE there's no undo command for this!

## find command
`find` command is used to list all files inside a folder:

```
#usage
find <path> [args]

#example:

#list files from current directory
find .

#list files from home directory
find ~/

#list only regular files (excludes directories)
find . -type f

#ignore files or folders
find . ! -path './ignore_path/*' 
```

## sed command
`sed` command is used to find and replaces words inside files:

```
#usage
sed [options] <file>

#replace all occurrences of word1 with word2 in file.txt
sed -i 's/word1/word2/g' file.txt

# -i replaces the word1 occurrences inside the file, otherwise the result of replacing will be just output to terminal without affecting the file itself
# 's/' option is to replace
# '/g' replaces all words inside a line, otherwise the sed command only replaces the first occurrence of each line inside the file
```

## Using the two commands together 
These two commands can be used together in multiple ways, it can be used for example pipes or `xargs` but in this article we will do things in other way. `find` command has the option `-exec` to run commands for each result it encounters. We can use `find` with `sed` in the following way to replace all occurrences of `word1` for `word2` in all files from current directory and sub directories:

```
find . -type f -exec sed -i '/s/word1/word2/g' {} +
```

## Real example
Now I am going to give a real example of one modification I needed to do in a NodeJS project. In this project I needed to replace the word `__model` for `_model` in all files. It should be noted that in this case the `node_modules` and `.git` folders should be ignored, so I ran this command:

```
find . -type f ! -path './node_modules/*' ! -path '.git/*' -exec sed -i 's/__model/_model/g' {} +
```


