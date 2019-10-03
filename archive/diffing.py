"""
Created on Wed Oct  2 21:20:06 2019

@author: Wenyi Chu (wc625)
HW1 partner: Qixin Ding ()
"""


import dynamic_programming

# DO NOT CHANGE THIS CLASS
class DiffingCell:
    def __init__(self, s_char, t_char, cost):
        self.cost = cost
        self.s_char = s_char
        self.t_char = t_char
        self.validate()

    # Helper function so Python can print out objects of this type.
    def __repr__(self):
        return "(%d,%s,%s)"%(self.cost, self.s_char, self.t_char)

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.cost) == int), "cost should be an integer"
        assert(type(self.s_char) == str), "s_char should be a string"
        assert(type(self.t_char) == str), "t_char should be a string"
#        assert(len(self.s_char) == 1), "s_char should be length 1"
#        assert(len(self.t_char) == 1), "t_char should be length 1"

# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i,j) for you.
def fill_cell(table, i, j, s, t, cost):

    if(i==0 and j==0):
        return DiffingCell('','', 0)
    
    if(i==0 and j!=0): # first row
        s_new = table.get(i,j-1).s_char + s[j-1]
        t_new = table.get(i,j-1).t_char  + '-'
        c = cost(s[j-1],'-')+ table.get(i,j-1).cost
        return DiffingCell(s_new,t_new, c)
    
    if(i!=0 and j==0): # first column
        s_new = table.get(i-1,j).s_char + '-'
        t_new = table.get(i-1,j).t_char + t[i-1]
        c = cost('-',t[i-1]) + table.get(i-1,j).cost
        return DiffingCell(s_new,t_new, c)
    
    # print choices
#    print(i,j)
#    print("choices are: %d , %d , %d" %
#    (cost('-',t[i-1])    + table.get(i-1,j).cost,        # up
#    cost(s[j-1],t[i-1]) + table.get(i-1,j-1).cost,      # match
#    cost(s[j-1],'-')    + table.get(i,j-1).cost))        # left

    
    cell_cost = min(
            cost('-',t[i-1])    + table.get(i-1,j).cost,        # up
            cost(s[j-1],t[i-1]) + table.get(i-1,j-1).cost,      # match
            cost(s[j-1],'-')    + table.get(i,j-1).cost)        # left

    if (cell_cost == cost('-',t[i-1]) + table.get(i-1,j).cost):         # up
        s_new = table.get(i-1,j).s_char + '-'
        t_new = table.get(i-1,j).t_char + t[i-1]
        
    elif (cell_cost == cost(s[j-1],t[i-1]) + table.get(i-1,j-1).cost):  # match
        s_new = table.get(i-1,j-1).s_char + s[j-1]
        t_new = table.get(i-1,j-1).t_char + t[i-1]
    else:                                                               # left
        s_new = table.get(i,j-1).s_char + s[j-1]
        t_new = table.get(i,j-1).t_char + '-'
    
    return DiffingCell(s_new, t_new, cell_cost)


# Input: n and m, represents the sizes of s and t respectively.
# Should return a list of (i,j) tuples, in the order you would like fill_cell to be called
def cell_ordering(n,m):
    result = []
    for i in range (n+1):
        base_case_row = (0,i)
        result.append(base_case_row)
    
    for i in range (1,m+1):
        base_case_col = (i,0)
        result.append(base_case_col)
    
    for i in range (1,n+1):
        for j in range (1,m+1):
            tuple = (i,j)
            result.append(tuple)

    return result

# Returns a size-3 tuple (cost, align_s, align_t).
# cost is an integer cost.
# align_s and align_t are strings of the same length demonstrating the alignment.
# See instructions.pdf for more information on align_s and align_t.
def diff_from_table(s, t, table):
    # TODO: YOUR CODE HERE
    cell = table.get(len(s),len(t))
    return (cell.cost, cell.s_char , cell.t_char)

# Example usage
if __name__ == "__main__":
    
    # cost table
    # Example cost function from instructions.pdf
    def costfunc(s_char, t_char):
        if s_char == t_char: return 0
        if s_char == 'a':
            if t_char == 'b': return 5
            if t_char == 'c': return 3
            if t_char == '-': return 2
        if s_char == 'b':
            if t_char == 'a': return 1
            if t_char == 'c': return 4
            if t_char == '-': return 2
        if s_char == 'c':
            if t_char == 'a': return 5
            if t_char == 'b': return 5
            if t_char == '-': return 1
        if s_char == '-':
            if t_char == 'a': return 3
            if t_char == 'b': return 3
            if t_char == 'c': return 3

    s = "acb"
    t = "baa"
    
    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1, cell_ordering(len(s), len(t)), fill_cell)
    D.fill(s = s, t = t, cost=costfunc)
    (cost, align_s, align_t) = diff_from_table(s,t, D)
    print align_s
    print align_t
    print "cost was %d"%cost
    
#    print(cell_ordering(len(s), len(t)))
    
#    for i in range(4):
#        for j in range(4):
#            print("curr: %d, %d, cost:%d" % (i,j,
#                    D.get(i,j).cost))
