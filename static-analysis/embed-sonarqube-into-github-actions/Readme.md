Learn how to embed SonarQube Scanner in GitHub Actions
================================================================

Use SonarQube Scanner tool to perform SAST in GitHub Actions
--------------------------------------------------------------------------------

In this scenario, you will learn how to embed SonarQube Scanner in GitHub Actions

Configure SonarQube
----------

configure like previous lab SQ

Embed SonarQube Scan in GitHub Actions
--------------------------------------------------------------------------------

As discussed in the Static Analysis using SonarQube exercise, we can embed SonarQube in our CI/CD pipeline. Now we need to embed SonarQube into CI/CD pipeline using the SonarQube Scan actions available from the GitHub Marketplace.

We will create credentials to save our SonarQube token using secrets in our repository. To set up a secret, go back to django.nv repository and click the Settings tab.

Click the Secrets option, then select New repository secret and add the following credentials into it.

> Name: SONAR_TOKEN
> 
> Value: Paste the token we just generated in SonarQube

> Name: SONAR_HOST_URL
> 
> Value: https://sonarqube-XqiHnDZ0.lab.practical-devsecops.training

Once done, click the Add secret button.

Let’s head back to the DevSecOps Box machine, and copy the below content to the .github/workflows/main.yaml file under test job.

```
  sonarqube:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        # Disabling shallow clone is recommended for improving relevancy of reporting
        fetch-depth: 0

    - name: SonarQube Scan
      uses: sonarsource/sonarqube-scan-action@master
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      with:
        projectBaseDir: .
        args: >
          -Dsonar.projectKey=Django
```

> Notice the errors? Please fix those errors and re-run the scan again.

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our django.nv repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.