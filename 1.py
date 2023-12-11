

def find_subsets_with_sum_and_n_elements(arr, S, N):
    subsets = []
    backtrack_for_find_subset(arr, S, N, [], subsets)
    return subsets


def backtrack_for_find_subset(arr, target, N, subset, subsets):
    if target == 0 and len(subset) == N:
        subsets.append(subset[:])
        return
    if target < 0 or len(subset) == N:
        return
    for i in range(len(arr)):
        subset.append(arr[i])
        backtrack_for_find_subset(arr[i+1:], target - arr[i], N, subset, subsets)
        subset.pop()



def flatten_lists(list_of_lists):
    result_set = set()

    for inner_list in list_of_lists:
        for element in inner_list:
            result_set.add(element)

    return result_set







def update_domain_for_sum(domain_of_all_variables, variable_list, target_sum):
    for variable in variable_list:
        valid_values = set()

        # Generate all possible combinations of values for the given variable
        v=variable_list.copy()
        v.remove(variable)
        for value_a in domain_of_all_variables[variable]:
            # Check if there exist values for other variables in the list such that the sum is equal to the target_sum

            if w(domain_of_all_variables,v,(target_sum-value_a),[]):
                valid_values.add(value_a)

        # Update the domain_of_all_variables with values that satisfy the constraint
        domain_of_all_variables[variable] = list(valid_values)


def w(domain_of_all_variables,variable_list,target_sum,pastv):

    if len(variable_list)==1:
        x=domain_of_all_variables.get(variable_list[0])
        if target_sum in x:
            if target_sum in pastv:
                return False
            else:
                return True
        else:
            return False


    for p in variable_list:
        x=domain_of_all_variables.get(p)
        v=variable_list.copy()
        v.remove(p)
        
        for z in x:
            if z in pastv:
                continue
            ppas=pastv.copy()
            ppas.append(z)

            if (w(domain_of_all_variables,v,target_sum-z,ppas)):
                return True
    

    return False
        

#makeing d
def extract_constraints(kakuro_puzzle):
    constraints = {}
    rows, cols = len(kakuro_puzzle), len(kakuro_puzzle[0])

    for i in range(rows):
        for j in range(cols):
            cell_value = kakuro_puzzle[i][j]

            if cell_value != 'X' and cell_value != 0:
                if cell_value.startswith('*'):
                    # Handle star, representing required sum
                    s1=cell_value[1:3]
                    target_sum1=-100
                    target_sum2=-100
                    
                    if s1.isdigit():
                        target_sum2= int(cell_value[1:3])
                        if len(cell_value)<5:
                            constraints[(i, j)] = (target_sum1, target_sum2)

                        else:
                            target_sum1= int(cell_value[5:])
                            constraints[(i, j)] = (target_sum1, target_sum2)

                    else:
                        target_sum1= int(cell_value[2:])
                        constraints[(i, j)] = (target_sum1, target_sum2)

    return constraints





def needpuzzle(kakuro_puzzle,d,b):
    #b =[]
    constraints = {}
    rows, cols = len(kakuro_puzzle), len(kakuro_puzzle[0])

    for i in range(rows):
        br=[]
        for j in range(cols):
            cell_value = kakuro_puzzle[i][j]

            if cell_value == 'X' or (cell_value != 0 and cell_value.startswith('*')):
                br.append(None)
            else:
                br.append(((-100,-100),(-100,-100)))
        b.append(br)

    
    for i in d:
        rl=d.get(i)[0]
        cl=d.get(i)[1]
        target_sum1=0
        target_sum2=0

        if rl==-100:
            target_sum1=-100
        else:
            target_sum1=0
            for j in range(i[1]+1,cols):
                cell_value = kakuro_puzzle[i[0]][j]
                if cell_value == 'X' or (cell_value != 0 and cell_value.startswith('*')):
                    break
                target_sum1=target_sum1+1
                b[i[0]][j]=(i,b[i[0]][j][1])
    

        if cl==-100:
            target_sum2=-100
        else:
            target_sum2=0
            for j in range(i[0]+1,rows):
                cell_value = kakuro_puzzle[j][i[1]]
                if cell_value == 'X' or (cell_value != 0 and cell_value.startswith('*')):
                        break
                target_sum2=target_sum2+1
                b[j][i[1]]=(b[j][i[1]][1],i)





        constraints[(i[0], i[1])] = (target_sum1, target_sum2)








    return constraints


























