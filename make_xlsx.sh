prefix_path="/home/titanxp/prac_nmt/nmt_data/reproduce"

:<<'END'
### Var : tgt_max_len ###
folder_name="tgt_len"
path=$prefix_path'/'$folder_name

for i in `seq 2 5`
do
	#cp ${path}/batch_32_layer_2_unit_128_[1-${i}]_de-en_trace_3.json /home/titanxp/log_json/
	python parsing_trace_format.py --json_file=/home/titanxp/log_json/batch_32_layer_2_unit_128_[1-${i}]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_128_[1-${i}]_de-en_trace_3.xlsx
done
END

:<<'END'
### Var : Batch_size ###
folder_name="batch"
path=$prefix_path'/'$folder_name

for ((i=32;i<=128;i=i*2))
do
	#cp ${path}/batch_$i_layer_2_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/
	python parsing_trace_format.py --json_file=/home/titanxp/log_json/batch_${i}_layer_2_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_${i}_layer_2_unit_128_[1-1]_de-en_trace_3.xlsx
done
END

:<<'END'
### Var : num_layers ###
folder_name="temp_layer"
path=$prefix_path'/'$folder_name

for ((i=4;i<=8;i=i*2))
do
	#cp ${path}/batch_32_layer_${i}_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/
	python parsing_trace_format.py --json_file=/home/titanxp/log_json/batch_32_layer_${i}_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_${i}_unit_128_[1-1]_de-en_trace_3.xlsx
done
END

:<<'END'
### Var : num_units ###
folder_name="unit"
path=$prefix_path'/'$folder_name

for ((i=32;i<128;i=i*2))
do
	#cp ${path}/batch_32_layer_2_unit_${i}_[1-1]_de-en_trace_3.json /home/titanxp/log_json/
	python parsing_trace_format.py --json_file=/home/titanxp/log_json/batch_32_layer_2_unit_${i}_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_${i}_[1-1]_de-en_trace_3.xlsx
done
END

#:<<'END'
### Var : src_max_len ###
folder_name="src_len"
path=$prefix_path'/'$folder_name

for i in `seq 6 15`
do
	#cp ${path}/batch_32_layer_2_unit_128_[${i}-1]_de-en_trace_3.json /home/titanxp/log_json/
	python parsing_trace_format.py --json_file=/home/titanxp/log_json/batch_32_layer_2_unit_128_[${i}-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_128_[${i}-1]_de-en_trace_3.xlsx
done
#END
