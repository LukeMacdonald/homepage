from kubernetes import client, config

config.load_kube_config()

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
batch_v1 = client.BatchV1Api()
networking_v1 = client.NetworkingV1Api()


def get_resources(namespace):
    resources = {}
    pods = core_v1.list_namespaced_pod(namespace=namespace)
    resources["pods"] = []
    for pod in pods.items:
        resources["pods"].append(pod.metadata.name)

    # Services
    resources["services"] = []
    services = core_v1.list_namespaced_service(namespace=namespace)
    for svc in services.items:
        resources["services"].append(svc.metadata.name)

    # Deployments
    deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
    resources["deployments"] = []
    for deploy in deployments.items:
        resources["deployments"].append(deploy.metadata.name)

    # Jobs
    jobs = batch_v1.list_namespaced_job(namespace=namespace)
    resources["jobs"] = []
    for job in jobs.items:
        resources["jobs"].append(job.metadata.name)

    # Ingress
    ingresses = networking_v1.list_namespaced_ingress(namespace=namespace)
    resources["ingress"] = []
    for ing in ingresses.items:
        resources["ingress"].append(ing.metadata.name)
    return resources


def get_all():
    namespaces = core_v1.list_namespace()
    resources = {}
    for ns in namespaces.items:
        resources[ns.metadata.name] = get_resources(ns.metadata.name)
    return resources
