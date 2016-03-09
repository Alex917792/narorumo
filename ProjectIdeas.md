# Future project scratch space #

## typewriter program that keeps track of daily wordcount ##
[Alex](Alex.md) has a dumb program called typewriter.py that he should put into narorumo; it's the simplest possible text editor. It gets one character at a time from the console (raw input) and appends them to a file, also printing them to stdout.

It should also keep a daily wordcount, so you can, y'know, make sure to write 1000 words a day, and finish your phd.

http://www.academicproductivity.com/2008/how-to-complete-your-phd-or-any-large-project-hard-and-soft-deadlines-and-the-martini-method/

This is seriously good advice, here:

http://lifehacker.com/#!281626/jerry-seinfelds-productivity-secret

## ajax class search for IUB ##
surely this has been done before. I want something like Kayak, but for finding classes.

Tickyboxes for: "show grad classes", "show undergrad classes"

Dropdown to let you add more departments to include. "Show CS, INFO, CSCI, COGS..."

Be able to show class descriptions or hide them.

Extra credit: search through all course descriptions and find out which department has the machine learning class this semester.

## Sleep Furiously (formerly: TEB) ##
SleepFuriouslyScratchSpace

## collaborative latex editor for wave ##
Wave is pretty great at collaborative editing for text (and as a platform, pretty great at collaborative whatever) -- what if there was a LaTeX editor for wave? You could be happily editing along with your, and there could be a "typeset!" button. LaTeX itself could either be made to run on App Engine (has it been ported to Java or Python?), or alternatively, the appengine-side of the wave robot could take your text and make a call out to a "latex web services" setup somewhere else, which would send back the typeset document, for your viewing pleasure. How does the pdf preview thing work in gmail? Is this accessible from, eg, wave?

## livejournal friends birthdays iGoogle gadget ##
LJ has a gadget where they tell you which of your friends have upcoming birthdays, but you don't look at the livejournal front page very often. Build an iGoogle gadget that keeps your LJ login information, queries for your friend-birthday data, and displays it attractively. To be polite, cache things somewhere, say in an appengine app that only polls here and again?

