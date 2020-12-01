from pymop import DTLZ1,DTLZ2,DTLZ3,DTLZ4,DTLZ5,DTLZ6,DTLZ7
import wfg
from moeaD import MOEAD
from moeadCoDE import MOEADCODE
from moeadSaDE import MOEADSADE
from moeadde import MOEADDE

models = [MOEAD, MOEADDE, MOEADSADE, MOEADCODE]
models_name = ['MOEAD', 'MOEADDE', 'MOEADSADE', 'MOEADCODE']
problems = [DTLZ1,DTLZ2,DTLZ3,DTLZ4,DTLZ5,DTLZ6,DTLZ7,
            wfg.WFG1,wfg.WFG2,wfg.WFG3,wfg.WFG4,wfg.WFG5,wfg.WFG6,wfg.WFG7,wfg.WFG8,wfg.WFG9]
problems_name = ['DTLZ1','DTLZ2','DTLZ3','DTLZ4','DTLZ5','DTLZ6','DTLZ7',
            'WFG1','WFG2','WFG3','WFG4','WFG5','WFG6','WFG7','WFG8','WFG9']