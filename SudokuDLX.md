﻿#summary Automatic Sudoku solving with DLX
#labels Featured,Sudoku,DLX
# Automatic Sudoku Solving with Dancing Links #
[Alex Rudnick](Alex.md)

If you've done some reading about automatic puzzle solving, you may have heard about [Dancing Links](http://en.wikipedia.org/wiki/Dancing_links), or DLX. It's a surprisingly fast constraint-satisfaction algorithm by [Donald Knuth](http://en.wikipedia.org/wiki/Donald_Knuth), and it works very well for solving sudoku.

My implementation of Dancing Links, and a sudoku solver implemented on top of that, is [available](http://code.google.com/p/narorumo/source/browse/#svn/trunk/sudokusolver) in the repository of this project. It's also [running on App Engine](http://sudokudlx.appspot.com). Here, I intend to give a clear description of how to use DLX to solve sudoku, and in a forthcoming writeup, I'll talk about implementing Dancing Links. Knuth's [original paper](http://www-cs-faculty.stanford.edu/~knuth/preprints.html) describes the algorithm in detail, but I found it pretty dense, and I think some extra discussion will be helpful.

## Solving Sudoku automatically ##
So first, I'd like to talk a bit about automatic sudoku-solving in general, then I'll get into how to apply DLX to sudoku. There are two common approaches to solving sudoku programmatically. One of them attempts to solve the problem entirely by "logic", this is to say, by forward-chaining inferences until you've reached a complete solution. This is something like the approach taken by human sudoku aficionados. While in general, published sudoku puzzles only have one valid solution, this approach can't solve an under-constrained puzzle.

The other approach is what a computer scientist would call "recursive search", but human sudoku players call "guessing" or ["Ariadne's Thread"](http://en.wikipedia.org/wiki/Ariadne%27s_thread_(logic)). In this style of play, we make an assumption ("let's say that this square here is a 9") and then follow along with that until we have to abandon it. At any given point, if we don't know what to do, we try something, always ready to unwind our suppositions when we find out they can't be true. With sudoku, since puzzles usually only have one answer, if your search algorithm tries all possible assumptions then you're guaranteed to find the answer through search. In the case of an under-constrained problem, one with more than one answer, you'll still always find a solution; you could find all of them, if you like.

As an aside, this does not have to be complicated. You could imagine writing a solver that does the dumbest possible search, cycling through each number for each square and checking for a solved puzzle. And it would find an answer, but it might take a while because you could end up searching through 9^81 solutions. But we have a better approach!

## What is Dancing Links? ##
Dancing Links (DLX) is an algorithm for solving [set cover](http://en.wikipedia.org/wiki/Set_cover) constraint satisfaction problems, sudoku being easily described as one of those. Let's talk about how to represent sudoku as a set-cover problem.

Say you have a grid of 1s and 0s, and you want to find a subset of the rows such that for every column, there is a single 1 in that column. No column gets more than one. If the first row were all '1's, for example, then the problem would be solved trivially. Here's a small example grid. A solution to this one is to take rows 1, 4, and 5.

```
# Grid 1 has a solution.
row 1: 0 0 1 0 1 1 0 
row 2: 1 0 0 1 0 0 1 
row 3: 0 1 1 0 0 1 0 
row 4: 1 0 0 1 0 0 0 
row 5: 0 1 0 0 0 0 1 
row 6: 0 0 0 1 1 0 1 
```

Note that the solution has exactly one '1' in each column.
```
# Grid 1's solution
row 1: 0 0 1 0 1 1 0 
row 4: 1 0 0 1 0 0 0 
row 5: 0 1 0 0 0 0 1 
```

Here's another grid; this one has no such solution.

```
# Grid 2, no solution.
row 1: 0 0 0 0 0 1 0
row 2: 0 1 0 1 0 0 0
row 3: 0 0 0 0 0 1 1
row 4: 1 1 0 1 0 0 0
row 5: 0 0 0 1 0 0 0
```

## How do I apply it to Sudoku? ##
At first, let's assume we have some software that can find solutions to these "exact cover" problems (this is where Dancing Links comes in) -- given a bunch of rows of 0s and 1s, it finds a subset of those rows such that there's exactly one 1 in every column. If we can represent a sudoku board in terms of these grids -- which we can -- then we're set!

In sudoku, there are four kinds of constraints: each cell must have a number in it; each row must have each number (1 through 9) once; each column must have each number once; and each box (3x3 area) must have each number once. To represent these constraints, we'll build a Dancing Links grid like the ones described in the previous section, in which each column represents one of these. There are 324 constraints total (81 of each of 4 types), so 324 columns.

Each row in the grid represents one possible assignment. For example, a row in the DLX grid might describe the idea that there is a 3 in the fifth row, second column. This assignment "contributes" exactly 4 '1's to the grid, one for each of the constraint types. When we've found a solution, we'll have picked 81 rows, each one of which has four '1's in it, exactly covering each of 324 columns.

Take a moment to consider this: a solved sudoku puzzle has exactly 81 assignments, one for each square, so it will have 81 rows in the DLX solution, each filling in 4 of the 324 columns.

### Row-Column Constraints ###
The first 81 columns of a row (representing an assignment) describe the row and column that it fills in -- we describe this as `rowR colC` where `R` and `C` are the row and column in the sudoku puzzle. So if the assignment is for row 3, column 5, then it gets a '1' for constraint `row3 col5`, and a 0 for each other row and column -- it doesn't satisfy those constraints.

### Row-Number, Column-Number and Box-Number Constraints ###
In the next 81 columns of the DLX row, we'll describe on which row the assignment falls, and what number it assigns. Much like the Row-Column constraints, we can write this as `rowR numN`. Then we'll do the analogous thing for Column-Number and Box-Number constraints -- we'll write down which row (or column or box) an assignment describes, and which number it assigns. And that handles the other three types of constraints, and the second, third and fourth 81-column sections.

Here's how I numbered the 9 "boxes" used in sudoku. Note the zero-indexing; it makes the math in the next section slightly easier.

```
def row_col_to_box(row, col):
  """Return the index for the box that the given (r, c) sudoku coordinates fits
  into. Boxes go like this:
  0 1 2
  3 4 5
  6 7 8
  """
  return (row - (row % 3)) + (col / 3)
```

### Mapping an assignment to a DLX row ###
So for a given assignment (the idea that for row R and column C, you'll put value V) you need to produce a list of 0s and 1s, 324 elements long. To do this, we'll produce four lists of 81 elements and concatenate them. For each constraint, we've got two numbers: row/column, row/number, column/number, and box/number. For ease of math, we'll assume that they're all zero-indexed; call the first number the "major" number and the second one the "minor" (my terminology). Now we just put a 1 in each 81-element list at a place that uniquely identifies the major and minor numbers.

```
def encode(major, minor):
  """Build a list of 81 values, with a 1 in the spot corresponding to the value
  of the major attribute and minor attribute."""
  out = [0] * 81
  out [major*9 + minor] = 1
  return out
```

Once we build these four lists and concatenate them together, we've represented a single assignment.

### Mapping a whole sudoku puzzle into a DLX problem ###
Now we have to turn a sudoku board into a DLX grid. Since the initial DLX grid describes the set of possible assignments, we map what we know about each square onto one or more rows. When you're given a sudoku board, each square is either already filled, or it's left blank. For the squares that are already filled, you generate the one row that describes that assignment. Otherwise, generate the possibility that it's each number, 1 through 9. Although I haven't tried it, I suspect you could do something more clever here and not generate _every_ row, front-loading some of your inferencing; there may be an optimization lurking here, but on the other hand, DLX may be so fast as to make trying something clever counter-productive.

Build up your list of possible assignments, and you have a big Dancing Links grid. It will have between 81 (for a totally filled board) and 729 (totally blank board) rows in it. Set your DLX solver loose on it and bask in glory.

### Mapping a solved DLX grid to a solved Sudoku board ###
Once your DLX solver is done, you'll have 81 rows that describe a solved sudoku board. The only thing left is to extract the solution from those DLX rows. To do this, we look at each row in the solution and grab the row/column information out of the first "constraint" area (the first 81 columns), and the value out of the second. This function `dlx_row_to_rcv` takes in a row from your solution and produces a tuple containing that row's row, column, value. (row and column here are still zero-indexed). Map it over your Dancing Links solution.

```
def dlx_row_to_rcv(dlxrow):
  """Pull (row,col,val) out from an encoded DLX list."""
  rowcol = dlxrow[0:81]
  rownum = dlxrow[81: 2*81]

  row,col = decode(rowcol)
  ignore,num = decode(rownum)

  return (row,col,num + 1)

def decode(lst):
  """Take a list of 81 values with a single 1, decode two values out of its
  position. Return them in a tuple (major,minor)."""

  position = lst.index(1)
  minor = position % 9
  major = position / 9
  return (major,minor)
```


## How is it implemented? ##
For my next trick, I'll write up my notes on how to implement DLX itself.