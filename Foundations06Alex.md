# One #
"Let Σ be a finite alphabet. Prove that Σ`∗` is a countable set."

To show that a set is countable, we'll want to establish a bijection with the natural numbers. We can do that. Σ`∗` is the "Kleene star" operation on that alphabet; the set of all strings of zero or more members of Σ.

We'll use something like a diagonalization argument. First, assume some arbitrary ordering on the (finite) members of Σ.

The first string is the empty string.

Then we follow with all of the length 1 strings, one for each member of Σ (generated by choosing each element of Σ in turn). There are |Σ| of these, and thus, we've generated the first |Σ| + 1 strings in Σ`∗`.

Then we follow with all of the length 2 strings, which can be generated by choosing each x in Σ in turn, and appending to it each y in Σ. There are |Σ| `*` |Σ| such strings xy; now we've generated 1 + |Σ| + |Σ| `*` |Σ| strings.

To generate all of the strings of length n, for n > 2, we choose each x in Σ in turn, and for that x, append each string s of length n - 1. There are |Σ|^n strings of length n.

Now we've defined a mapping from the natural numbers to the strings in Σ`*`, to go the other way (from a string to a natural number), simply start generating strings with the algorithm given above and count how many strings have been generated before you get to your target string.