prefix_path="/home/titanxp/prac_nmt/nmt_data/reproduce"

:<<'END'
### Var : tgt_max_len ###
folder_name="tgt_len"
path=$prefix_path'/'$folder_name

for i in `seq 1 5`
do
	python parsing_trace_format.py --json_file=${path}/batch_64_layer_2_unit_128_[1-$i]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_64_layer_2_unit_128_[1-$i]_de-en_trace_3.xlsx
	cp ${path}/batch_64_layer_2_unit_128_[1-$i]_de-en_trace_3.json /home/titanxp/log_json/
done
END

### Var : src_max_len ###
folder_name="src_len"
path=$prefix_path'/'$folder_name

for i in `seq 2 5`
do
	python parsing_trace_format.py --json_file=${path}/batch_32_layer_2_unit_128_[$i-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_128_[$i-1]_de-en_trace_3.xlsx
	cp ${path}/batch_32_layer_2_unit_128_[$i-1]_de-en_trace_3.json /home/titanxp/log_json/
done

#:<<'END'
### Var : Batch_size ###
folder_name="batch"
path=$prefix_path'/'$folder_name

python parsing_trace_format.py --json_file=${path}/batch_64_layer_2_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_64_layer_2_unit_128_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_64_layer_2_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/

python parsing_trace_format.py --json_file=${path}/batch_128_layer_2_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_128_layer_2_unit_128_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_128_layer_2_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/

### Var : num_layers ###
folder_name="layer"
path=$prefix_path'/'$folder_name

python parsing_trace_format.py --json_file=${path}/batch_32_layer_4_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_4_unit_128_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_32_layer_4_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/

python parsing_trace_format.py --json_file=${path}/batch_32_layer_8_unit_128_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_8_unit_128_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_32_layer_8_unit_128_[1-1]_de-en_trace_3.json /home/titanxp/log_json/

### Var : num_units ###
folder_name="unit"
path=$prefix_path'/'$folder_name

python parsing_trace_format.py --json_file=${path}/batch_32_layer_2_unit_32_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_32_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_32_layer_2_unit_32_[1-1]_de-en_trace_3.json /home/titanxp/log_json/

python parsing_trace_format.py --json_file=${path}/batch_32_layer_2_unit_64_[1-1]_de-en_trace_3.json --output_dir=/home/titanxp/log_json/batch_32_layer_2_unit_64_[1-1]_de-en_trace_3.xlsx
cp ${path}/batch_32_layer_2_unit_64_[1-1]_de-en_trace_3.json /home/titanxp/log_json/
#END
