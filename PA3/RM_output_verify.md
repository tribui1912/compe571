Rate Monotonic Schedule Verification
Input1.txt Analysis
Periods (Priority: Highest → Lowest):

w4: 200s (highest)
w2: 220s
w5: 300s
w3: 500s
w1: 520s (lowest)

Schedule Verification

Initial Order (0-200s) ✓

t=0: w4 runs (highest priority) ✓
t=57: w2 runs (2nd priority) ✓
t=97: w5 runs (3rd priority) ✓
t=132: w3 runs (4th priority) ✓


Key Release Points ✓

t=200: w4 preempts (highest priority) ✓
t=220: w2 gets CPU after w4 ✓
t=300: w5 runs at its period ✓
t=400: w4 preempts again ✓
t=500: w3 gets CPU after higher priorities ✓


Idle Periods (7.90%) ✓

t=789-800
t=857-880
t=955-1000



Input2.txt Analysis
Periods (Priority: Highest → Lowest):

w5: 300s (highest)
w2: 320s
w4: 450s
w3: 500s
w1: 520s (lowest)

Schedule Verification

Initial Order (0-300s) ✓

t=0: w5 runs (highest priority) ✓
t=35: w2 runs (2nd priority) ✓
t=75: w4 runs (3rd priority) ✓
t=132: w3 runs (4th priority) ✓
t=236: w1 runs (lowest priority) ✓


Key Release Points ✓

t=300: w5 preempts (highest priority) ✓
t=320: w2 runs after w5 ✓
t=450: w4 gets CPU ✓
t=500: w3 runs ✓


Idle Periods (24.70%) ✓

t=289-300
t=375-450
t=739-900