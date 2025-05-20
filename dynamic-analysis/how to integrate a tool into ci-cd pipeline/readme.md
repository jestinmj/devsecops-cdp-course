# How To Integrate a Tool Into a CI/CD Pipeline

In this scenario, you will learn how to integrate a tool into a CI/CD pipeline.

The information taught in this exercise is essential for all our courses.

#  How To Integrate a Tool Into a CI/CD Pipeline
--------------------------------
# Getting Started

This exercise is designed to help you gain proficiency in configuring volumes when running security tools in a CI/CD pipeline. It focuses on two diverse tools: ZAP (Zed Attack Proxy) and hysnsec/safety.

Additionally, you will understand how to test these tools locally and integrate them into your CI/CD pipeline effectively. By the end of this exercise, you should be able to configure the tools, perform local testing, and prepare for future pipeline integration.

After completing this exercise, you will have:
- Gathered information about ZAP and hysnsec/safety from documentation
- Understood volume configuration requirements
- Tested ZAP and hysnsec/safety locally with volume configurations
- Prepared for CI/CD pipeline integration
Let’s move to the next step.

# Testing and Integrating ZAP into Your CI/CD Pipeline
--------------------------------
# Getting Started

## Exploring the Documentation
To begin, start by conducting a thorough internet search for the tool you want to use. Look for the [official website](https://www.zaproxy.org/docs/docker/baseline-scan/) or relevant documentation that provides information about the tool’s functionality, requirements, and configuration options.
![image](https://github.com/user-attachments/assets/b74841f2-eb8a-4554-871d-c90d51dedf75)

## Understanding Volume Configuration
Once you have accessed the official website or documentation, take the time to carefully read through the provided information. Look for any specific mentions of volumes, as these indications will be crucial for configuring the tool correctly.
![image](https://github.com/user-attachments/assets/c1bab472-1f9a-4705-943d-433742e3ea33)

## Discovering ZAP’s Help Command Options
For a deeper understanding of ZAP’s capabilities and volume options available, input the help command pertaining to ZAP in your terminal. The help command elucidates a list of available options, which includes specific arguments or flags related to volumes.
![image](https://github.com/user-attachments/assets/f8cf7a25-af80-43f2-a6be-f56197150764)

## Exploring ZAP on Docker Hub
Docker Hub is a vast resource for finding pre-built Docker containers. Visit [Docker Hub](https://hub.docker.com/search?q=zap) and conduct a search for ZAP. Explore the search results to locate the official Docker container for the tool, and take note of the container’s name and version.
![image](https://github.com/user-attachments/assets/fc386223-6fd0-4e04-9f72-4e1569766649)

We started by searching for ZAP (Zed Attack Proxy) documentation online. This helped us understand how to use the tool and set up its volumes. We then explored ZAP’s commands and found its official Docker container.

## Local Testing
Before integrating a tool into CI/CD, test it locally to experiment with its options and configurations.

Let’s start by pulling the ZAP image in our DevSecOps-Box machine (terminal).<br>
`docker pull ghcr.io/zaproxy/zaproxy:stable`
<br>
> Note:
> Docker is already installed on the DevSecOps-Box machine, if you are using your own machine, ensure Docker is installed on your local machine.

To run the ZAP image, we execute a specific script called zap-baseline.py within the container. The final command would look as follows:<br>
`docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html`
```
--snip--
2025-05-20 06:30:19,527 Unable to copy yaml file to /zap/wrk/zap.yaml [Errno 13] Permission denied: '/zap/wrk/zap.yaml'
--snip--
```

If you wondering why we are using /zap/wrk/ as the volume, it is because ZAP expects the wrk directory to be present in the container and the testreport.html file to be present in the wrk directory.

`docker run --user $(id -u):$(id -g) -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html`
> GHCR stands for GitHub Container Registry. More information about GHCR can be found at the following link: [https://www.zaproxy.org/docs/docker/about/](https://www.zaproxy.org/docs/docker/about/)

Note that the –user $(id -u):$(id -g) option sets the user and group IDs inside the container to match those of the user running the command on the host. This helps prevent potential permission issues when writing files to mounted volumes.

> Why do we use zap-baseline.py?
> ZAP have two types of scans:
> - Active Scan: This type of scan actively attacks the target and is not suitable for learning purposes also takes a long time to complete.
> - Baseline Scan: This type of scan is passive and does not actively attack the target. It is suitable for learning purposes and takes a short time to complete.
> Running Baseline Scan is the best option to use for short term testing especially in CI/CD pipelines as we don’t want it running for a long time and blocking the pipeline.

References: https://www.zaproxy.org/docs/docker/baseline-scan/
![image](https://github.com/user-attachments/assets/df0fd00d-0343-4916-b4b1-54bf80675b56)

## Integrating ZAP into Your CI/CD Pipeline
If ZAP meets your requirements and functions as anticipated, you’ll be ready to incorporate it into your CI/CD pipeline. The following steps will come in handy:
1. Identify the volume configurations required by ZAP using the documentation and other resources.
2. Add these volume configurations to your pipeline to ensure ZAP has access to necessary data and storage.
3. In future exercises, you’ll learn to test ZAP in your pipeline to verify volume configurations and data handling in the DAST (Dynamic Analysis) chapter.
Let’s move to the next step.


# Testing and Integrating safety into Your CI/CD Pipeline
--------------------------------
We are going to use hysnsec/safety tool in this exercise, that created by Practical DevSecOps team and functionally remains the same as safety.

## Understanding the Tool
## Exploring the Documentation
As usual, we will start by searching for the tool’s documentation. In this case, the custom tool, hysnsec/safety. Browse through [Docker Hub](https://hub.docker.com/search?q=hysnsec%2Fsafety) page or any relevant documentation to collect information about the tool’s functionality, requirements, and configuration options.

![image](https://github.com/user-attachments/assets/5045ea95-ac0b-47ac-bdb2-496195db2c4e)

## Understanding Volume Configuration
Review hysnsec/safety’s Docker Hub documentation, paying special attention to volume configuration requirements.
![image](https://github.com/user-attachments/assets/ff54e21e-e3b8-4503-abd8-396a91e3e6af)

## Local Testing using Docker
Lets do the same thing we did for ZAP.<br>
`docker pull hysnsec/safety`

Before running the tool, we need to have a source code to scan.<br>
`git clone https://gitlab.practical-devsecops.training/pdso/django.nv.git`

And then move to the source code directory.<br>
`cd django.nv`

Next, we will run the tool.
`docker run --rm -v $(pwd):/src hysnsec/safety check`

This command starts an instance of the Docker container running hysnsec/safety. The –rm option tells Docker to automatically remove the container after it finishes running. The -v $(pwd):/src part mounts your current directory on your computer to the /src directory inside the container.
This command runs the hysnsec/safety Docker container, automatically cleans it up after it exits, and mounts the current directory to /src in the container.

As you can see, the tool is running and scanning the source code but why the tool is able to scan the source code?

In some tools, you need to specify the source code directory to scan. But in hysnsec/safety, it will scan /src directory by default hence we don’t need to specify the source code directory as we already mounted the current directory to /src in the container.

Now, if you want to save the output data from hysnsec/safety for further analysis or reporting, you can append an output redirection operator (>) at the end of the command followed by the output file’s name. The expanded command looks like this:
```
docker run --rm -v $(pwd):/src hysnsec/safety check --json > testreport.json
```
The --json flag outputs the results in JSON format and saves them to testreport.json. Since we mounted the current directory to /src, this file persists on your host machine even after the container stops running. This makes it easy to analyze the results later or use them in your pipeline.
![image](https://github.com/user-attachments/assets/4f7b07a7-86e4-4c62-91ea-ec91e123db56)

## Integrating safety into Your CI/CD Pipeline
If hysnsec/safety works well for you, you can add it to your DevSecOps pipeline by following these steps:

- Find out what volume configurations hysnsec/safety needs. You will learn how to do this in the next exercises by using the documentation and other resources.
- Add the correct volume configurations to your pipeline so that hysnsec/safety’s containers have the data and storage they need.
- In the next sections, we will explore tool integrations in the SCA (Software Composition Analysis) chapter. You will learn how to test the tool in your pipeline to ensure the volume configurations work and hysnsec/safety can handle the data properly.
Let’s move to the next step.

# Understanding Docker Run Commands and Output Redirects

In this section, we will discuss two different docker run commands and their respective output redirections. It is important to understand the differences between these commands and their effects on output storage.

## Saving the Output within the Container
```
docker run --rm -v $(pwd):/project image_name sh -c "command --json > output.json"
```
Example:
```
docker run --user $(id -u):$(id -g) \
    -v $(pwd):/zap/wrk/:rw \
    -t --name zap-scan \
    -t ghcr.io/zaproxy/zaproxy:stable \
    sh -c "zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html > output1.html"
```
The purpose of this code is to run a Docker container using the docker run command. Here's a breakdown of the options and the command:
- --user $(id -u):$(id -g): This sets the user and group ID of the container to the current user and group ID of the host machine.
- -v $(pwd):/zap/wrk/:rw: This mounts the current working directory of the host machine to the /zap/wrk/ directory in the container, with read-write permissions.
- -t --name zap-scan: This gives the container the name zap-scan.
- -t: This allocates a pseudo-TTY and allocates a pseudo-TTY to the container.
- ghcr.io/zaproxy/zaproxy:stable: This is the image name and tag to use for the container. In this case, it's the stable version of the ZAP (Zed Attack Proxy) image.
- sh -c "...": This runs a new shell (in this case, the sh shell) and executes the command inside the container.
- zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html > output1.html: This is the command to run inside the container. It runs the zap-baseline.py script with the following options:
- -t https://prod-p30jrhut.lab.practical-devsecops.training: specifies the target URL to scan.
- -r testreport.html: specifies the output file name for the report.
- > output1.html: redirects the output to a file named output1.html in the container.
In summary, this command runs a ZAP container with a specific configuration, scans the specified URL, and saves the report to a file named output1.html in the container.

Command Output:
```
bin   dev  home  lib32  libx32  mnt  proc  run   srv  testreport.html  tmp  var
boot  etc  lib   lib64  media   opt  root  sbin  sys  testreport.json  usr  zap.yaml
```

## Saving the Output on the Local Machine<br>
`docker run --rm -v $(pwd):/project image_name sh -c "command --json" > output.json`

Example:
```
docker run --user $(id -u):$(id -g) \
    -v $(pwd):/zap/wrk/:rw \
    -t ghcr.io/zaproxy/zaproxy:stable \
    sh -c "zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html" > output2.html
```
The purpose of this command is to run a Docker container with the ZAP (Zed Attack Proxy) tool and perform a web application security scan on a target URL, generating a report in HTML format.

Here's a breakdown of the command:

docker run: This command is used to run a Docker container.
- --user $(id -u):$(id -g): This option sets the user ID and group ID of the container to the current user's ID and group ID on the host machine.
- -v $(pwd):/zap/wrk/:rw: This option mounts the current directory (identified by pwd) to the /zap/wrk/ directory in the container, with read-write permissions.
- -t ghcr.io/zaproxy/zaproxy:stable: This option specifies the Docker image to use, which is the official ZAP image from the GitHub Container Registry.
- sh -c: This option runs a command inside the container using the shell.
- zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -r testreport.html: This command runs the zap-baseline.py script with the following options:
- -t https://prod-p30jrhut.lab.practical-devsecops.training: specifies the target URL to scan.
- -r testreport.html: specifies the output file name and format (HTML).
- > output2.html: redirects the output of the command to a file named output2.html in the current directory.
In summary, this command runs a ZAP container, mounts the current directory to the container, and performs a web application security scan on the specified target URL, generating a report in HTML format, which is saved to a file named output2.html

By understanding these different ways to redirect output in docker run commands, you can manage your data more effectively and easily access it for analysis later.

 ## Understanding and Modifying Docker Run Commands
Understanding and modifying docker run commands is key to using Docker effectively and integrating it into your workflows. Here are some important points:

Pay attention to the order and placement of arguments, options, and commands in the docker run command.
Know the options for volume mappings, working directory settings, and output redirects, as they affect the container’s behavior and output storage.
Always check the documentation for the tool or command you are running in the Docker container to ensure correct syntax and arguments.
By understanding and adjusting your docker run commands, you can fully utilize Docker and manage your containerized applications efficiently.

Let’s move to the Conclusion.

# Conclusion
Through your research and testing, you’ve learned how to:
- Configure appropriate volumes for Docker containers
- Manage output redirection between containers and host machines
- Customize Docker run commands for specific needs

Key takeaways:
1. Read the documentation of the tool you are using
2. Test Docker run commands locally before CI/CD integration (this is important!)

Good luck with integrating other security tools into your DevSecOps pipeline!
