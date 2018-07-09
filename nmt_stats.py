import argparse
import json
from collections import OrderedDict
import operator

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

# event descriptions
EV_NAME = 'name'
EV_CAT  = 'cat'
EV_PH   = 'ph'
EV_TS   = 'ts'
EV_DUR  = 'dur'
EV_TTS  = 'tts'
EV_PID  = 'pid'
EV_TID  = 'tid'
EV_ARGS = 'args'

# event type
EV_DURATION_BEGIN   = 'B'
EV_DURATION_END     = 'E'

EV_COMPLETE         = 'X'
EV_INSTANT          = 'I'
EV_COUNTER          = 'C'

EV_FLOW_EVENT_START = 's'
EV_FLOW_EVENT_STEP  = 't'
EV_FLOW_EVENT_END   = 'f'

EV_OBJECT_CREATED   = 'N'
EV_OBJECT_SNAPSHOT  = 'O'
EV_OBJECT_DESTROYED = 'D'

EV_METADATA         = 'M'

# event category
EV_CAT_TENSOR       = 'Tensor'
EV_CAT_OP           = 'Op'

# event metadata args
EV_META_DATA_NAME   = 'name'

# name
PROC_NAME = "process_name"

# args
EVENT_ARG_GPU_TENSORS          = "/job:localhost/replica:0/task:0/device:GPU:0 Tensors"
EVENT_ARG_SNAPSHOT             = 'snapshot'
EVENT_ARG_SNAPSHOT_TENSOR_DESC = 'tensor_description'
EVENT_ARG_GPU_ALL_COMPUTE      = "/device:GPU:0/stream:all Compute"
EVENT_ARG_NAME                 = 'name'
EVENT_ARG_OP                   = 'op'

# allocation description
ALLOC_DESC                     = 'allocation_description'
ALLOC_DESC_REQ_BYTES           = 'requested_bytes:'
ALLOC_DESC_ALLOC_BYTES         = 'allocated_bytes:'

# mega bytes
ONE_MEGA = 1024*1024

def extract_process_name(trace_line, proc_name, type):
    pid = -1

    for trace_ev in trace_line:
        if (trace_ev[EV_NAME] == proc_name and trace_ev[EV_PH] == EV_METADATA):
            args = trace_ev[EV_ARGS]
            # print(args)
            if args[EV_META_DATA_NAME] == type:
                pid = trace_ev[EV_PID]
                # print(pid)
    
    return pid

def show_memory_stats(trace_line, pid, requested_mem_str, allocated_mem_str):
    requested_mem_bytes = -1
    allocated_mem_bytes = -1

    mem_stats_list           = []
    mem_stats_list_exception = []

    for trace_ev in trace_line:
        if (trace_ev[EV_PID] == pid and trace_ev[EV_PH] == EV_OBJECT_SNAPSHOT and 
            trace_ev[EV_CAT] == EV_CAT_TENSOR):
            tensor_name = trace_ev[EV_NAME]
            args = trace_ev[EV_ARGS]

            snapshot_desc = args[EVENT_ARG_SNAPSHOT]
            tensor_desc = snapshot_desc[EVENT_ARG_SNAPSHOT_TENSOR_DESC]
            #print('>>>', tensor_name)
            #print(tensor_desc)

            # print(type(tensor_desc))
            if tensor_desc.find(ALLOC_DESC) > 0:
                tensor_desc_list = tensor_desc.split(' ')
                #print(tensor_desc_list)
                
                if (requested_mem_str in tensor_desc_list):
                    i = tensor_desc_list.index(requested_mem_str)
                    requested_mem_bytes = tensor_desc_list[i+1]
                else:
                    requested_mem_bytes = 0

                if (allocated_mem_str in tensor_desc_list):
                    i = tensor_desc_list.index(allocated_mem_str)
                    allocated_mem_bytes = tensor_desc_list[i+1]
                else:
                    allocated_mem_bytes = 0

                #print(requested_mem_bytes, allocated_mem_bytes)
                mem_stats_list.append((tensor_name, int(requested_mem_bytes), int(allocated_mem_bytes)))
            else:
                mem_stats_list.append((tensor_name, 0, 0))
                mem_stats_list_exception.append(tensor_name)
                #print(tensor_name)

    sorted_mem_stats_list = sorted(mem_stats_list, key=operator.itemgetter(2))
    sorted_mem_stats_list_exception = sorted(mem_stats_list_exception, key=operator.itemgetter(2))

    return sorted_mem_stats_list, sorted_mem_stats_list_exception

