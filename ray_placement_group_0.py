import os

import ray
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
import torch

ray.init(
    runtime_env={
        "env_vars": {
            "RAY_DEBUG_POST_MORTEM": "1",
            "RAY_DEBUG": "1",
        },
    },
)


@ray.remote(num_cpus=0, num_gpus=2)
def f():
    # breakpoint()
    print(f"torch.cuda.device_count: {torch.cuda.device_count()}")
    print(f"CUDA_VISIBLE_DEVICES: {os.environ['CUDA_VISIBLE_DEVICES']}")
    return 0


pg = ray.util.placement_group([{"CPU": 0, "GPU": 2}])

ret = ray.get(
    f.options(
        scheduling_strategy=PlacementGroupSchedulingStrategy(placement_group=pg)
    ).remote()
)
