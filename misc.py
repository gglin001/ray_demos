import ray


def is_initialized():
    print(f"ray.is_initialized(): {ray.is_initialized()}")


def get_num_gpus():
    num_gpus = ray.cluster_resources().get("GPU")
    print(f"num_gpus: {num_gpus}")


if __name__ == "__main__":
    is_initialized()
    get_num_gpus()
