#
# Bayesian Optimization of Combinatorial Structures
#
# Copyright (C) 2018 R. Baptista & M. Poloczek
# 
# BOCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BOCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with BOCS.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2018 MIT & University of Arizona
# Authors: Ricardo Baptista & Matthias Poloczek
# E-mails: rsb@mit.edu & poloczek@email.arizona.edu
#

import numpy as np
import matplotlib.pyplot as plt
from BOCS import BOCS
from quad_mat import quad_mat
from sample_models import sample_models
import subprocess
import csv

FLAGS = [ '-fbranch-probabilities', '-fprofile-values', '-fvpt', '-fbranch-target-load-optimize', '-fbranch-target-load-optimize2', '-fcaller-saves', '-fcprop-registers', '-fcse-follow-jumps', '-fcse-skip-blocks', '-fdata-sections', '-fdelayed-branch', '-fdelete-null-pointer-checks', '-fexpensive-optimizations', '-ffast-math', '-ffloat-store', '-fforce-addr', '-fforce-mem', '-ffunction-sections', '-fgcse', '-fgcse-lm', '-fgcse-sm', '-fgcse-las', '-floop-optimize', '-fcrossjumping', '-fif-conversion', '-fif-conversion2', '-finline-functions', '-fkeep-inline-functions', '-fkeep-static-consts', '-fmerge-constants', '-fmerge-all-constants', '-fmove-all-movables', '-fnew-ra', '-fno-branch-count-reg', '-fno-default-inline', '-fno-defer-pop', '-fno-function-cse', '-fno-guess-branch-probability', '-fno-inline', '-fno-math-errno', '-fno-peephole', '-fno-peephole2', '-funsafe-math-optimizations', '-ffinite-math-only', '-fno-trapping-math', '-fno-zero-initialized-in-bss', '-fomit-frame-pointer', '-foptimize-register-move', '-foptimize-sibling-calls', '-fprefetch-loop-arrays', '-fprofile-generate', '-fprofile-use', '-freduce-all-givs', '-fregmove', '-frename-registers', '-freorder-blocks', '-freorder-functions', '-frerun-cse-after-loop', '-frerun-loop-opt', '-frounding-math', '-fschedule-insns', '-fschedule-insns2', '-fno-sched-interblock', '-fno-sched-spec', '-fsched-spec-load', '-fsched-spec-load-dangerous', '-fsched2-use-superblocks', '-fsched2-use-traces', '-fsignaling-nans', '-fsingle-precision-constant', '-fstrength-reduce', '-fstrict-aliasing', '-ftracer', '-fthread-jumps', '-funroll-all-loops', '-funroll-loops', '-fpeel-loops', '-funswitch-loops', '-fold-unroll-loops', '-fold-unroll-all-loops']

def read_output():
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        s = 0
        for row in csv_reader:
            s = s + float(row[1])
        return s/3

def run(flags):
    try:
        subprocess.run(['./test.sh', ' '.join(flags)])
        return read_output()
    except:
        return 0

def model(x):
    flags = []
    if x.shape[0] == 1:
        x = x.reshape(x.shape[1])
    for i in range(len(x)):
        if int(x[i]) != 0:
            flags.append(FLAGS[i])
    return run(flags)

# Save inputs in dictionary
inputs = {}
inputs['n_vars']     = 10
inputs['evalBudget'] = 5
inputs['n_init']     = 1
inputs['lambda']     = 1e-4

# Save objective function and regularization term
# Q = quad_mat(inputs['n_vars'], 10)
inputs['model']    = lambda x: model(x)
inputs['penalty']  = lambda x: inputs['lambda']*np.sum(x,axis=1)

# Generate initial samples for statistical models
inputs['x_vals']   = sample_models(inputs['n_init'], inputs['n_vars'])
# inputs['y_vals']   = inputs['model'](inputs['x_vals'])
y_vals = []
for row in inputs['x_vals']:
    y = model(row)
    y_vals.append(y)
inputs['y_vals'] = np.asarray(y_vals)    


# Run BOCS-SA and BOCS-SDP (order 2)
(BOCS_SA_model, BOCS_SA_obj)   = BOCS(inputs.copy(), 2, 'SA')

# Compute optimal value found by BOCS
iter_t = np.arange(BOCS_SA_obj.size)
BOCS_SA_opt = np.minimum.accumulate(BOCS_SA_obj)
# BOCS_SDP_opt = np.minimum.accumulate(BOCS_SDP_obj) 



# # Compute minimum of objective function
# n_models = 2**inputs['n_vars']
# x_vals = np.zeros((n_models, inputs['n_vars']))
# str_format = '{0:0' + str(inputs['n_vars']) + 'b}'
# for i in range(n_models):
# 	model = str_format.format(i)
# 	x_vals[i,:] = np.array([int(b) for b in model])
# f_vals = inputs['model'](x_vals) + inputs['penalty'](x_vals)
# opt_f  = np.min(f_vals)

# Plot results
fig = plt.figure()
ax  = fig.add_subplot(1,1,1)
ax.plot(iter_t, np.abs(BOCS_SA_opt), color='r', label='BOCS-SA')
ax.set_yscale('log')
ax.set_xlabel('$t$')
ax.set_ylabel('Best $\log$ write speed')
ax.legend()
fig.savefig('BOCS_simpleregret.pdf')
plt.close(fig)

# -- END OF FILE --