'''
- 'X' : represents a cell that you don't need to fill.
- Empty cell : represents a cell that you need to fill with a digit (1 - 9).
- Cell with digit : the given digit is part of the solution, don't change it.
- Cell with star at the beginning: the required sum of the corresponding cells.
- X# : the vertical sum X of the cells downwards,
- \\X : the horizontal sum X of the cells to the right
- all numbers must have 2 digits

'''


kakuro_puzzle = [
    ['X', 'X', 'X', '*17#','*28#','X','X'],
    ['X', 'X',  "*27#\\16", 0, 0,"*17#","*17#"],
    ['X', "*11#\\27", 0, 0, 0, 0, 0],
    ['*\\03', 0, 0, "*14#\\19", 0, 0,0],
    ['*\\34', 0, 0, 0, 0, 0,'*17#'],
    ['X', '*\\30', 0, 0, 0, 0,0],
    ['X', '*\\03', 0, 0 , '*\\16', 0,0]
]

# the required sum of the corresponding cells . (location):(row limitation, col limitation)
d = extract_constraints(kakuro_puzzle)
"""
d = {
    (1,2):(16,27),
    (0,3):(-100,17),
    (0,4):(-100,28),
    (1,5):(-100,17),
    (1,6):(-100,17),
    (2,1):(27,11),
    (3,0):(3,-100),
    (3,3):(19,14),
    (4,0):(34,-100),
    (4,6):(-100,17),
    (5,1):(30,-100),
    (6,1):(3,-100),
    (6,4):(16,-100),
    }
"""


b=[]
# number of indexes for each  the required sum of the corresponding cells.
tedad=needpuzzle(kakuro_puzzle,d,b)
"""
tedad= {
    (1,2):(2,5),
    (0,3):(-100,2),
    (0,4):(-100,5),
    (1,5):(-100,5),
    (1,6):(-100,2),
    (2,1):(5,2),
    (3,0):(2,-100),
    (3,3):(3,3),
    (4,0):(5,-100),
    (4,6):(-100,2),
    (5,1):(5,-100),
    (6,1):(2,-100),
    (6,4):(2,-100),
    }

b=[
    [None,None,None,None,None,None,None],
    [None,None,None,((1,2),(0,3)),((1,2),(0,4)),None,None],
    [None,None,((2,1),(1,2)),((2,1),(0,3)),((2,1),(0,4)),((2,1),(1,5)),((2,1),(1,6))],
    [None,((3,0),(2,1)),((3,0),(1,2)),None,((3,3),(0,4)),((3,3),(1,5)),((3,3),(1,6))],
    [None,((4,0),(2,1)),((4,0),(1,2)),((4,0),(3,3)),((4,0),(0,4)),((4,0),(1,5)),None],
    [None,None,((5,1),(1,2)),((5,1),(3,3)),((5,1),(0,4)),((5,1),(1,5)),((5,1),(4,6))],
    [None,None,((6,1),(1,2)),((6,1),(3,3)),None,((6,4),(1,5)),((6,4),(4,6))],

]

"""

domainofpuzzle={}

rowsize, colsize = len(kakuro_puzzle), len(kakuro_puzzle[0])




for i in range (rowsize):
    for j in range(colsize):
        x=b[i][j]
        if x is not None:
            p1=x[0]
            p2=x[1]
            pp1=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p1)[0],tedad.get(p1)[0])
            pp2=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p2)[1],tedad.get(p2)[1])
            f1=flatten_lists(pp1)
            f2=flatten_lists(pp2)
            f=list(f1& f2)
            domainofpuzzle[(i,j)]=f


for state in d:
    z0=d[state][0]
    z1=d[state][1]
    if z0!=-100:
        domin=[]
        t=tedad[state][0]
        for i in range(1,t+1):
            x=(state[0],state[1]+i)
            domin.append(x)
        update_domain_for_sum(domainofpuzzle, domin, z0)




    if z1!=-100:
        domin=[]
        t=tedad[state][1]
        for i in range(1,t+1):
            x=(state[0]+i,state[1])
            domin.append(x)
        update_domain_for_sum(domainofpuzzle, domin, z1)






