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





3. [Install Neo4j Using Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/)

    3.1 **Getting the Neo4j image**

    [https://hub.docker.com/_/neo4j](https://hub.docker.com/_/neo4j)

    3.2 **Using the Neo4j Docker image**
    
    You can start a Neo4j container by using the following command. Note that this Neo4j container will not persist data between restarts and will have the default username/password.

    `docker run --restart always --publish=7474:7474 --publish=7687:7687 neo4j:5.26.0`

    3.3 **Persisting data between restarts**

    The --volume option maps a local folder to the container, where you can persist data between restarts. To persist the contents of the database between containers, mount a volume to the /data directory on starting the container:

    `docker run --restart always --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=neo4j/your_password --volume=/path/to/your/data:/data neo4j:5.26.0`

    3.4 **Using NEO4J_AUTH to set an initial password**

    When using Neo4j in a Docker container, you can set the initial password for the database directly by specifying the NEO4J_AUTH in your run directive:

    `docker run --restart always --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=neo4j/your_password neo4j:5.26.0`

    Alternatively, you can disable authentication by specifying NEO4J_AUTH to none:

    `docker run --restart always --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=none neo4j:5.26.0`

4. [Setup Ollama Docker](https://hub.docker.com/r/ollama/ollama)