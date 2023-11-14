from xgboost import DMatrix
import numpy as np
import joblib
import pandas as pd


class SizeError(Exception): 
    """Raised when inputs have different sizes"""
    pass

class SurrogateProp:
    
    def __init__(self, D, P, V, N, rho, Sol = None, Family = None):
        
        n = N/60
        inputs = [D, P, V, N, rho, Sol, Family]
        inputs = [np.array(i) for i in inputs]
        sizes = np.array([i.size for i in inputs])
        
        try:
            
            unit_inputs = (sizes == 1)
                
            if unit_inputs.sum() < 6:
                raise SizeError
                
        except SizeError:
            print('More than one inputs is a sequence')
            
        size = sizes.max()
            
        self.P = P
        self.D = D
        self.V = V
        self.N = N
        self.J = V / (n * D)
        self.Solidity = Sol
        self.Family = Family
        
        if Sol is None and Family is None:
            
            self.ct_model = joblib.load('../../models/CT_General_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_General_model_2023-11-4_15-19.joblib')
            
            M = np.zeros((size, 3))
            
            M[:, 0] = self.J
            M[:, 1] = P/D
            M[:, 2] = N
            
            M_cp = M.copy()
            M_ct = M.copy()
        
        elif Sol is None and Family is not None:
            
            self.ct_model = joblib.load('../../models/CT_Family_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_Family_model_2023-11-4_15-19.joblib')
            
            self.cp_encoder = joblib.load('../../models/CP_Family_encoder_2023-11-4_15-19.joblib')
            self.ct_encoder = joblib.load('../../models/CT_Family_encoder_2023-11-4_15-19.joblib')
            
            M = np.empty((size, 4), dtype = object)
            
            M[:, 0] = self.J
            M[:, 1] = P/D
            M[:, 2] = N
            M[:, 3] = Family
            
            M_cp = M.copy()
            M_ct = M.copy()
            
            M_cp[:, 3] = self.cp_encoder.transform(M).iloc[:, 3]
            M_ct[:, 3] = self.ct_encoder.transform(M).iloc[:, 3]
            
            
        else:
            
            self.ct_model = joblib.load('../../models/CT_Solidity_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_Solidity_model_2023-11-4_15-19.joblib')
            
            M = np.zeros((size, 4))
            
            M[:, 0] = self.J
            M[:, 1] = P/D
            M[:, 2] = N
            M[:, 3] = Sol
            
            M_cp = M.copy()
            M_ct = M.copy()
            
        M_cp = DMatrix(M_cp)
        M_ct = DMatrix(M_ct)
        
        self.CT = self.ct_model.predict(M_ct)
        self.CP = self.cp_model.predict(M_cp)
        self.eta = self.J.reshape(-1, 1) * self.CT / self.CP
        
        self.Tr = rho * n ** 2 * D ** 4 * self.CT
        self.Pw = rho * n ** 3 * D ** 5 * self.CP
        
    def to_dataframe(self):
        
        df = pd.DataFrame()
        adim_df = pd.DataFrame()
        
        adim_df['J'] = self.J
        adim_df['P_D'] = self.P / self.D
        adim_df['N'] = self.N
        adim_df['Solidity'] = self.Solidity
        adim_df['Family'] = self.Family
        adim_df['CT'] = self.CT[:, 1]
        adim_df['CT_005'] = self.CT[:, 0]
        adim_df['CT_095'] = self.CT[:, 2]
        adim_df['CP'] = self.CP[:, 1]
        adim_df['CP_005'] = self.CP[:, 0]
        adim_df['CP_095'] = self.CP[:, 2]
        adim_df['eta'] = self.eta[:, 1]
        adim_df['eta_005'] = self.eta[:, 0]
        adim_df['eta_095'] = self.eta[:, 2]
        
        
        df['V'] = self.V
        df['P'] = self.P 
        df['D'] = self.D
        df['N'] = self.N
        df['Solidity'] = self.Solidity
        df['Family'] = self.Family
        df['Tr'] = self.Tr[:, 1]
        df['Tr_005'] = self.Tr[:, 0]
        df['Tr_095'] = self.Tr[:, 2]
        df['Pw'] = self.Pw[:, 1]
        df['Pw_005'] = self.Pw[:, 0]
        df['Pw_095'] = self.Pw[:, 2]
        adim_df['eta'] = self.eta[:, 1]
        adim_df['eta_005'] = self.eta[:, 0]
        adim_df['eta_095'] = self.eta[:, 2]
        
        return adim_df, df
        
        
        
        
        
        
        
        
        
        
        
        
        