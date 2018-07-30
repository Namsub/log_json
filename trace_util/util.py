import pandas as pd
import operator
import copy
from . import extract_layer_stat

def print_list(show_list):
	for val in show_list:
		print(val)

def eliminate_redundancy(ops_list):
	ops_list_wo_redundancy = []
	prev_ops = ops_list[0]
	ops_list_wo_redundancy.append(prev_ops)
	for cur_ops in ops_list:
		if prev_ops != cur_ops:
			ops_list_wo_redundancy.append(cur_ops)
			prev_ops = cur_ops
	
	return ops_list_wo_redundancy

def accumulate_ops(ops_list):
	temp_list = []
	prev_ops = ops_list[0]
	temp_list.append(prev_ops)
	for cur_ops in ops_list:
		if prev_ops != cur_ops:
			temp_list.append(cur_ops)
			prev_ops = cur_ops

	sorted_temp_list = sorted(temp_list, key=operator.itemgetter(2))	
	
	accumulated_ops_list = []
	prev_ops = sorted_temp_list[0]
	accumulated_ops_list.append(prev_ops)
	for cur_ops in sorted_temp_list:
		if prev_ops[2] != cur_ops[2]:
			accumulated_ops_list.append(prev_ops)
			prev_ops = cur_ops
		else:
			prev_ops[3] += cur_ops[3]	# dur
	
	sorted_with_ts_accumulated_ops_list = sorted(accumulated_ops_list, key=operator.itemgetter(0))

	del temp_list
	del sorted_temp_list
	del accumulated_ops_list

	return sorted_with_ts_accumulated_ops_list

def write_to_excel(ops_list, memory_with_ops_list, mode, filename):

	writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')

	## metrics
	print("write_to_excel")
	accumulated_ops_list = accumulate_ops(ops_list)
	columns_format = ['ts', 'op_type', 'op', 'total_dur(μs)', 'alloc_mem', 'req_mem', 'input_list', 'read_memory(MB)', 'write_memory(MB)', 'memory_usage(MB)', 'memory_bandwidth(GB/s)']
	ops_values = pd.DataFrame(accumulated_ops_list, columns=columns_format)
	ops_values.to_excel(writer, sheet_name='metrics')

	## cpu/cpu_pool/cuda_host/gpu memory_usage
	memory_with_ops_list_wo_redundancy = eliminate_redundancy(memory_with_ops_list)
	columns_format = ['ts', 'cpu', 'cpu_pool', 'cuda_host', 'gpu', 'op']
	memory_values = pd.DataFrame(memory_with_ops_list_wo_redundancy, columns=columns_format)
	memory_values.to_excel(writer, sheet_name = 'memory_status_for_op')

	## for CNN
	if mode == 'vgg':
		layer_stats_list = extract_layer_stat.vgg(ops_list)
		columns_format = ['layer', 'duration(ms)', 'memory_usage(MB)']
		layer_values = pd.DataFrame(layer_stats_list, columns=columns_format)
		layer_values.to_excel(writer, sheet_name = 'layer granularity')
	
	elif mode == 'resnet':
		block_stats_list, unit_stats_list = extract_layer_stat.resnet(ops_list)			
		columns_format = ['layer', 'duration(ms)', 'Req_memory(MB)', 'allocated_memory(MB)']
		block_values = pd.DataFrame(block_stats_list, columns=columns_format)
		block_values.to_excel(writer, sheet_name = 'block granularity')
		unit_values = pd.DataFrame(unit_stats_list, columns=columns_format)
		unit_values.to_excel(writer, sheet_name = 'unit granularity')

	writer.save()

#def plot_memory_usage(memory_with_ops_list):
