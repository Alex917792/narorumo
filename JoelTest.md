# Joel's "Could you have passed my freshman-year midterms?" test #

[Lindsey Kuper](Lindsey.md)

I was having a [hard time](http://lindseykuper.livejournal.com/261785.html) with _SICP_ today.  Because I have my Honor to Defend, or possibly because I'm a masochist, I decided to take part of a [programming test](http://www.joelonsoftware.com/articles/TestYourself.html) linked from [everyone's favorite Joel on Software article](http://www.joelonsoftware.com/articles/ThePerilsofJavaSchools.html).

## Problem ##

> Using the function

```
(define (accumulate combiner null-value l) 
   (if (null? l)
       null-value
       (combiner (car l)
                 (accumulate combiner
                             null-value
                             (cdr l)))))
```


> Implement `sum-of-squares`, which calculates the sum of squares of a list,
> for example

```
 sum-of-squares '(1 2 3 4 5))
```

> should evaluate to 55.

## Solution ##

The first thing I did was to write `sum-of-squares` the way I'd do it _without_ `accumulate`:

```
(define boring-sum-of-squares
  (lambda (ls)
    (let ((square (lambda (x) (* x x))))
    (if (null? ls)
        0
        (+ (square (car ls)) (boring-sum-of-squares (cdr ls)))))))
```

And then I just generalized it out:

```
(define sum-of-squares
  (lambda (ls)
    (accumulate + 0 (map (lambda (x) (* x x)) ls))))
```

This turned out to be different from [Joel's solution](http://www.joelonsoftware.com/articles/TestYourself.html), which puts the squaring in a different place and doesn't use `map`.  It hadn't occurred to me that using the built-in `map` might not be allowed, but in that case I'd write my own:

```
(define sum-of-squares
  (letrec ((map
            (lambda (fn ls)
              (if (null? ls)
                  '()
                  (cons (fn (car ls)) (map fn (cdr ls)))))))
    (lambda (ls)
      (accumulate + 0 (map (lambda (x) (* x x)) ls)))))
```

Doing the initial problem with `map` took about twelve minutes, and doing it without `map` took another ten, most of which I spent trying to remember what the `letrec` syntax looked like.  So, 22 minutes total on this problem, and my solution isn't as nice as the one that's given, but at least it works.  Honor somewhat intact!  I can't do pointertastic C like the second and third problems call for, especially not at three in the morning like it is right now.  But darn it, I can understand recursion.

[Alex Rudnick](Alex.md)

`accumulate` is [reduce](http://en.wikipedia.org/wiki/Reduce_(higher-order_function)); particularly in this case, foldr!