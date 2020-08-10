from ml_models.light_ml_model import LightMlModel
from utils.task_executor.task_executor import TaskExecutor

if __name__ == '__main__':
    model = LightMlModel()
    executor = TaskExecutor(model)
    result = executor.start_execution(2)
    print(result)
