


import random
import copy

from script_commons import *

def make_multitrace(outer_loop_n):
    multi_trace = {}
    for key in sensor_example_lifelines:
        multi_trace[key] = []
    #
    while outer_loop_n > 0:
        multi_trace["CSI"] = multi_trace["CSI"] + ["CSI!ce"]
        multi_trace["CI"] = multi_trace["CI"] + ["CI?ce.CI!cmi"]
        multi_trace["SM"] = multi_trace["SM"] + ["SM?cmi.SM!rlsoc"]
        multi_trace["SOS"] = multi_trace["SOS"] + ["SOS?rlsoc.SOS!lsoc"]
        multi_trace["SM"] = multi_trace["SM"] + ["SM?lsoc"]
        # the par
        multi_trace["LSM"] = multi_trace["LSM"] + ["LSM?rbm.LSM!bm"]
        multi_trace["CSM"] = multi_trace["CSM"] + ["CSM?rcm.CSM!cm"]
        ## choices for interleaving
        interleav_1 = ["SM!rbm","SM?bm"]
        interleav_2 = ["SM!rcm","SM?cm"]
        interleaved = [x.pop(0) for x in random.sample([interleav_1]*len(interleav_1) + [interleav_2]*len(interleav_2), len(interleav_1)+len(interleav_2))]
        multi_trace["SM"] = multi_trace["SM"] + interleaved
        #
        multi_trace["SM"] = multi_trace["SM"] + ["SM!cm"]
        multi_trace["CSI"] = multi_trace["CSI"] + ["CSI?cm"]
        #
        inner_loop_n = random.randint(0,4)
        while inner_loop_n > 0:
            multi_trace["CA"] = multi_trace["CA"] + ["CA!tdc"]
            multi_trace["CR"] = multi_trace["CR"] + ["CR?tdc.CR!tmu"]
            multi_trace["CSM"] = multi_trace["CSM"] + ["CSM?tmu.CSM!ucm"]
            multi_trace["SM"] = multi_trace["SM"] + ["SM?ucm.SM!ucm"]
            multi_trace["CSI"] = multi_trace["CSI"] + ["CSI?ucm"]
            inner_loop_n -= 1
        outer_loop_n -= 1
    return multi_trace

def print_multi_trace(name,multi_trace):
    f = open("{}.htf".format(name), "w")
    f.truncate(0)  # empty file
    f.write("{\n")
    f.flush()
    for lf_name in sensor_example_lifelines:
        f.write("[{}] {}".format(lf_name, ".".join(multi_trace[lf_name])))
        if lf_name != sensor_example_lifelines[-1]:
            f.write(";\n")
        else:
            f.write("\n}\n")
        f.flush()

def multi_trace_length(mu):
    return sum( [len(x) for _,x in mu.items()] )

def cut_end_multi_trace(mu,goal_length):
    if multi_trace_length(mu) <= goal_length:
        return mu
    else:
        keys = [key for key,trace in mu.items() if len(trace) > 0]
        got_key = random.choice(keys)
        mu[got_key] = mu[got_key][:-1]
        return cut_end_multi_trace(mu,goal_length)

def add_err_at_end(mu):
    got_key = random.choice(sensor_example_lifelines)
    mu[got_key] += ["{}!err".format(got_key)]
    return mu

def generate():
    random.seed(10)
    #
    for outer_loop_n in multitrace_outer_loop_ns:
        mu = make_multitrace(outer_loop_n)
        length = multi_trace_length(mu)
        for obs in multi_trace_obs:
            goal_length = int( length*(obs/100) )
            got_mu = cut_end_multi_trace(copy.deepcopy(mu),goal_length)
            print_multi_trace("mu_{}_{}".format(outer_loop_n,obs), got_mu)
            fail_mu = add_err_at_end(got_mu)
            print_multi_trace("mu_{}_{}_fail".format(outer_loop_n,obs), fail_mu)

