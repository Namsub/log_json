#for i in `seq 2 5`
#do
#	for j in `seq 3 3`
#	do
#		if [ $1 = "src" ]
#		then
#			python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/$1_seq_diff_log/[$i-1]_32_de-en_trace_$j.json --output_dir=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/$1_seq_diff_log/[$i-1]step_$j.xlsx
#		elif [ $1 = "tgt" ]
#		then
#			python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/$1_seq_diff_log/[1-$i]_32_de-en_trace_$j.json --output_dir=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/$1_seq_diff_log/[1-$i]step_$j.xlsx
#		fi
#
#	done
#done

python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/layer_diff_log/layer_$1_batch_32_de-en_trace_3.json --output_dir=/home/titanxp/prac_nmt/nmt_data/layer_diff_log/layer_$1_batch_32_step_3.xlsx
