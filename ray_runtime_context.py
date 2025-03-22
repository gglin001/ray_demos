import os

import ray
import ray.runtime_context
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

    runtime_context: ray.runtime_context.RuntimeContext = ray.get_runtime_context()
    job_id = runtime_context.get_job_id()
    node_id = runtime_context.get_node_id()
    worker_id = runtime_context.get_worker_id()
    task_name = runtime_context.get_task_name()
    runtime_env_string = runtime_context.get_runtime_env_string()
    resource_ids = runtime_context.get_resource_ids()
    accelerator_ids = runtime_context.get_accelerator_ids()
    gpu_ids = runtime_context.get_accelerator_ids()["GPU"]
    print(f"job_id: {job_id}")
    print(f"node_id: {node_id}")
    print(f"worker_id: {worker_id}")
    print(f"task_name: {task_name}")
    print(f"runtime_env_string: {runtime_env_string}")
    print(f"resource_ids: {resource_ids}")
    print(f"accelerator_ids: {accelerator_ids}")
    print(f"gpu_ids: {gpu_ids}")
    return 0


pg = ray.util.placement_group(
    [
        {"CPU": 0, "GPU": 4},
        {"CPU": 0, "GPU": 4},
    ]
)

r0 = f0.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(
        placement_group=pg,
        placement_group_bundle_index=1,
        placement_group_capture_child_tasks=True,
    )
).remote()


print(ray.get([r0]))