## logo compiler ##
([started, dropped off. should maybe start again.](http://code.google.com/p/narorumo/source/browse/#svn/trunk/wogo))
Learn Logo, preferably the dialect supported by ucblogo. Compile it to javascript, gwt-style, and do turtle graphics with the canvas tag. Is there a formal grammar for ucblogo? The problem with this idea is: no repl.

There's a beautiful online logo interpreter, though: [papert](http://logo.twentygototen.org/).

## make the paip source code work with recent common lisps ##
Norvig's Paradigms of Artificial Intelligence Programming source doesn't load right with the CL implementations I have on my Ubuntu box, sbcl and clisp. CL has had problems standardizing its loading/packaging mechanisms for a while, but there's no good reason PAIP shouldn't run nicely on recent CLs. Fix it and send Dr. Norvig a patch! Also make sure the Debian package gets updated.

## Generate good sudoku puzzles ##
So the [sudoku solver](http://sudokudlx.appspot.com) ([now with GWT/Scala version!](http://gwtdlx.appspot.com)) seems to work pretty well. But Ross would like an automated puzzle generator. How can we go about that? You can imagine generating an empty sudoku puzzle, shuffling the internal representation and then solving that (producing a random **solved** sudoku), but what then? What's the best way to take out the squares? A naive thing to do would be randomly pick some squares to take out, and keep backing up either until some set number/proportion have been erased, or until the puzzle is about to become underspecified. But the problem with that -- how do you determine whether a sudoku puzzle is underspecified? How do you modify Dancing Links to find all possible solutions instead of just the most convenient one?

## itouched ##
Every time you touched a file, it diffs it against the last time you touched that file and records this in a database -- so you know how many lines of code or whatever you wrote in a day, or per week, or per month! Keep stats for later! ...

Develop a habit: every time you edit a file, go like "itouched filename".
Or maybe it just sits running all the time and watches for changes in your
home directory?

Maybe this isn't terribly useful, in the world of version control. You at least know what you committed, when.

## Scrabblebot ##
I was working on a Scrabblebot for a while, and I felt like I had a promising approach for finding valid moves quickly... Scrabblebot wants to be refitted with a faster database. Look at how the other scrabblebots work to understand the problem space better. Write the scrabblebot in Scala. Learn Scala.

## that online programming community for kids ##
Figure out what to do about an online community where kids can build stuff in code and share it with each other. Look over notes towards WebMOOSE. Does this want to be made of Scratch, or similar to it? Can we include proper inheritance? Make it work for the OLPC.

## for ynniv ##
Less ambitious. Write a MUD. Do it in Scheme.
Doing it in Python would be verging on easy. There are quite a few MUD engines out there in Python.

## Erdos Number calculator ##
If you've published in computer science or mathematics, or probably other fields, you likely have an Erdos number; Paul Erdos has 0, everyone else has 1 + (the lowest Erdos number of any of your co-authors).

Write an Erdos Number calculator with the dblp dataset. Learn a lot about databases. Do it with postgres; sqlite is apparently not nearly as fast.

## Sudoku solver in Haskell ##
Learn Haskell well enough to solve Sudoku with it. **How do you implement Dancing Links in a purely functional language?** Surely it's possible in principle, but would it be so awkward as to not be worth it?

## Checkers bot ##
That'd be a good exercise. If you're going to overturn the world with your brilliant Go bot later, you should start out somewhere...

## Strick's challenge ##
Build a language and virtual machine. Educational for me, not very useful for other people. Recommended by Strick. Building a VM at a pretty high level of abstraction might not be that hard, just think about stack frames and returning things and whatnot?  At what level do things like the Python VM work? What's the JVM like, really?  Surely there are different approaches used for this? What are they? Would it be hard to build something with multithreading in mind from the bottom up? What about a purely functional lambda-calculus implementation? Then layers of abstraction and naming on top of the LC?

## archiving todo gadget ##
It'd be pretty cool to have a nicer Google Gadget (for igoogle) for keeping TODO lists. There are a bunch of these already, clearly, but one that archives your old items, searches and tags, would be pretty rockin'. And good practice. And make me learn to build gadgets.

## inline test cases ##
[doctest](http://docs.python.org/library/doctest.html) for Python is pretty hip. What if that was available for your other favorite language?

There's a project going for Haskell, apparently: [hs-doctest](http://github.com/nkchenz/hs-doctest/tree/master).

### firefox: browser cache browsing ###
There should be firefox functionality that lets you see what's in your browser cache, say if you're offline. It should show cached files like the history view, as a tree, by site.

Also see:
about:cache?device=disk

There's something sort of like this, CacheViewer, but the UI doesn't look great.

## AllRunsTogether ##
Say you have several people who all want to go running together, and they live fairly nearby. What if you had a Google Maps mashup that could help plan a route for everybody to meet up and run together? What if some participants are stronger runners than others, and wouldn't mind going farther to get to a meetup point?
Could some routes be circuits, where not everybody goes on all parts of the run, and people get dropped back off at their starting location later?
Didn't I have a demo of something like this, a few years ago? Where did that code go?

## hook sleep-furiously up to an IRC bot ##
http://code.google.com/p/ircbot-collection/

# done #

## make your papers shorter ##
**implemented and launched!** http://kompressr.appspot.com

  * find all the ngrams (greater than, say, n=3, and up to a large n)
  * for every ngram that happens more than once, define an acronym in the text.
  * replace all subsequent occurrences by the acronym.

"As you can see (AYCS) ..."

(idea largely due to [Mike Riley](http://research.google.com/pubs/author125.html))

### Firefox: ~~tear off tabs to be new windows~~ ###
I'd like a Firefox extension that lets you take a tab and drag it out into space, causing it to become a new window. Or just context-menu the tab to do that same thing.

**As of Firefox 3.1, there's a context menu to do exactly that, great!**