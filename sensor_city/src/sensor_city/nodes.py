from . import worker_node

def start_worker_node():
    worker_node.WorkerNode().spin()
