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
def f0():
    # breakpoint()
    print(f"torch.cuda.device_count: {torch.cuda.device_count()}")
    print(f"CUDA_VISIBLE_DEVICES: {os.environ['CUDA_VISIBLE_DEVICES']}")
    return 0


@ray.remote(num_cpus=0, num_gpus=2)
def f1():
    # breakpoint()
    print(f"torch.cuda.device_count: {torch.cuda.device_count()}")
    print(f"CUDA_VISIBLE_DEVICES: {os.environ['CUDA_VISIBLE_DEVICES']}")
    return 1


pg = ray.util.placement_group([{"CPU": 0, "GPU": 4}])

r0 = f0.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(placement_group=pg)
).remote()


r1 = f1.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(placement_group=pg)
).remote()

print(ray.get([r1, r0]))
