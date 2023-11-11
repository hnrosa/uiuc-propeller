from xgboost import DMatrix
import numpy as np
import joblib


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
        
        if Sol is None and Family is None:
            
            self.Solidity = None
            self.ct_model = joblib.load('../../models/CT_General_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_General_model_2023-11-4_15-19.joblib')
            
            self.ct_quantile_model = joblib.load('../../models/CT_General_model_quantile_2023-11-4_15-19.joblib')
            self.cp_quantile_model = joblib.load('../../models/CP_General_model_quantile_2023-11-4_15-19.joblib')
            
            
            M = np.zeros((size, 3))
            
            M[:, 0] = self.J
            M[:, 1] = P/D
            M[:, 2] = N
            
            M_cp = M.copy()
            M_ct = M.copy()
        
        elif Sol is None and Family is not None:
            
            self.Family = Family
            self.ct_model = joblib.load('../../models/CT_Family_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_Family_model_2023-11-4_15-19.joblib')
            
            self.ct_quantile_model = joblib.load('../../models/CT_Family_model_quantile_2023-11-4_15-19.joblib')
            self.cp_quantile_model = joblib.load('../../models/CP_Family_model_quantile_2023-11-4_15-19.joblib')
            
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
            
            self.Solidity = Sol
            self.ct_model = joblib.load('../../models/CT_Solidity_model_2023-11-4_15-19.joblib')
            self.cp_model = joblib.load('../../models/CP_Solidity_model_2023-11-4_15-19.joblib')
            
            self.ct_quantile_model = joblib.load('../../models/CT_Solidity_model_quantile_2023-11-4_15-19.joblib')
            self.cp_quantile_model = joblib.load('../../models/CP_Solidity_model_quantile_2023-11-4_15-19.joblib')
            
            
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
        self.CT_quant = self.ct_quantile_model.predict(M_ct)
        self.CP_quant = self.cp_quantile_model.predict(M_cp)
        
        self.T = rho * n ** 2 * D ** 4 * self.CT
        self.T_quant = rho * n ** 2 * D ** 4 * self.CT_quant
        
        self.P = rho * n ** 3 * D ** 5 * self.CP
        self.P_quant = rho * n ** 3 * D ** 5 * self.CP_quant
        
        self.eta = self.J * self.CT / self.CP
        self.eta_quant = self.J.reshape(-1, 1) * self.CT_quant / self.CP_quant

