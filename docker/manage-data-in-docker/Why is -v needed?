The -v parameter in Docker is primarily utilized to create a volume. It offers the potential to mirror and store directories within the Docker container. This Docker volume functionality can be understood from two perspectives:

First: {our_specific_directory}:{docker_directory} essentially links our local directory to a directory inside the Docker container. If we denote a local directory as /src:/tmp, it signifies that the local directory /src, containing requirements.txt and other files, will mirror to /tmp within the Docker container. An instance would be $(pwd):/src.

$(pwd): This points to the local directory. In the context of this CI/CD scenario, the content of the Django.nv directory will be read and transmitted to the Docker container.
/src: This represents a pathway inside the Docker container designated to house the contents of the Django.nv directory.
However, what is the role of the -v flag? The function within the Docker container operates correctly since Docker verifies and records the existence of the necessary files prior to the execution of the safety command or any other. (please see the 3rd image for reference) - The 4th image depicts our local setup. We encourage you to compare them for better comprehension.

Second: {created_volume}:{docker_directory} is predominantly for generating a volume managed by Docker. This proves useful in scenarios linked to the container (like updating or recreating it), where we intend to utilize the same contents or particular contentswhile crafting another container.

To offer a comparison, the first usage demonstrates a mutualistic symbiosis. Any local changes made will be acknowledged by the Docker container and subsequently applied to its own content, and vice versa.

However, the second usage exhibits a commensalistic symbiosis. This is because any Docker container modifications are stored in the Docker-created volume. However, we cannot directly update the content in the volume, unless it’s done from inside the Docker container.
