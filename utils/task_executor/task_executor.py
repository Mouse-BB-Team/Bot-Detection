import concurrent.futures
import logging.config
from pathlib import Path

logger_config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class TaskExecutor:
    def __init__(self, ml_model):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.ml_model = ml_model

    def start_execution(self, number_of_task_to_run=30):
        if number_of_task_to_run <= 0:
            msg = "Illegal argument. Number of task to run has to be grater than 0"
            self.__logger.error(msg)
            raise ValueError(msg)

        final_results = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures_map = {
                executor.submit(self._run_single_task, self.ml_model, task_id): f"task_{task_id}"
                for task_id in range(number_of_task_to_run)
            }

            for future in concurrent.futures.as_completed(futures_map.keys()):
                try:
                    future_result = future.result()
                    final_results.append(future_result)
                except Exception as e:
                    self.__logger.error("Error while evaluating %s: %s", futures_map[future], e)
                    raise e

        return final_results

    def _run_single_task(self, model, task_id):
        self.__logger.info("Running task id %d...", task_id)
        execution_result = model.run()
        return execution_result
