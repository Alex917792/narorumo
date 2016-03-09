_(To quote danah boyd: "This is a rough unedited crib of the actual talk.")_

Hi!  For those of you who don't know me, my name is Lindsey Kuper.  Up until a month ago, I was a Perl programmer, and in another month I'll be a computer science grad student.  Right now I'm a happily unemployed geek.  Today I want to talk about my experience participating in the ICFP Programming Contest this year.

The ICFP Programming Contest is an international programming competition which is held each year in a different location around the world, and it's an outgrowth of the International Conference on Functional Programming, which is a annual academic conference about functional programming.  The contest takes place over a 72-hour period, from noon on Friday until noon on Monday, in the time zone of the institution organizing the contest.  It's been going on since 1998 and is organized by a different institution every year, usually a university.  This year it was hosted right here in Portland by PSU.

I first heard about the ICFP contest last year, when four of my friends participated and ended up doing quite well, earning 28th place out of 869 teams.  After seeing my friends do so well in this contest and have so much fun, I started thinking of participating in it myself.

Another reason I wanted to participate is because I love functional programming, and the ICFP contest is sponsored by a conference that focuses on functional programming.  The contest itself doesn't necessarily have anything to do with functional programming, but because I love it so much, I want to talk briefly about what it is.  Rather than offer a hard-and-fast definition I just want to tell you what I think some characteristics of functional programming are.

Functional programming is a style of programming that focuses on what is to be computed, rather than how it is to be computed.  When I was preparing this talk yesterday, I was looking at the Haskell wiki and came across a great example of this.  They say that if you've ever used a spreadsheet that uses formulas to specify the value of certain cells in terms of the values of other cells, you'll be able to understand this aspect of functional programming.  When you write those formulas, you don't tell the spreadsheet how to allocate its memory -- you expect it to allocate memory only to those cells which are actually in use, even though there's an apparently infinite plane of cells there available to you.  What you try to do instead is write a mathematically sound expression which the spreadsheet program will be able to evaluate, rather than a sequence of commands which have to be carried out one after the other.

That brings us to our next item, which is that in functional programming we don't specify the order in which computation takes place.  If you think about mathematical definitions and formulas, they're not time-dependent or order-dependent -- they have the same meaning no matter when they're being evaluated.  Functional programming works the same way.  To shamelessly steal another example from the Haskell wiki, think about a database query in SQL.  A SQL query is an expression involving selections, joins and so forth. The query says what relation should be computed, without saying how it should be computed, and in fact the query can be evaluated in any convenient order.  As the SQL programmer, you don't have to worry about that.  It's the SQL implementation's job to determine the best order in which to evaluate the expression.

Functional programming treats functions as first-class data objects.  By "first-class" we mean that we can pass functions as arguments to other functions, and you we return functions as results from functions.  Everything we can do with "data" can be done with functions themselves.  So this in turn encourages "higher-order" programming, which is when we have functions that operate on functions that operate on functions and so on.

So, spreadsheets and SQL are both fairly specialized languages. Functional programming languages take the same ideas and move them into the realm of general-purpose programming.  And a functional programming language is one that supports and encourages programming in a functional style.

So why do I like functional programming so much?
  * First, it's less code.
  * Second, it's easier to reason mathematically about functional programs.
  * Third, I'm a native speaker.  Functional programming was the first style of programming that I learned.  I didn't start programming until I got to college and even then I didn't start until my second year of college!  I think that put me at an advantage.

Back when I was a little geek, just starting out, my first programming language was Scheme.  Scheme, if you're not familiar with it, is a flavor of Lisp, which is usually considered to be the first functional language.  And the functional style of programming was how I first learned to program.  Eight years later Scheme is still my favorite language (so far) and functional programming is still my favorite kind of programming.

But I've spent most of those eight years not writing Scheme, and I decided at the beginning of this year that I missed it and wanted to get back into it.  There's a classic book about programming, called Structure and Interpretation of Computer Programs (also known as SICP) which uses Scheme and the functional style.  This book was written 20 years ago and it's still relevant and interesting.   It was used for a long time to teach computer science at MIT.  My understanding is that they recently stopped using it, although a number of other schools still do.  Anyway, even though we used Scheme in my intro CS courses, I'd never used this book before.  I started reading the book and working through the exercises in it, working together with my partner Alex.  And here's a picture of him.  It was Alex's idea to do all of the exercises in SICP, and we both worked on it, sometimes working together and sometimes not.  There are 46 exercises in chapter 1, and my goal was to the 46 exercises before the ICFP contest started, and then compete in the contest using Scheme.  I might not have been able to do this, but because I left my job at the beginning of July, I was able to do a lot of programming in the last couple of weeks before the contest, and I ended up doing the last 20 or so exercises myself, and I finished the last one of the exercises the day before the contest started!  So I was feeling pretty confident going in.

