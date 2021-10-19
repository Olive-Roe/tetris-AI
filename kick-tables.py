#kick table for jlszt pieces
jlszt_table = {'0->R': ['(0, 0)', '(-1, 0)', '(-1, 1)', '(0, -2)', '(-1, -2)', 'R->0'], '(0, 0)': ['(1, 0)', '(1, -1)', '(0, 2)', '(1, 2)', 'R->2', '(0, 0)'], '(1, 0)': ['(1, -1)', '(0, 2)', '(1, 2)', '2->R', '(0, 0)', '(-1, 0)'], '(-1, 1)': ['(0, -2)', '(-1, -2)', '2->L', '(0, 0)', '(1, 0)', '(1, 1)'], '(0, -2)': ['(1, -2)', 'L->2', '(0, 0)', '(-1, 0)', '(-1, -1)', '(0, 2)'], '(-1, 2)': ['L->0', '(0, 0)', '(-1, 0)', '(-1, -1)', '(0, 2)', '(-1, 2)'], '0->L': ['(0, 0)', '(1, 0)', '(1, 1)', '(0, -2)', '(1, -2)', '']}
#kick table for i pieces
i_table = {'0->R': ['(0, 0)', '(-2, 0)', '(1, 0)', '(-2, -1)', '(1, 2)', 'R->0'], '(0, 0)': ['(2, 0)', '(-1, 0)', '(2, 1)', '(-1, -2)', 'R->2', '(0, 0)'], '(-1, 0)': ['(2, 0)', '(-1, 2)', '(2, -1)', '2->R', '(0, 0)', '(1, 0)'], '(-2, 0)': ['(1, -2)', '(-2, 1)', '2->L', '(0, 0)', '(2, 0)', '(-1, 0)'], '(2, 1)': ['(-1, -2)', 'L->2', '(0, 0)', '(-2, 0)', '(1, 0)', '(-2, -1)'], '(1, 2)': ['L->0', '(0, 0)', '(1, 0)', '(-2, 0)', '(1, -2)', '(-2, 1)'], '0->L': ['(0, 0)', '(-1, 0)', '(2, 0)', '(-1, 2)', '(2, -1)']}
#kick table for 180 degree rotations
flip_table = {'0->2': ['(0, 0)', '(0, 1)', '(1, 1)', '(-1, 1)', '(1, 0)', '(-1, 0)'], '2->0': ['(0, 0)', '(0, -1)', '(1, -1)', '(-1, 0)', '(-1, 0)', '(1, 0)'], 'R->L': ['(0, 0)', '(1, 0)', '(1, 2)', '(1, 1)', '(0, 2)', '(0, 1)'], 'L->R': ['(0, 0)', '(-1, 0)', '(-1, 2)', '(-1, 1)', '(0, 2)', '(0, 1)']}