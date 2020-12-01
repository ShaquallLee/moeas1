def evaluate(problem, x):
    '''
    计算模型的fitness值
    '''
    if 'WFG' in problem.pname:
        y = problem.problem(x, int(problem.n_var/2), problem.n_obj)
    elif 'DTLZ' in problem.pname:
        y = problem.problem.evaluate(x)
    else:
        print('no problem')
        return None
    return y