import concurrent.futures
# import src.ml_moodel as model
import src.ml_model_mock as model
from typing import List
import logging.config
from pathlib import Path
import os

logger_config_path = Path(__file__).parent.joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class TaskExecutor:
    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

    def start_execution(self, number_of_task_to_run):
        final_results = []
        ml_model = model.MlModelMock()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures_map = {
                executor.submit(self.run_single_task, ml_model, task_id): f"task_{task_id}"
                for task_id in range(number_of_task_to_run)
            }

            for future in concurrent.futures.as_completed(futures_map):
                try:
                    final_results.append(future.result())
                except Exception as e:
                    self.__logger.error("Error while evaluating %s: %s", futures_map[future], e)

        return final_results

    def run_single_task(self, model, task_id):
        self.__logger.info("Running %d...", task_id)
        # os.system()
        execution_result = model.run()
        return execution_result

    def calculate_execution_statistics(self, execution_results: List):
        # TODO: [BD-89] Create script for collecting results and statistics
        for result in execution_results:
            self.__logger.info("%s", result)
        pass


if __name__ == '__main__':
    task_executor = TaskExecutor()
    exec_results = task_executor.start_execution(5)
    task_executor.calculate_execution_statistics(exec_results)
