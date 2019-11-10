# random-choices-unit-test
Practice of using python ```unittest'''

### Dependencies
* python 3

### Description
Given a set of items and the corresponding weights, generate random choices of items according to the weights. If no weights are given, uniform sampling will be performed.

A variety of test cases are created accordingly:
* ```search_interval'''
  * has only one interval to search
  * searched item cannot be found in the range of the list
  * best case (O(1))
  * worst case (O(log(n))
  * with negative intervals
  
* ```accumulate'''
  * single element
  * multiple elements(float, integer, string)

* ```random_choice'''
  * the given population is not a sequence or a set
  * the number of items and weights mismatch
  * invalid ```k'''
  * weights not sum up to 1
  * multiple 0s in weights
  * single item
  * multiple items (w/ or w/o pre-defined weights)
