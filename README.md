## Installation
### Dependencies

This guide provides references to resources used to install the required dependencies across differenct projects.

1. [Install Docker Engine on Fedora](https://docs.docker.com/engine/install/fedora/)

    1.1  Uninstall old versions
    
    Older versions of Docker went by docker or docker-engine. Uninstall any such older versions before attempting to install a new version, along with associated dependencies.

    `sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-selinux docker-engine-selinux docker-engine `

    1.2 Install using the rpm repository

    Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.

    `sudo dnf -y install dnf-plugins-core`

    `sudo dnf-3 config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo`

    1.3 Install Docker Engine

    `sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

    1.4 Start Docker

    `sudo systemctl start docker`

    1.5 Verify Installation

    `sudo docker run hello-world`

2. [Install Nvidia Drivers](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation)





