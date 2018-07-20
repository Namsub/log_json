import pandas as pd
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

def write_to_excel(ops_list, memory_with_ops_list, mode, filename):
	writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')

	# metrics
	ops_list_wo_redundancy = eliminate_redundancy(ops_list)
	columns_format = ['ts', 'op_type', 'op', 'total_dur(μs)', 'allocated_memory', 'input_list', 'read_memory(MB)', 'write_memory(MB)', 'memory_usage(MB)', 'memory_bandwidth(GB/s)']
	ops_values = pd.DataFrame(ops_list_wo_redundancy, columns=columns_format)
	ops_values.to_excel(writer, sheet_name='metrics')

	# cpu/cpu_pool/cuda_host/gpu memory_usage
	memory_with_ops_list_wo_redundancy = eliminate_redundancy(memory_with_ops_list)
	columns_format = ['ts', 'cpu', 'cpu_pool', 'cuda_host', 'gpu', 'op']
	memory_values = pd.DataFrame(memory_with_ops_list_wo_redundancy, columns=columns_format)
	memory_values.to_excel(writer, sheet_name = 'memory_status_for_op')

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
