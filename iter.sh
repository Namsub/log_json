for i in `seq 2 5`
do
	for j in `seq 3 3`
	do
		python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/src_seq_diff_log/[$i-1]_32_de-en_trace_$j.json --output_dir=/home/titanxp/prac_nmt/nmt_data/sequence_length_diff_log/src_seq_diff_log/[$i-1]step_$j.xlsx
	done
done
