# %%
import math

board = [
        0,0,0,0,1,0,0,0,0,
        0,0,0,3,0,2,0,0,0,
        0,0,9,0,0,0,3,0,0,
        0,2,0,0,0,0,0,4,0,
        3,0,0,0,0,0,0,0,5,
        0,4,0,0,0,0,0,6,0,
        0,0,4,0,0,0,7,0,0,
        0,0,0,1,0,8,0,0,0,
        0,0,0,0,9,0,0,0,0
        ]

rules = ['row','col','quad','knight']

#%%
def create_ind_dict(size, rows, rules=['row','col','quad']):
    ind_dict = {}
    for ind in range(size):
        ind_list = []
        row = int(ind/rows)
        col = ind%rows
        quad = 3*int(row/(rows/3)) + int(col/(rows/3))

        for index in range(size):
            if index == ind: continue
            irow = int(index/rows)
            icol = index%rows

            # Indexes in same row
            if irow == row and 'row' in rules:
                ind_list.append(index)
                continue
            
            # Indexes in same column
            if icol == col and 'col' in rules:
                ind_list.append(index)
                continue
            
            # Indexes in same square
            if 3*int(irow/(rows/3)) + int(icol/(rows/3)) == quad and 'quad' in rules:
                ind_list.append(index)
                continue
            
            # Knight move 
            if 'knight' in rules:
                if abs(col-icol) == 1 and abs(row-irow) == 2:
                    ind_list.append(index)
                    continue
                if abs(col-icol) == 2 and abs(row-irow) == 1:
                    ind_list.append(index)
                    continue
                
            # King move
            if 'king' in rules and abs(row-irow) <= 1 and abs   (col-icol) <= 1:
                ind_list.append(index)
                continue
            
        ind_dict[ind] = sorted(ind_list)
    return ind_dict

#%%
def update_cand_dict(board, ind_dict,numbers, index="All"):
    candidate_dict={}
    if index == 'All':
        for i, v in enumerate(board):
            if v != 0: 
                candidate_dict.pop(i,None)
                continue
            value_list = [board[ind] for ind in ind_dict[i]]
            candidate_dict[i] = sorted(numbers.difference(set(value_list)))
    return candidate_dict

#%%
def initialize(board, rules):
    size = len(board)
    rows = int(math.sqrt(len(board)))
    numbers_set = set(list(range(1,rows+1,1)))
    index_dictionary = create_ind_dict(size, rows, rules)
    candidate_dictionary = update_cand_dict(board, index_dictionary, numbers_set)
    solve(board, index_dictionary, candidate_dictionary, numbers_set)
    return
#%%
def solve(board, index_dictionary, candidate_dictionary, numbers):
    if candidate_dictionary == {}:
        return True
    index = sorted(candidate_dictionary.keys())[0]
    for value in candidate_dictionary[index]:
        board[index] = value
        candidate_dictionary = update_cand_dict(board, index_dictionary,numbers)
        if valid_board(candidate_dictionary) is True:
            
            if solve(board, index_dictionary, candidate_dictionary, numbers):
                return True
            board[index] = 0
            candidate_dictionary = update_cand_dict(board, index_dictionary, numbers)
        board[index] = 0
        candidate_dictionary = update_cand_dict(board, index_dictionary, numbers)

    return False

#%%
def valid_board(candidate_dictionary):
    for index in candidate_dictionary:
        if len(candidate_dictionary[index]) == 0:
            return False
    return True

# %%
def print_board(board):
    for index, value in enumerate(board):
        if index%3 == 0 and index%9 != 0:
            print("|", end='')
        if index%27 == 0 and index != 0:
            print('------+------+-----')
        print(str(value)+' ',end='')
        if (index+1) % 9 == 0:
            print('', end='\n')
# %%
print_board(board)
initialize(board, rules)
print("""
~~~~~~~~~~~~~~~~~~~
""")
print_board(board)