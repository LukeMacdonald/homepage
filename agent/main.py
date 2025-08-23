from fastapi import FastAPI
from vm import Virtual_Machine

app = FastAPI()


@app.get("/")
def read_root():
    vm = Virtual_Machine()
    payload = {
        "Host": vm.name,
        "CPU": vm.get_cpu(),
        "RAM": vm.get_ram(),
        "Disk": vm.get_disk_usage(),
        "Nginx": vm.get_nginx_info(),
        "Services Running": {
            "Kubernetes": vm.is_kubernetes_running(),
            "Docker": vm.is_docker_running(),
            "Apache": vm.is_apache_running(),
            "Nginx": vm.is_nginx_running(),
        },
    }
    if vm.is_docker_running():
        payload["Docker"] = vm.get_docker_info()
    if vm.is_kubernetes_running():
        payload["Kubernetes"] = vm.get_kube_info()
    return payload
