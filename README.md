# pgebaselinestudy

Load modeling is a complex task, with factors such as weather, time of year, location, purpose of building, and more. This study’s purpose is to use non-Demand-Response data from customers in order to find the most accurate method of predicting load behavior for Demand-Response days.

### HOW-TO
In global_vars, specify the INTERVALFLAG (0 = 15 minute intervals, 1 = 60 minute intervals), the PRINTFLAG (0 = Print only amount of SAIDs completed, 1 = Print SAID name, program, 2 = Print individual dates and all error rates), and the GRAPHFLAG (0 = No graph, 1 = All graphs for given time interval) (GRAPHFLAG = 1 will not store data, but only produce graphs). Also specify the SAID_LIMIT and SAID_OFFSET.

Run main.py to iterate through SAIDs and complete the calculations.

To select a random sample to average over, specify input_program, random_seed, and number in deliverable_create.py, then run it.

Have fun!
