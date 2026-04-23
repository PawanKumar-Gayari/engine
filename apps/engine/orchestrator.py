from .state_manager import PipelineState
from .pipeline import Pipeline


def run_pipeline(keyword):

    state = PipelineState(keyword)

    pipeline = Pipeline(state)
    result = pipeline.run()

    return result