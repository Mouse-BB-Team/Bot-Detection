import pytest
from utils.task_executor.task_executor import TaskExecutor
from utils.task_executor.__tests__.mocks.ml_model_mock import MlModelMock, ExceptionModelMock


@pytest.mark.parametrize('arg', [0, -1])
def test_should_raise_value_error_when_illegal_argument(arg):
    model = MlModelMock()
    executor = TaskExecutor(model)
    with pytest.raises(ValueError):
        assert executor.start_execution(number_of_task_to_run=arg)


def test_should_execute_and_return_list():
    model = MlModelMock()
    executor = TaskExecutor(model)
    result = executor.start_execution()
    assert isinstance(result, list)


def test_should_execute_with_default_argument():
    model = MlModelMock()
    executor = TaskExecutor(model)
    result = executor.start_execution()
    assert len(result) == 30
