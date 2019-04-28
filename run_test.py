import subprocess
import csv
import numpy as np

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
    for i in range(len(x)):
        if x[i] != 0:
            flags.append(FLAGS[i])
    return run(flags)
    