for i in range (rowsize):
    for j in range(colsize):
        x=b[i][j]
        if x is not None:
            p1=x[0]
            p2=x[1]
            pp1=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p1)[0],tedad.get(p1)[0])
            pp2=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p2)[1],tedad.get(p2)[1])
            f1=flatten_lists(pp1)
            f2=flatten_lists(pp2)
            f=list(f1& f2)
            domainofpuzzle[(i,j)]=f




for state in d:
    z0=d[state][0]
    z1=d[state][1]
    if z0!=-100:
        domin=[]
        t=tedad[state][0]
        for i in range(1,t+1):
            x=(state[0],state[1]+i)
            domin.append(x)
        update_domain_for_sum(domainofpuzzle, domin, z0)




    if z1!=-100:
        domin=[]
        t=tedad[state][1]
        for i in range(1,t+1):
            x=(state[0]+i,state[1])
            domin.append(x)
        update_domain_for_sum(domainofpuzzle, domin, z1)



dd=d.copy()
for s in range(2):
    for i in range(rowsize):
        for j in range(colsize):
            x=b[i][j]
            if x is not None:
                p1=x[0]
                p2=x[1]
                sumrow=d.get(p1)[0]
                sumcol=d.get(p2)[1]

                state=p1
                z0=d[state][0]
                z1=d[state][1]
                domin=[]
                t=tedad[state][0]
                for i in range(1,t+1):
                    x=(state[0],state[1]+i)
                    domin.append(x)
                update_domain_for_sum(domainofpuzzle, domin, sumrow)

                state=p2
                domin=[]
                t=tedad[state][1]
                for i in range(1,t+1):
                    x=(state[0]+i,state[1])
                    domin.append(x)
                update_domain_for_sum(domainofpuzzle, domin, sumcol)



            













print("Kakuro Puzzle:")
for row in kakuro_puzzle:
    for x in row:
        print(str(x).ljust(9),end="\t|")
    print("")





qq=kakuro_puzzle.copy()
print(" solution level 1: ")
for i in range(rowsize):
    for j in range(colsize):
        if kakuro_puzzle[i][j]==0:
            x=domainofpuzzle.get((i,j))
            qq[i][j]=x[0]



for row in qq:
    for x in row:
        print(str(x).ljust(9),end="\t|")
    print("")



















#level_2
print("\n\n level_2 : with LCV: ")

def update_domain_for_sum_b(domain_of_all_variables, variable_list, target_sum):
    # Sort variables by MRV (minimum remaining values)
    sorted_variables = sorted(variable_list, key=lambda var: len(domain_of_all_variables[var]))

    for variable in sorted_variables:
        valid_values = set()

        
        v = sorted_variables.copy()
        v.remove(variable)

        # Sort values by LCV (least constraining value)
        sorted_domain = sorted(domain_of_all_variables[variable],key=lambda value: count_conflicts(domain_of_all_variables, v, value))


        for value_a in sorted_domain:
            
            if ww(domain_of_all_variables, v, (target_sum - value_a), []):
                valid_values.add(value_a)

        
        domain_of_all_variables[variable] = list(valid_values)


def count_conflicts(domain_of_all_variables, variable_list, value):
    conflicts = 0

    for variable in variable_list:
        # Check if there exist values for other variables in the list such that the value conflicts
        if value in domain_of_all_variables.get(variable, []):
            conflicts += 1

    return conflicts

def ww(domain_of_all_variables,variable_list,target_sum,pastv):

    if len(variable_list)==1:
        x=domain_of_all_variables.get(variable_list[0])
        if target_sum in x:
            if target_sum in pastv:
                return False
            else:
                return True
        else:
            return False


    for p in variable_list:
        x=domain_of_all_variables.get(p)
        v=variable_list.copy()
        v.remove(p)

        sorted_domain = sorted(x,key=lambda value: count_conflicts(domain_of_all_variables, v, value))


        for z in sorted_domain:
            if z in pastv:
                continue
            ppas=pastv.copy()
            ppas.append(z)

            if (ww(domain_of_all_variables,v,target_sum-z,ppas)):
                return True
    

    return False
        






'''
- 'X' : represents a cell that you don't need to fill.
- Empty cell : represents a cell that you need to fill with a digit (1 - 9).
- Cell with digit : the given digit is part of the solution, don't change it.
- Cell with star at the beginning: the required sum of the corresponding cells.
- X# : the vertical sum X of the cells downwards,
- \X : the horizontal sum X of the cells to the right

'''


