#This script uses the Zhang-Shasha Tree edit distance:http://www.grantjenks.com/wiki/_media/ideas:simple_fast_algorithms_for_the_editing_distance_between_tree_and_related_problems.pdf
#Details about the python implementation are found in https://zhang-shasha.readthedocs.io/en/latest/

from zss import simple_distance, Node

def normalize_label(lbl): #catches ortographic variations (e.g., "np" vs. "NP" vs. "Np ") and normalizes spelling
	lbl = lbl.strip(' ').lower()
	if lbl in dict_of_spelling_alternatives:
		lbl = dict_of_spelling_alternatives[lbl]
	return(lbl)


def plant_tree(tag_list):
	nodes_dict = {} #create a dictionary to save the tree nodes we construct along the way
	parent_list = [] #to keep track of family tree
	nm_idx = 0 #unique identifier for each label (in case there are multiple nodes with the same label)
	for t_idx in range(len(tag_list)): #iterate over XML tags
		if 'syntacticstructure' in tag_list[t_idx].split(): #if the tag identifies a node, extract the label of the node
			nm = normalize_label(tag_list[t_idx+1].split('"')[1]) + str(nm_idx) #extract label of the node
			if parent_list == []: #tree initialization. If no previous parent: must be root
				nodes_dict[nm] = Node(nm) #add node to the dictionary
				parent_list.append(nm) #mark it as a parent of everything that follows until we get to a /syntacticstructure tag
			else: #not root node
				nodes_dict[nm] = Node(nm) #is a node
				parent = parent_list[-1] #last element in parent_list is parent
				nodes_dict[parent].addkid(nodes_dict[nm]) #is a child of its parent
				parent_list.append(nm)
			nm_idx += 1
		if '/syntacticstructure>' in tag_list[t_idx].split(): #each time a tag closes, we stop adding children to this branch and go one branch up
			del parent_list[-1]
	return(nodes_dict)



#This dictionary tracks all ortographic variations that count as the same (already lowercased) label. 
dict_of_spelling_alternatives = {'determiner': 'det',
								 'noun': 'n',
								 'verb': 'v',
								 'noun phrase': 'np',
								 'verb phrase': 'vp',
								 'adjective': 'adj'}




with open('trees/ex/lee.xml') as f:
    tag_list=[word for line in f for word in line.split('<')] #split whenever a tag opens

a = plant_tree(tag_list)

print(a['s'].get_children(a['s'])) #shows children of a node
len(a.keys()) #is the total of nodes of a tree. Can be used to normalize scores. 


with open('trees/ex/leeb.xml') as f:
    tag_list=[word for line in f for word in line.split('<')] #split whenever a tag opens

b = plant_tree(tag_list)


simple_distance(a['s0'], b['s0']) / len(a.keys())

