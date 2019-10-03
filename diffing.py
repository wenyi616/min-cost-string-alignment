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
        assert(len(self.s_char) == 1), "s_char should be length 1"
        assert(len(self.t_char) == 1), "t_char should be length 1"

# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i,j) for you.
def fill_cell(table, i, j, s, t, cost):
    c1 = cost(s[j-1],'-')
    c2 = cost('-',t[i-1])
    c3 = cost(s[j-1],t[i-1])
    
    if(i==0 and j==0):
        return DiffingCell('-','-', 0)
    
    if(i==0 and j!=0): # first row
        c = c1 + table.get(i,j-1).cost
        return DiffingCell(s[j-1],'-', c)
    
    if(i!=0 and j==0): # first column
        c = c2 + table.get(i-1,j).cost
        return DiffingCell('-',t[i-1], c)
    
    # print choices
#    print(i,j)
#    print("choices are: %d , %d , %d" %
#    (cost('-',t[i-1])    + table.get(i-1,j).cost,        # up
#    cost(s[j-1],t[i-1]) + table.get(i-1,j-1).cost,      # match
#    cost(s[j-1],'-')    + table.get(i,j-1).cost))        # left

    
    cell_cost = min(
            c2    + table.get(i-1,j).cost,      # up
            c3 + table.get(i-1,j-1).cost,       # match
            c1    + table.get(i,j-1).cost)      # left

    if (cell_cost == c2 + table.get(i-1,j).cost):      # up
        return DiffingCell('-', t[i-1], cell_cost)
        
    elif (cell_cost == c3 + table.get(i-1,j-1).cost):  # match
        return DiffingCell(s[j-1], t[i-1], cell_cost)
    else:                                              # left
        return DiffingCell(s[j-1], '-', cell_cost)
    
    return DiffingCell('', '', cell_cost)


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
    align_s = ''
    align_t = ''
    
    row = len(t)
    col = len(s)  
    c = table.get(row,col).cost
    
    while (row >= 0 and col >= 0):        
        cell = table.get(row,col)
        if (cell.s_char == '-' and cell.t_char == '-'):
            # print("reach (0,0)")
            row = row - 1
            col = col - 1
            
        elif (cell.s_char == '-' and cell.t_char != '-'):     # up
            # print("upup")
            align_s = cell.s_char + align_s
            align_t = cell.t_char + align_t
            row = row - 1
            
        elif (cell.s_char != '-' and cell.t_char == '-'):     # left
            # print("left")
            align_s = cell.s_char + align_s
            align_t = cell.t_char + align_t
            col = col - 1
            
        elif (cell.s_char != '-' and cell.t_char != '-'):     # diag
            # print("diag")
            align_s = cell.s_char + align_s
            align_t = cell.t_char + align_t
            row = row - 1
            col = col - 1
    
    # print("done backtrace")
    return (c, align_s , align_t )

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


# another quicky sanity check example
# generated_example_49
# bbwwqb;rvbrrb;16

#    def costfunc(s_char, t_char):
#        if s_char == t_char: return 0
#        if s_char == 'b':
#            if t_char == 'y': return 7
#            if t_char == 'r': return 9
#            if t_char == 'v': return 3
#            if t_char == 't': return 4
#            if t_char == 'b': return 0
#            if t_char == '-': return 2
#        if s_char == 'q':
#            if t_char == 'y': return 4
#            if t_char == 'r': return 4
#            if t_char == 'v': return 2
#            if t_char == 't': return 5
#            if t_char == 'b': return 1
#            if t_char == '-': return 8
#        if s_char == 'w':
#            if t_char == 'y': return 4
#            if t_char == 'r': return 3
#            if t_char == 'v': return 6
#            if t_char == 't': return 4
#            if t_char == 'b': return 3
#            if t_char == '-': return 4
#        if s_char == '-':
#            if t_char == 'y': return 5
#            if t_char == 'r': return 4
#            if t_char == 'v': return 7
#            if t_char == 't': return 6
#            if t_char == 'b': return 9
#
#    s = "bbwwqb"
#    t = "rvbrrb"
#    
#    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1, cell_ordering(len(s), len(t)), fill_cell)
#    D.fill(s = s, t = t, cost=costfunc)
#    (cost, align_s, align_t) = diff_from_table(s,t, D)
#    print align_s
#    print align_t
#    print "cost was %d"%cost