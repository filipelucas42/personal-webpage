---
title: "[Linux] Tar Command"
date: 2020-02-25
draft: false
---

# Tar Command

If you use linux you mostly likely already needed to extract compressed files from tar.gz or tar and if you are like me you probably checked the command to extract the files every single time you needed it.

I checked the command to extract the files until I actually learnt what each flag from `tar -xzf file.tar.gz` command means. The flags are very straightforward in a way it is very easy to learn their meaning so you never need to check the command again each time you want extract from tar files.

In this post I will explain briefly how to use and possibly memorize the basic usage of tar command.

## Extract files

Command to extract files:
```
tar -xzf file.tar.gz
```

Meaning of the flags:
* **x**: extract files
* **f**: option to give the filename that is going to be extracted
* **z**: it means that *tar* should extract files using *gzip* compression mode. There are the -j option that refers to *bzip2* compression mode but this option is less used since it takes more time to compress and extract, although it can compress the files to a smaller size

Sometimes the command appers like:
```
tar -xzfv file.tar.gz
```

The `v` flag turns the process verbose meaning that the command will output the process of extraction.

You can commonly encounter the following command too:
```
tar -C /destination/path -xzf file.tar.gz
```

The `C` flag extract the files to */destination/path* instead extracting to the current directory

## Compress files

I personally never used the tar commmand to compress files but since I am writing about it I will put here the basics to compress files.

Command to compress files:
```
tar -cfzv files.tar.gz file1 file2 file3 ...
```

Meaning of the flags:
* the **fzv** was already explained, but to recapitulate: **f** (filename) / **z** compress algoritm (gzip) / **v** verbose mode
* **c**: flag to compress the files and create the files.tar.gz. The opposite to **c** (create) is **x** (extract) as we already reference it in the extract section of this post