Docker Networking
================================

We will learn how to use different network drivers in Docker
----------

In this scenario, you will learn about networking in Docker containers.

Bridge
---------

Docker has several Network drivers that we can use when creating the containers, including the following.

- bridge : This is the default network driver when you don’t specify a driver to the containers. Containers on the same bridged network can speak to each other, but are isolated from containers on other bridged networks. All containers can access the external network through NAT
- host: The containers use the host’s networking directly, while retaining separation on storage and processing. Ports exposed by the container are exposed on the external network using the host’s IP address
- macvlan: When creating a macvlan, you assign a parent network device (e.g. “eth0”). Each container on the macvlan network will receive its own MAC address on the network that eth0 is connected to. Each container has full network access. Warning: when misconfigured, you may overrun the network with too many MACs, or you may duplicate IP addresses
- none: networking is disabled with this network driver, containers cannot communicate to each others, nor with the external network

> Read about macvlan [here](https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/) for more explanation

Next, we will explore networking in docker with provided command called docker network.

```
docker network --help
```
To see available networks, we can use this command.
```
docker network ls
docker network list
```
output
```
NETWORK ID          NAME                DRIVER              SCOPE
a49ba9341007        bridge              bridge              local
d12b019b2364        host                host                local
ddc639acd513        none                null                local
```
As mentioned, there are three networks created when we install docker. We can create a new network with the following command.
```
docker network create mynetwork
```
We can verify the network creation process by using the following command.

```
docker network ls
```
output
```
NETWORK ID          NAME                DRIVER              SCOPE
8b2369f350d5        bridge              bridge              local
019ff813f4f4        host                host                local
4e2338e54328        mynetwork           bridge              local
a9e2bdd51902        none                null                local
```

We can also explore more details about the network using docker inspect command. As you can see, we can ascertain the subnet and the gateway assigned to the network as well.

```
docker inspect mynetwork
```
output
```
[
    {
        "Name": "mynetwork",
        "Id": "3fe38cb3e9d0e5b2667ee91c4126f899aa322845ec64c0e4046f0cbeeae7d790",
        "Created": "2021-09-01T07:35:56.832546188Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```
We can attach the network to any container with the following command.
```
docker run -d --name ubuntu --network mynetwork -it ubuntu:18.04
```
We can verify the network details using the docker inspect command.
```
docker inspect mynetwork
```
output
```
[
    {
        "Name": "mynetwork",
        "Id": "3fe38cb3e9d0e5b2667ee91c4126f899aa322845ec64c0e4046f0cbeeae7d790",
        "Created": "2021-09-01T07:35:56.832546188Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "ad503fb878ab81c81837f38659c25dd7d3f061e12c7e159ddca55be39fa83a0d": {
                "Name": "ubuntu",
                "EndpointID": "624127fafba84118fb958b35d585b3bcf13a383d905d2b64373fc836ef83d558",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

We can test the network connectivity in the container by executing apt update command. If the below command works, then the container is able to reach external world, including the DNS server.

```
docker exec ubuntu apt update
```
We are able to update the apt cache so we do have network connectivity to the internet.

Lets clean up by removing the container and the network we created before.

```
docker rm -f ubuntu
docker network rm mynetwork
```

>  Learn more about docker network [here](https://docs.docker.com/engine/reference/commandline/network).

macvlan
---------

We can create macvlan network by using the network create –driver macvlan \<network_name> command.

```
docker network create --driver macvlan mymacvlan
```
Let’s see if our network is created.
```
NETWORK ID          NAME                DRIVER              SCOPE
1201ad8119bc        bridge              bridge              local
76876641b5a2        host                host                local
8df059075f38        mymacvlan          macvlan             local
188042442f13        none                null                local
```

If we run ifconfig, we will see there is an interface with the name dm-8df059075f38.
```
ifconfig
---------
dm-8df059075f38: flags=195<UP,BROADCAST,RUNNING,NOARP>  mtu 1500
        ether f6:9b:f7:8e:93:53  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:61:86:fc:30  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.19.0.3  netmask 255.255.0.0  broadcast 172.19.255.255
        ether 02:42:ac:13:00:03  txqueuelen 0  (Ethernet)
        RX packets 2127  bytes 28809037 (28.8 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 878  bytes 72857 (72.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 28  bytes 3258 (3.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 28  bytes 3258 (3.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
We can attach the new network to a container with the following command.
```
docker run -d --name ubuntu --network mymacvlan -it ubuntu:18.04
```
Let’s cross check the network information with docker inspect.
```
docker inspect ubuntu -f "{{json .NetworkSettings.Networks }}" | jq
```
output
```
{
  "mymacvlan": {
    "IPAMConfig": null,
    "Links": null,
    "Aliases": [
      "2a42eb64e5ac"
    ],
    "NetworkID": "8df059075f385271a681a5ddc78b6f137607117aa0a5ac1cd22159c599d804c8",
    "EndpointID": "55dba5d94d70ba1554e6bff9f27c2437e96ad28fcd48786ba9944eb9217a1b3d",
    "Gateway": "172.18.0.1",
    "IPAddress": "172.18.0.2",
    "IPPrefixLen": 16,
    "IPv6Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "MacAddress": "02:42:ac:12:00:02",
    "DriverOpts": null
  }
}
```

Next, we will clean up the changes we made by removing the container and network we created.

```
docker rm -f ubuntu
docker network rm mymacvlan
```
> Learn more about docker macvlan [here.](https://docs.docker.com/network/macvlan/)

none
---------

This network disables/isolates the network in the container(s).

```
docker run -d --name ubuntu --network=none -it ubuntu:18.04
```
We can explore the network information with the docker inspect command.
```
docker inspect ubuntu -f "{{json .NetworkSettings.Networks }}" | jq
```

We can test the network connectivity in the container by executing apt update command. If the below command works, then the container is able to reach external world, including the DNS server.

```
docker exec ubuntu apt update
```

As we can see, it failed to update the packages, it doesn’t have access to the internet.


Exercise
---------
### "Challenge: Docker Networking"

1. Create a network with bridge driver called app and define 172.10.2.0/16 as a subnet

```bash
docker network create --driver=bridge --subnet=172.10.2.0/16 app
docker inspect app -f "{{json .IPAM.Config}}"
```

2. Run the containers with ubuntu:18.04 image in the background

```bash
docker run -d -it --name myubuntu ubuntu:20.04

```

3. Attach app network to the running container, detailed how to at this link

```bash
docker network connect app app
```

4. What would happen if we remove the network driver without killing the container?

Docker answer with an error while removing the network

