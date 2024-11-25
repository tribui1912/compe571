# To run the program, use the following command:
```
python3 scheduler.py <input> <policy> <energy_efficient>
```
Policy can be RM or EDF.
Energy efficient can be EE or not EE (leave blank for no EE).

# For input should be in format:
```
First row: <# of tasks> < the time the system will execute up to in seconds> <active CPU power @ 1188 Mhz> <active CPU power @ 918 Mhz> <active CPU power @ 648Mhz> <active CPU power @ 384 Mhz> <idle CPU power @ lowest frequency>
All other rows: <name of task> <deadline/period> <WCET @ 1188 Mhz> <WCET @ 918 Mhz> <WCET @ 648 Mhz> <WCET @ 384 Mhz>
```

# Output Explained:
```
Schedule:
<time> <task> <frequency> <duration> <energy>
0 w5 384 104 22.048J    # time=0, task=w5, freq=384MHz, runs for 104s
...

Total Energy Consumption: 288.175J
Percentage of time spent idle: 4.40%
Frequency Distribution:
1188: 124s (12.40%)
...
```

