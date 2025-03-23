import os

import ray
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
import torch


# https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html


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
    print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES', 'NONE')}")
    dev = torch.device("cuda:0")
    torch.cuda.set_device(dev)
    print(dev)
    return 0


@ray.remote(num_cpus=0, num_gpus=2)
def f1():
    # breakpoint()
    print(f"torch.cuda.device_count: {torch.cuda.device_count()}")
    print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES', 'NONE')}")
    dev = torch.device("cuda:1")
    torch.cuda.set_device(dev)
    print(dev)
    return 1


pg = ray.util.placement_group([{"CPU": 0, "GPU": 2}])

r0 = f0.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(
        placement_group=pg,
        placement_group_bundle_index=0,
        placement_group_capture_child_tasks=True,
    )
).remote()


r1 = f1.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(
        placement_group=pg,
        placement_group_bundle_index=0,
        placement_group_capture_child_tasks=True,
    )
).remote()

print(ray.get([r0, r1]))
