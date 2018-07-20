#for i in 32 64 128
#do
#	r=${$i//[0-9]/}
#	if [ -z "$r" ] ; then
#		echo "$i is number."
#	else
#		echo "$i is not number."
#	fi
#done

#for i in 32 64 128
#do
#	for j in `seq 3 3`
#	do
#		python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/batch_diff_log/batch_diff_log_batch_$i_de-en_trace_$j.json --output_dir=/home/titanxp/prac_nmt/nmt_data/batch_diff_log/batch_$i_step_$j.xlsx
#	done
#done


## Batch iter
python parsing_trace_format.py --json_file=/home/titanxp/prac_nmt/nmt_data/batch_diff_log/batch_diff_log_batch_$1_de-en_trace_$2.json --output_dir=/home/titanxp/prac_nmt/nmt_data/batch_diff_log/batch_$1_step_$2.xlsx