One thing that I really like about the ICFP contest is that most of the prizes don't honor the team members specifically; they honor the **programming language** that the winning teams used.  To participate in the ICFP contest, you don't have to use a functional language, and you don't have to write in a functional style.  At this point, I'd like to say something like "but it helps", but the fact is that people have won in the past writing assembly, so it's not really valid to say that.  But I think I can say that people who really care about functional programming languages are by definition people who really care about programming languages.  And I really like that aspect of this contest and the the way that the prizes are awarded -- winning is less about personal glory than it is about honoring a language that you think is great.

  * First prize: _Language 1_ is the programming tool of choice for discriminating hackers.
  * Second prize: _Language 2_ is a fine programming tool for many applications.
  * Third prize: _Language 3_ is not too shabby.
  * Winner of the lightning division: _Language L_ is very suitable for rapid prototyping.
  * Judges' prize: _Team X_ are an extremely cool bunch of hackers.

The contest presents a different programming challenge every year, and you can read about the past ones on Wikipedia.  There's usually an elaborate task description of some kind, which is unveiled on the internet at noon on the Friday the contest begins, which may or may not be a convenient time depending on the time zone you're in.

This year, as I mentioned, the contest was organized by PSU, so it started at noon Portland time on Friday, July 11.  Alex and I were in Atlanta, Georgia, three hours later, so the task description was unveiled at 3 p.m. our time, and we jumped in!

The task description told us, "NASA is seeking examples of real-time control software to operate its latest model Martian rovers from control centers on Earth."  Our task was to write software that would be able to send and receive data from a rover traveling over the surface of Mars.  In particular we'd have to navigate around a rectangular area, avoiding craters and Martians, and having to steer around boulders, in an attempt to get to home base which would always be at the center of the rectangle.  Your contest entry would be scored on how quickly you could navigate to home base while avoiding obstacles.  Lower scores were better, so you would gain points for the time you took.

According to the rules of the contest, boulders were bad to run into, but not deadly.  You'd gain points for running into a boulder, and you'd bounce off of it but not die.  If you hit a crater, though, you would crash into it and die.  And if you hit a Martian it would kill you.

So, at this point, we didn't know yet how we were going to have the rover move around, but the first thing that we wanted to do was try to establish two-way communication between the rover and controller, or between Mars and Earth.  That is, we had to be able to both send and receive messages.

The format of the messages we'd be receiving from Mars was something that the contest organizers had come up with.  Luckily, they gave us very specific details of what these messages would look like!  So there are two kinds of messages, initialization messages and telemetry messages.  So the first thing that you see is a letter I, which is short for "initialization".  I is the message tag signifying initialization; dx is how wide the map is across; dy is how tall the map is, up and down; time-limit is the amount of time you have to finish, meaning get to the middle; min-sensor and max-sensor are the minimum and maximum range of your visual sensors; max-speed is your maximum speed,
max-turn is your maximum rotational speed when turning; and max-hard-turn is your maximum rotational speed when turning hard.

So, you get one message that looks like that.  Almost every message you receive for the rest of the session will be a "telemetry" message.  A telemetry message starts with the letter T, followed by: time-stamp, the number of milliseconds since you started; vehicle-ctl, the current state of the vehicle controls; vehicle-x, your x-coordinate; vehicle-y your y-coordinate; vehicle-dir, your current direction, vehicle-speed, your current speed; and objects a list of obstacles or Martians that are in visual range.

An Object message, in turn, has its own format: object-kind, which is b for boulder, c for crater, m for Martian, or h for home base; object-x, the x-coordinate of the object's center; object-y, the y-coordinate of the object's center; and object-r, the radius of the object.  If the object is a Martian, the description will start with m, and it'll have direction and speed, because Martians move, unlike boulders and craters!

