# Trees: Evaluation of user-generated trees against gold standards

***

### Requirements

The script is written in python 3

The only requirement is the [Zhang-Sasha tree edit distance module](https://pythonhosted.org/zss/) but *numpy* and *editdist* are also recommended:

```bash
pip install zss
```

Refer to the module's webpage for details and alternatives.


***
### Data

The main script, `trees/evaluate.py`, expects data to be located in `data/`, with one subfolder per true tree. All the other XML-files in this subfolder are evaluated against this true tree. The true tree should be named *gold.xml*

***

### Example
The folder `data/test` comes with one true tree (*gold.xml*) and two user-generated trees

To evaluate these trees just pass the data subfolder as an argument to `evaluate.py`

```python
python trees/evaluate.py --data test/ 
```

The following output should be printed

```bash
### Data ###
test/


Evaluating test-student-1.xml
Distance: 17.0
Normalized distance: 0.30357142857142855


Evaluating test-student-2.xml
Distance: 27.0
Normalized distance: 0.48214285714285715
```

*Normalized distance* is the raw edit distance between the two trees divided by the number of nodes of the true tree. Intuitively, the more nodes the true tree has, the higher is the likelihood that the user-generated tree will deviate from it. This is a simple (too simplistic maybe?) way to compare distances across differently sized trees.


### Spelling alternatives
The current implementation collects spelling alternatives for part of speech tags in a dictionary named *dict_of_spelling_alternatives* in `evaluate.py`. For instance, we don't want a node labeled *det* to be evaluated as being different from *DET*; *Determiner*, or *Det*. Prior to evaluation, every label is lowercased but for more "involved" differences, spelling alternatives need to be manually added to the dictionary.


### TO DO / Issues

  * Handle exception if user-generated tree does not have a root labeled *S*. Currently, the script would break if not. 
  * Internally, nodes are labeled with a unique identifier to be able to keep track of non-unique labels (e.g. *NP* appearing thrice in a tree). This could lead to an over-penalization of trees in cases in which *NP1* is missing and therefore *NP2* (as labeled by the gold standard) is named *NP1* in the user-generated tree.
  * Currently, the we use the "standard" tree edit distance of ZSS^[`zss.simple_distance` see [https://pythonhosted.org/zss/](https://pythonhosted.org/zss/) for details and alternatives ] but it's unclear whether this is the most useful way of scoring trees against the true tree.
  * Save dictionary of spelling alternatives separately from `evaluate.py`