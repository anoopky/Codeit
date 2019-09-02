def id3(examples, classification_attribute, attributes):
    create a root node for the tree
    if all examples are positive/yes:
        return root node with positive/yes label
    else if all examples are negative/no:
        return root node with negative/no label
    else if there are no attributes left:
        return root node with most popular classification_attribute label
    else:
        best_attribute = attribute from attributes that best
                         classifies examples
        assign best_attribute to root node
        for each value in best_attribute:
            add branch below root node for the value
            branch_examples = [examples that have that value
                               for best_attribute]
            if branch_examples is empty:
                add leaf node with most popular
                    classification_attribute label
            else:
                add subtree id3(branch_examples,
                                classification_attribute,
                                attributes - best_attribute)