

from subprocess import STDOUT, check_output, TimeoutExpired
import time
import statistics

from script_commons import *

timeout_in_seconds = 10

def get_tool_time(hsf, htf, num_tries, isPass):
    hsf_file = "{}.hsf".format(hsf)
    htf_file = "{}.htf".format(htf)
    #
    outwrap = None
    tries = []
    while len(tries) < num_tries:
        t_start = time.time()
        try:
            outwrap = check_output(["./ourtool.exe", "analyze", hsf_file, htf_file], stderr=STDOUT, timeout=timeout_in_seconds)
            tries.append(time.time() - t_start)
        except TimeoutExpired:
            return timeout_in_seconds
    t_total = statistics.mean(tries)
    #
    outwrap = str(outwrap)
    if "Pass" in outwrap:
        if isPass:
            return t_total
        else:
            raise Exception("Pass but expected Fail")
    elif "Fail" in outwrap:
        if isPass:
            raise Exception("Fail but expected Pass")
        else:
            return t_total
    elif "Inconc" in outwrap:
        raise Exception("Inconc ?")

def get_experiment_line(outer_loop_n,obs,isPass):
    htf = "mu_{}_{}".format(outer_loop_n,obs)
    if isPass == False:
        htf += "_fail"
    #
    line = "{},{},{}".format(outer_loop_n,obs,isPass)
    for hsf in hsfs:
        got_time = get_tool_time(hsf,htf,3,isPass)
        line += ",{}".format(got_time)
    return line

def experiment(csv_name):
    f = open("{}.csv".format(csv_name), "w")
    f.truncate(0)  # empty file
    f.write("outer_loop_n,obs,isPass,{}\n".format(",".join(hsfs)))
    f.flush()
    #
    for outer_loop_n in multitrace_outer_loop_ns:
        for obs in multi_trace_obs:
            line1 = get_experiment_line(outer_loop_n,obs,True)
            f.write("{}\n".format(line1))
            f.flush()
            line2 = get_experiment_line(outer_loop_n, obs, False)
            f.write("{}\n".format(line2))
            f.flush()

