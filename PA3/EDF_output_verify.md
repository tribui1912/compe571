EDF Schedule Verification

Input1.txt Verification (w1:520s, w2:220s, w3:500s, w4:200s, w5:300s)
Time 0-200 (First Period) ✓

t=0: w4 chosen (deadline 200) ✓
t=57: w2 chosen (deadline 220) ✓
t=97: w5 chosen (deadline 300) ✓
t=132: w3 chosen (deadline 500) ✓

Time 200-400 ✓

t=200: w4 new release (deadline 400) ✓
t=220: w2 new release (deadline 440) ✓
t=300: w5 new release (deadline 600) ✓

Task Completion Times ✓

w4: Completes before 200s, 400s, 600s, 800s
w2: Completes before 220s, 440s, 660s, 880s
w5: Completes before 300s, 600s, 900s
w3: Completes before 500s, 1000s
w1: Completes before 520s

Input2.txt Verification (w1:520s, w2:320s, w3:500s, w4:450s, w5:300s)
Time 0-300 (First Period) ✓

t=0: w5 chosen (deadline 300) ✓
t=35: w2 chosen (deadline 320) ✓
t=75: w4 chosen (deadline 450) ✓
t=132: w3 chosen (deadline 500) ✓
t=236: w1 chosen (deadline 520) ✓
t=289: IDLE (no ready tasks) ✓

Time 300-600 ✓

t=300: w5 new release (deadline 600) ✓
t=320: w2 new release (deadline 640) ✓
t=450: w4 new release (deadline 900) ✓
t=500: w3 new release (deadline 1000) ✓
t=520: w1 new release (deadline 1040) ✓

Task Completion Times ✓

w5: Completes before 300s, 600s, 900s
w2: Completes before 320s, 640s, 960s
w3: Completes before 500s, 1000s
w4: Completes before 450s, 900s
w1: Completes before 520s, 1040s