def show_list(list_item):
    for name, req_bytes, alloc_bytes in list_item:
        s = "{0:100s} {1:12d} {2:12d}".format(name, req_bytes, alloc_bytes)
        print(s)

def show_operation(trace_line, pid, mem_stats_list):
    ops_list = []
    mem_stats_dict = OrderedDict()
    for name, req_bytes, alloc_bytes in mem_stats_list:
        mem_stats_dict[name] = int(alloc_bytes)

    for trace_ev in trace_line:
        if (trace_ev[EV_PID] == pid and 
            trace_ev[EV_PH] == EV_COMPLETE and 
            trace_ev[EV_CAT] == EV_CAT_OP ):
            ts   = int(trace_ev[EV_TS])
            dur  = int(trace_ev[EV_DUR])

            args = trace_ev[EV_ARGS]
            name = args[EVENT_ARG_NAME]
            op   = args[EVENT_ARG_OP]

            alloc_bytes = mem_stats_dict[name]
            if (alloc_bytes < 0):
                alloc_bytes = 0 
            
            ops_list.append((op, name, ts, dur, alloc_bytes))
    
    return ops_list
    

def plot_mem_stats(mem_stats_list):
    tensor_names    = []
    req_mem_bytes   = []
    alloc_mem_bytes = []

    for name, req_bytes, alloc_bytes in mem_stats_list:
        tensor_names.append(name)
        req_mem_bytes.append(int(req_bytes/ONE_MEGA))
        alloc_mem_bytes.append(int(alloc_bytes/ONE_MEGA))
        #req_mem_bytes.append(req_bytes)
        #alloc_mem_bytes.append(alloc_bytes)

    print('req bytes', sum(req_mem_bytes))
    print('alloc bytes', sum(alloc_mem_bytes))
    print('diff', sum(alloc_mem_bytes) - sum(req_mem_bytes))

    plt.grid(True)
    plt.plot(req_mem_bytes, 'g-', alloc_mem_bytes, 'r-')

    #y_pos = np.arange(len(tensor_names))
    #plt.barh(y_pos, tensor_names, align='center', alpha = 0.5)
    #plt.yticks(y_pos, tensor_names)

    plt.show()


def main(tf):
    with open(tf, 'rt') as data_file:
        trace_data = json.load(data_file, object_pairs_hook=OrderedDict)
        trace_line = trace_data['traceEvents']
        # print(trace_line)

        pid_gpu_all_compute = extract_process_name(trace_line,PROC_NAME, EVENT_ARG_GPU_ALL_COMPUTE)
        #print('pid_gpu_all_compute=', pid_gpu_all_compute)
        pid_gpu_tensor = extract_process_name(trace_line,PROC_NAME, EVENT_ARG_GPU_TENSORS)
        #print('pid_gpu_tensor=', pid_gpu_tensor)
        mem_stats_list, mem_stats_list_exception = show_memory_stats(
                          trace_line, 
                          pid_gpu_tensor, 
                          requested_mem_str = ALLOC_DESC_REQ_BYTES, 
                          allocated_mem_str = ALLOC_DESC_ALLOC_BYTES)
        
        #show_list(mem_stats_list)
        #print('<<<<----------------------->>>>')
        #for name in mem_stats_list_exception:
        #    print(name)
        #plot_mem_stats(mem_stats_list)

        ops_list = show_operation(trace_line, pid_gpu_all_compute, mem_stats_list)
        #for op, name, ts, dur, alloc_bytes in ops_list:
        #    s = "{0:25s} {1:175s} {2:16d} {3:10d} {4:16d}".format(op,name,ts,dur, alloc_bytes)
        #    print(s)

        writer = pd.ExcelWriter('gpu_ops.xlsx', engine = 'xlsxwriter')
        columns_format = ['op', 'name', 'ts', 'dur', 'alloc_bytes']
        ops_values = pd.DataFrame(ops_list, columns=columns_format)
        ops_values.to_excel(writer, sheet_name='metrics')
        writer.save()



if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', 
        type=str, 
        help="trace file to be parsed")

    args = parser.parse_args()
    # print(args.json_file)
    main(args.json_file)
