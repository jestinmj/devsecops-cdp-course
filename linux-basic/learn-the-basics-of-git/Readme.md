Git Basics
=======================

We will learn the basics of Git, such as commit, pushing changes
-----

In this scenario, you will learn the basics of working with Git as a Source Code Management (SCM) system.

The information taught in this exercise are essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.

Working with Git Locally
----------

> Git is a well-known version control system AKA source code management system. It is used to store the application code and configurations. With DevOps, we are now storing infrastructure as code, security as code, and other necessary documentation in Git.
>
> Git is the most usable skill for any DevOps/DevSecOps Engineer, and many DevOps methodologies rely on git as a version control system like GitOps, Infrastructure as Code, CI/CD pipelines and Cloud-Native.

Initial git setup
----------

To work with git repositories, we need to first setup a username and email.

We can use git config commands to set it up.

```
git config --global user.email "student@pdevsecops.com"
git config --global user.name "student"
```

Download/clone/copy the repository
-----
We can use the git clone command to download the git repository to a local machine.
```
git clone http://root:pdso-training@gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git
cd django-nv
```

Add a file to the repository
-----------

Let’s create a file in the repository using the cat command.

```
cat > myfile <<EOL
This is my file
EOL
```
While we are at it, lets modify the README.md file with a new line.
```
echo "Practical DevSecOps" >> README.md
```
Once you create a file or modify a file, you can check the status of the repository (that is what files are added, modified, removed)

```
git status
```
As we can see myfile is under Untracked files, and README.md is under modified.

We need to use git add command to add these two files to store them in the Git repository. Even though, these two files are in the directory, they are not yet added to the repository.

So lets add them.

```
git add myfile README.md
git status
```
output
```
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   README.md
        new file:   myfile
```
Wonderful, two files are added to the repo. Next, we need to commit these changes to the repo. Unlike typical file operations, adding a file to a git repo is a two-step process.

1. Add the file(s) to the stage
2. Commit the changes to the repository

We already did step 1. Let’s commit the changes to the repo (short for repository) using the git commit command.

```
git commit -m "Add myfile and update README.md"
-----
[master fb7a678] Add myfile and update README.md
 2 files changed, 2 insertions(+)
 create mode 100644 myfile
```
 -m is a comment that is required while committing changes to Git.

Pushing Commits to the Remote Repository
-----------

> Since Git is a decentralized source code management system, all changes live in your local git repository till you push them to the server. Think it like this, git was meant to run even when you do not have internet connectivity, on flights, vessels, or in a jungle somewhere.
>
> We have internet connectivity, lets push the local changes to the remote git repository using git push command.


```
git push
```
Let’s open up the GitLab URL in your browser to see these changes https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.

We can use the GitLab credentials provided below to login i.e.,

Pull the changes from the repository
------------------------------------------------

Suppose someone has a copy of this repo on their machine. That person can pull/download these changes using the git pull command.

```
git pull
```

> Sometimes during the exercises we might use GitLab Web UI to edit some files. While we can technically clone a repository, change a file, stage, commit, and push, to make editing a little convenient, we might choose to use GitLab Web UI.
>
> However at any time during the lab, if you are comfortable with git cli, and prefer not to use GitLab Web UI to edit files such as .gitlab-ci.yml, feel free to use git cli.

