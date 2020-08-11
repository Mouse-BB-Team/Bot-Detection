#from ml_models.light_ml_model import LightMlModel
#from utils.task_executor.task_executor import TaskExecutor
import tensorflow as tf


if __name__ == '__main__':
#    model = LightMlModel()
#    executor = TaskExecutor(model)
#    result = executor.start_execution(2)
#    print(result)
	devices = tf.config.experimental.list_physical_devices()
	print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
	
	for device in devices:
		print(device)