This is almost it for the messages you'll be receiving from the rover on Mars.  There are a few other messages.  There are three kinds of "unhappy occurrence" messages: you hit a boulder, you fell into a crater, you got killed by a Martian.  And there's a "success" message when you reach the center.  There's also a an "end-of-run" message which gets sent either when you succeed or when you die.

Now, your job as the controller is to respond to all these messages coming from the rover and somehow react to them by sending messages back.  There are only four things that you can tell the rover to do -- can anyone guess what they are?  Turn left, turn right, brake, accelerate.  That's it!

So, we were sending these messages back and forth via TCP, which is one of the networking protocols of the Internet, so, a lot of programming languages have some kind of support for it.  I had never done TCP in Scheme before, but we found a great article by Shriram Krishnamurthi about networking in Scheme.  (Incidentally, he's one of the authors of How to Design Programs, which is another great book that uses Scheme.)  The particular flavor of Scheme we were using, which is called PLT Scheme, which has a networking library called, surprisingly enough, scheme/tcp, which we used.

I'm not going to show all of the code that we wrote to parse messages coming from Mars, although some of it is cool -- it's all in our repository for you to look at if you want to.  But I'll quickly show the code that sets up the TCP connection in the first place, and I'll show the code that sends messages TO Mars, and then I'll show a simplified version of what the main loop of our program did at this point.

So this was as far as we got on the first day, Friday.  We had two-way communication set up, but we weren't really doing anything cool with the messages we were receiving, and we weren't really telling our rover to do anything, either!

Saturday started.  We knew we wanted to get our rover to get to the center of the map.  So, I had an extremely sophisticated plan for doing this:
  * Figure out which way home is.
  * Go there!

I got to dig out my 11th-grade trigonometry for this.  I realized that if we know where we are (which we do know, from the telemetry data), and if we know where home is (which we know because it's always the origin, zero-zero), then we can use trigonometry to figure out what direction home is.  This angle here is theta, the tangent of this angle, opposite over adjacent...If this is confusing, I should explain that the hardest part of the competition for me was believing that this always worked.  I don't have a great intuitive sense for geometry, and I kept saying "Well, yeah, but what about on the other side of the y-axis?" and so on and so on.  I actually had to sequester myself for three hours with pencil and paper until I convinced myself of this basic geometry.  Once I was able to get past that, we were fine.

So, earlier, when I said there were cool things that I wasn't mentioning about the way we wrote the code that parses messages coming from Mars?  One of those things that I thought was cool was that we defined data structures for each of those kinds of messages.  So we had a data structure called "telemetry".  And we passed these telemetry structs around all the time.  Every time you see "t" in the first line of a procedure definition here, that's a telemetry struct.  And we're able to grab information out of that struct (like the x and y coords of our rover, or the direction we're currently facing) using some procedures that were defined on that telemetry struct.

So we wrote "direction-to"...and once we had "direction-to" we were able to write all kinds of code based on it.

So at this point...great.  We know how to figure out which way home is, we know how to go that way.  It's the end of the day Saturday...

...Now we want to figure out how to evade obstacles: that is, boulders, We're getting all this telemetry data coming at us, every few milliseconds, and often, it's about obstacles we don't care about!  So, we decided that we only cared about obstacles that meet two criteria.  One, they're near us, and two, we're moving toward them.  So we defined these two predicates, "nearby?" and "moving-toward?"

And with those we were able to define a predicate called "need-to-be-worried?" which I'm not going to show, since I've shown a lot of code, but it looks at a particular item and tells us whether or not we should care!  And finally, based on that, we defined an "anything-worrying?" predicate that iterates through everything in the "objects" list and tells us if there's anything we need to worry about in it.

You'll notice that there's one thing that I didn't really talk about here, which was that we don't do any fancy pathfinding.

Our rover has two modes, GO-HOME and EVADE (which are also our team's preferred two modes of social interaction), which are implemented as a
stack, CURRENT-STRATEGY. The GO-HOME mode is always the bottom-most item on
the stack. On each iteration through our main loop, the ANYTHING-WORRYING?
predicate examines each of the objects in our view and lets us know if we
should be concerned about any of them. If not, we happily continue toward the
center of the map; if so, we evade the bad stuff using an extremely
sophisticated pathfinding algorithm known as "accelerate and turn left".

Thanks!