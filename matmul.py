import tensorflow as tf
from tensorflow.python.client import timeline

with tf.device('/cpu:0'):
	x = tf.constant([[1.0, 2.0, 3.0]])
	w = tf.constant([[2.0], [2.0], [2.0]])
with tf.device('/gpu:0'):
	y = tf.matmul(x, w)

print(x.get_shape())

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()

sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
init = tf.global_variables_initializer()
sess.run(init, options=run_options, run_metadata=run_metadata)
result = sess.run(y, options=run_options, run_metadata=run_metadata)
print(result)

tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)

with open("./temp.json", 'w') as f:
	f.write(ctf)
