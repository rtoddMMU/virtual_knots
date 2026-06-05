# To-Do

## Bugs
[ ] Fix the comutation of the Euler characteristic of the carter surface

[ ] Need to fix the arc routing from a crossing to itself
- exclude the case of a creating a small local component: strand 0 to iteslf or strand 1 to itself.
- from strand 0 to strand 1: no problem. That's a small RI move. Should it be removed? It the compoents are still all cc
- from strand 1 to strand 0: this has nontrivial behavior. I'll to check the cases to see if we can still arrive at all circles being cc oriented. 

## Features
[ ] Impliment rectangular diagram for finding virutal crossings.
- arc routing
- line sweep
- add virutal crossing
- etc.

[ ] Impliment Vogel's algoirht part 1:
- by constructon all seifert components are oriented cc
- find non-nested cicles
- perfom vRII move
- update seifert circles
- continue untill all circle are nested

[ ] Impliment Vogel's algorithm part 2:
- index nested circles from inside out ( or whatever)
- construct seifert circle graph
- read around cc and build braid word
[ ] Impliment Micah's computation (from mathematica) for computation of gl(m|n) invariants in braid form

## Future Features
[ ] Add PD (Planar Diagram) code parser

[ ] Add DT (Dowker-Thistlethwaite) code parser

[ ] Knot simplification algorithms

[ ] other invariants? 