kakuro_puzzlee = [
    ['X', 'X', 'X', '*17#','*28#','X','X'],
    ['X', 'X',  "*27#\\16", 0, 0,"*17#","*17#"],
    ['X', "*11#\\27", 0, 0, 0, 0, 0],
    ['*\\3', 0, 0, "*14#\\19", 0, 0,0],
    ['*\\34', 0, 0, 0, 0, 0,'*17#'],
    ['X', '*\\30', 0, 0, 0, 0,0],
    ['X', '*\\3', 0, 0 , '*\\16', 0,0]
]
rowsize, colsize = len(kakuro_puzzlee), len(kakuro_puzzlee[0])
# the required sum of the corresponding cells . (location):(row limitation, col limitation)

d = extract_constraints(kakuro_puzzlee)
b=[]
# number of indexes for each  the required sum of the corresponding cells.
tedad=needpuzzle(kakuro_puzzlee,d,b)

domainofpuzzlee={}






for i in range (rowsize):
    for j in range(colsize):
        x=b[i][j]
        if x is not None:
            p1=x[0]
            p2=x[1]
            pp1=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p1)[0],tedad.get(p1)[0])
            pp2=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p2)[1],tedad.get(p2)[1])
            f1=flatten_lists(pp1)
            f2=flatten_lists(pp2)
            f=list(f1& f2)
            domainofpuzzlee[(i,j)]=f


for state in d:
    z0=d[state][0]
    z1=d[state][1]
    if z0!=-100:
        domin=[]
        t=tedad[state][0]
        for i in range(1,t+1):
            x=(state[0],state[1]+i)
            domin.append(x)
        update_domain_for_sum_b(domainofpuzzlee, domin, z0)




    if z1!=-100:
        domin=[]
        t=tedad[state][1]
        for i in range(1,t+1):
            x=(state[0]+i,state[1])
            domin.append(x)
        update_domain_for_sum_b(domainofpuzzlee, domin, z1)






for i in range (rowsize):
    for j in range(colsize):
        x=b[i][j]
        if x is not None:
            p1=x[0]
            p2=x[1]
            pp1=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p1)[0],tedad.get(p1)[0])
            pp2=find_subsets_with_sum_and_n_elements(range(1,10),d.get(p2)[1],tedad.get(p2)[1])
            f1=flatten_lists(pp1)
            f2=flatten_lists(pp2)
            f=list(f1& f2)
            domainofpuzzlee[(i,j)]=f




for state in d:
    z0=d[state][0]
    z1=d[state][1]
    if z0!=-100:
        domin=[]
        t=tedad[state][0]
        for i in range(1,t+1):
            x=(state[0],state[1]+i)
            domin.append(x)
        update_domain_for_sum_b(domainofpuzzlee, domin, z0)




    if z1!=-100:
        domin=[]
        t=tedad[state][1]
        for i in range(1,t+1):
            x=(state[0]+i,state[1])
            domin.append(x)
        update_domain_for_sum_b(domainofpuzzlee, domin, z1)



dd=d.copy()
for s in range(2):
    for i in range(rowsize):
        for j in range(colsize):
            x=b[i][j]
            if x is not None:
                p1=x[0]
                p2=x[1]
                sumrow=d.get(p1)[0]
                sumcol=d.get(p2)[1]

                state=p1
                z0=d[state][0]
                z1=d[state][1]
                domin=[]
                t=tedad[state][0]
                for i in range(1,t+1):
                    x=(state[0],state[1]+i)
                    domin.append(x)
                update_domain_for_sum_b(domainofpuzzlee, domin, sumrow)

                state=p2
                domin=[]
                t=tedad[state][1]
                for i in range(1,t+1):
                    x=(state[0]+i,state[1])
                    domin.append(x)
                update_domain_for_sum_b(domainofpuzzlee, domin, sumcol)





qq=kakuro_puzzlee.copy()
print(" solution:  with LCV ")
for i in range(rowsize):
    for j in range(colsize):
        if kakuro_puzzlee[i][j]==0:
            x=domainofpuzzlee.get((i,j))
            qq[i][j]=x[0]



for row in qq:
    for x in row:
        print(str(x).ljust(9),end="\t|")
    print("")












