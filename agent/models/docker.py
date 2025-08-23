import docker


class Docker:
    """
    Docker class
    """

    def __init__(self):
        self._client = docker.from_env()

    def get_images(self):
        """
        Function to return all docker images running on host
        """
        image_objs = self._client.images.list()
        images = [image.attrs for image in self._client.images.list()]
        image_names = []
        for image in image_objs:
            for repo in image.attrs.get("RepoTags", []):
                image_names.append(repo)
        return images, image_names

    def get_volumes(self):
        """
        Function to return all docker volumes on host
        """
        return [volume.attrs for volume in self._client.volumes.list()]

    def get_networks(self):
        """
        Function to return all docker networks on host
        """
        return [network.attrs for network in self._client.networks.list()]

    def get_containers(self):
        """
        Function to return all docker containers running on host
        """
        containers = [
            container.attrs for container in self._client.containers.list(all=True)
        ]
        names = [container.get("Name", "") for container in containers]
        return containers, names

    def get_info(self):
        """
        Function to return basic docker information
        """
        return self._client.info()

    def get_data_usage(self):
        """
        Function to return data usage information of docker on host
        """
        return self._client.df()
