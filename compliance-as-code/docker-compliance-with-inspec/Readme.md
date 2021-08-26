Docker Compliance using Inspec
================================

Learn how to implement CIS Docker Benchmark using the Inspec tool
----------

In this scenario, you will learn how to implement CIS Docker Benchmark checks as an Inspec profile.

Let’s install the Inspec on the system to learn Compliance as code.

Download the Inspec Debian package from the InSpec website.

```
wget https://packages.chef.io/files/stable/inspec/4.18.114/ubuntu/16.04/inspec_4.18.114-1_amd64.deb
dpkg -i inspec_4.18.114-1_amd64.deb
inspec --help
```
Run the Inspec profile
----------

In addition to scanning a host, we can also use Inspec to inspect a running container or the Docker Daemon itself. We can define compliance controls in our organization and avoid running containers that do not satisfy the organization’s compliance baselines.

Lets try to check whether our servers follow the CIS Docker Benchmark best practices using the Dev-Sec’s cis-docker-benchmark Inspec profile.

Let’s run the profile against the DevSecOps Box(local machine).

```
inspec exec https://github.com/dev-sec/cis-docker-benchmark --chef-license accept
```
output
```
+---------------------------------------------+
✔ 1 product license accepted.
+---------------------------------------------+
[2021-02-14T04:47:07+00:00] WARN: URL target https://github.com/dev-sec/cis-docker-benchmark transformed to https://github.com/dev-sec/cis-docker-benchmark/archive/master.tar.gz. Consider using the git fetcher

Profile: CIS Docker Benchmark Profile (cis-docker-benchmark)
Version: 2.1.2
Target:  local://

  ×  docker-4.2: Use trusted base images for containers
     ×  Environment variable DOCKER_CONTENT_TRUST content is expected to eq "1"

     expected: "1"
          got: nil

     (compared using ==)

  ↺  docker-4.3: Do not install unnecessary packages in the container
     ↺  Do not install unnecessary packages in the container
  ↺  docker-4.4: Rebuild the images to include security patches
     ↺  Rebuild the images to include security patches
  ×  docker-4.5: Enable Content trust for Docker
     ×  Environment variable DOCKER_CONTENT_TRUST content is expected to eq "1"

     expected: "1"
          got: nil

     (compared using ==)

  ↺  docker-4.8: Remove setuid and setgid permissions in the images
     ↺  Use DevSec Linux Baseline in Container
  ↺  docker-4.10: Do not store secrets in Dockerfiles
     ↺  Manually verify that you have not used secrets in images

  ...[SNIP]...

  ×  host-1.7: Audit docker daemon (4 failed)
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
     ×  Service auditd is expected to be installed
     expected that `Service auditd` is installed
     ×  Service auditd is expected to be enabled
     expected that `Service auditd` is enabled
     ×  Service auditd is expected to be running
     expected that `Service auditd` is running
  ×  host-1.8: Audit Docker files and directories - /var/lib/docker
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
  ×  host-1.9: Audit Docker files and directories - /etc/docker
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
  ↺  host-1.10: Audit Docker files and directories - docker.service
     ↺  Cannot determine docker path
  ↺  host-1.11: Audit Docker files and directories - docker.socket
     ↺  Cannot determine docker socket
  ×  host-1.12: Audit Docker files and directories - /etc/default/docker
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
  ×  host-1.13: Audit Docker files and directories - /etc/docker/daemon.json
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
  ×  host-1.14: Audit Docker files and directories - /usr/bin/docker-containerd
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist
  ×  host-1.15: Audit Docker files and directories - /usr/bin/docker-runc
     ×  Auditd Rules
     Command `/sbin/auditctl` does not exist


Profile Summary: 15 successful controls, 25 control failures, 35 controls skipped
Test Summary: 79 successful, 80 failures, 36 skipped
```

You can see, the output does inform us about 15 successful controls and 25 control failures.

The above profile not only helps us in scanning for daemon related misconfigurations but also running containers. Let’s try to run a docker container and see this functionality in action!

```
docker run -d --name alpine -it alpine /bin/sh
```

We can see all the running containers on a machine using the docker ps command.

```
docker ps
```

We will now run the linux-baseline profile against this container.

```
inspec exec https://github.com/dev-sec/linux-baseline --chef-license accept -t docker://alpine
```

> You can also use container name or container id as URI target

output
```
[2021-02-14T05:51:53+00:00] WARN: URL target https://github.com/dev-sec/linux-baseline transformed to https://github.com/dev-sec/linux-baseline/archive/master.tar.gz. Consider using the git fetcher

Profile: DevSec Linux Security Baseline (linux-baseline)
Version: 2.6.4
Target:  docker://871af75c081a67c2ad05d1dacb1eb81960c4b064823cf58aa0ea11c254ff3a2f

  ✔  os-01: Trusted hosts login
     ✔  File /etc/hosts.equiv is expected not to exist
  ×  os-02: Check owner and permissions for /etc/shadow (1 failed)
     ✔  File /etc/shadow is expected to exist
     ✔  File /etc/shadow is expected to be file
     ✔  File /etc/shadow is expected to be owned by "root"
     ✔  File /etc/shadow is expected not to be executable
     ✔  File /etc/shadow is expected not to be readable by other
     ✔  File /etc/shadow group is expected to eq "shadow"
     ✔  File /etc/shadow is expected to be writable by owner
     ✔  File /etc/shadow is expected to be readable by owner
     ×  File /etc/shadow is expected not to be readable by group
     expected File /etc/shadow not to be readable by group

  ...[SNIP]...

  ↺  sysctl-31b: Secure Core Dumps - dump path
     ↺  Skipped control due to only_if condition.
  ↺  sysctl-32: kernel.randomize_va_space
     ↺  Skipped control due to only_if condition.
  ↺  sysctl-33: CPU No execution Flag or Kernel ExecShield
     ↺  Skipped control due to only_if condition.


Profile Summary: 15 successful controls, 2 control failures, 39 controls skipped
Test Summary: 39 successful, 8 failures, 40 skipped
```

Now that we have a container running, what would happen if we run the cis-docker-benchmark profile again on this machine?

```
inspec exec https://github.com/dev-sec/cis-docker-benchmark --chef-license accept
```
output

```
...[SNIP]...

Profile Summary: 29 successful controls, 36 control failures, 35 controls skipped
Test Summary: 100 successful, 94 failures, 36 skipped
```

The output changes from 15 successful controls to 29 and 25 control failures to 36.

This change is because of skipped container runtime checks as no containers were running when we first used this inspec profile. After we started a container, Inspec also included runtime checks as part of the scan.

We can verify this behaviour by visiting https://github.com/dev-sec/cis-docker-benchmark and selecting the container_runtime.rb under the controls directory.

