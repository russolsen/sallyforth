# SallyForth: A simple Forth-like language implemented in Python.

SallyForth is a simple hobby implementation of a FORTH-like programming
language. Possibly the most interesting thing about SallyForth is the
name, which 
[Michael Nygard suggested](https://twitter.com/mtnygard/status/1249781530219642883)
as a name for a FORTH implementation
at exactly the same time that I happened to be writing this code.

## Running SallyForth

SallyForth is writting in Python 3 and will happily run with
either the standard C Python implementation or Pypy. To
run SallyForth just kick off the sallyforth.py file:

````
$ python sallyforth/sallyforth.py
````

## The Sally Language

Like FORTH, Sally is a stack oriented concatenative programming language.
What this means is that any constant value in a sallyforth program,
like a number or a string:

```
sallySh> "Hello, world!"
```

Has the effect of pushing the value onto an ever present data stack.
There are also commands or functions -- called *words* -- that you
can use to do things.

So the word `p` will pop the value off of the top of the stack 
and print it:


```
sallySh> "Hello, world!"
sallySh> p
Hello, world!
```

Sally parsing is about as simple as you can get: words and constant
values are separated by whitespace. So if you wanted to print
a number of values, you could do this:

```
sallySh> 1 2 3 p p p
3
2
1
```

The only execeptions to the _separated by whitespace rule_ are
double quoted strings, which work about the way you would expect:

```
sallySh> "I can have spaces in my string"
sallySh> p
I can have spaces in my string
```

Sally comes prepackaged with a host of useful words, everything
from basic arithmetic:

```
sallySh> 1 2 + p
3
sallySh> 10 10 * 1 + p
101
```

To boolean logic:

```
sallySh> true false and p
False
sallySh> false true or p
True
```

To IO:

```
sallySh> "hello.txt" read-file
sallySh> p
This is the contents of hello.txt.
Use it wisely.
```

You can also define your own words. A word defintion starts with
a colon, followed by the name of your new word, followed by
the contents of your new word, followed by a semicolon. 
Keep in mind that everything -- including the colon and semicolon,
needs to be set off with whitespace:

```
: hello-world "Hello, world!" p ;
```

Once your new word is defined you can use it like any other word:

```
sallySh> hello-world
Hello, world!
```

