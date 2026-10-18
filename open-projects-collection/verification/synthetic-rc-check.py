import json,numpy as np
from impedance.models.circuits import CustomCircuit
f=np.array([5000.,10000.,20000.,50000.,100000.,200000.])
R0,R1,C1=100.,500.,1e-8
z=R0+R1/(1+1j*2*np.pi*f*R1*C1)
c=CustomCircuit('R0-p(R1,C1)',initial_guess=[90,450,1.2e-8])
c.fit(f,z)
r=c.predict(f)
assert np.allclose(c.parameters_,[R0,R1,C1],rtol=1e-4)
assert np.all(z.imag<0)
assert np.max(np.abs(r-z))<1e-3
print(json.dumps({'label':'SYNTHETIC NOT HARDWARE DATA','frequency_Hz':f.tolist(),'true_parameters':[R0,R1,C1],'fit_parameters':c.parameters_.tolist(),'max_complex_error_ohm':float(np.max(np.abs(r-z)))}))
