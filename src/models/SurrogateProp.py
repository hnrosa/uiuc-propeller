from collections.abc import Sequence
import numpy as np
import joblib


class SizeError(Exception): 
    """Raised when sequences have different sizes"""
    pass

class SurrogateProp:
    
    def __init__(self, D, P, V, N, rho, Sol = None):
        
        n = N/60
        inputs = [D, P, V, N, rho, Sol]
        seq_map = [isinstance(i, Sequence) for i in inputs]
        s = sum(seq_map)
        vecs = [i for i, s in enumerate(seq_map) if s]
        
        if s == 0:
            size = 1
        
        elif s == 1:
            size = len(inputs[vecs[0]])
            
        else:
            try:
                sizes  = [len(inputs[v]) for v in vecs]
                c = sizes[0] 
                
                if all(x==c for x in sizes):
                    raise SizeError
                
            except SizeError:
                    print('Sequences does not have the same size')
                    print()
            
            else:
                size = len(inputs[vecs[0]])
            
        self.P = P
        self.D = D
        self.V = V
        self.N = N
        self.J = V / (n * D)
        
        if Sol is None:
            self.Solidity = None
            self.ct_model = joblib.load('ct_no_sol.joblib')
            self.cp_model = joblib.load('cp_no_sol.joblib')
            
            M = np.zeros((size, 3))
            
            M[:, 0] = P/D
            M[:, 1] = self.J
            M[:, 2] = N
            
        else:
            self.Solidity = Sol
            self.ct_model = joblib.load('ct_sol.joblib')
            self.cp_model = joblib.load('cp_sol.joblib')
            
            M = np.zeros((size, 4))
            
            M[:, 0] = P/D
            M[:, 1] = self.J
            M[:, 2] = N
            M[:, 3] = Sol
        
        self.CT = self.ct_model.predict(M)
        self.CP = self.cp_model.predict(M)
        
        self.T = rho * n ** 2 * D ** 4 * self.CT
        self.P = rho * n ** 3 * D ** 5 * self.CP
        self.eta = self.J * self.CT / self.CP





