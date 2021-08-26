Welcome to Practical DevSecOps Labs
=======================

Are you new to DevSecOps? This is the perfect place to start learning!
----

Are you ready to explore DevSecOps?

Practical DevSecOps is all about learning by doing and practical skills. In this lesson, we’ll take you through the basics of how to use the labs and show you some of the power of DevSecOps!

In this scenario, you will learn how to use Practical DevSecOps Labs DevSecOps environment.

The User Interface
----------

The section below this text contains instructions about what to do and how to proceed to the next step.

The left panel contains the instructions to complete a lesson/exercise, and the right panel in the browser includes a terminal placeholder to run the commands.

> Move your mouse cursor over to the right and click on Start the Exercise button.
>
> You need to click on this button every time without fail; otherwise, your machines won’t be provisioned


Run a command!
----------------------------------------------------------------

To achieve DevSecOps Goals, we do have to install, configure and run commands.

The commands will run in the terminal available in the right panel, and the commands are marked with a dark background and has an Enter symbol at the end.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
cd webapp
```

Woah, it worked.

You can also interact with the terminal by typing some commands like ls.

Support Channel
----------

Got any questions? Contact us in the cdp channel on the slack.

Take a note
----------

Sometimes, you need a tip or a hint to solve a challenge. We provide these tips using a light purple color background.

> I’m a tip, take a note of me as I’m here to help.

Copying is the best form of flattery
----------

We might have twisted Oscar Wilde’s quote, but copying text to configure a system like CI/CD helps in performing a task faster.

You can copy the following text by clicking on it.

```
stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  script:
    - echo "This is a build step."

test:
  stage: test
  script:
    - echo "This is a test step."

integration:
  stage: integration
  script:
    - echo "This is an integration step."
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

> Oh fancy, the text jiggles when clicked on it

Now that you have copied the text open a text editor and paste the text. You can use Control + V on Windows and Linux; Command + V on Mac OS.

Need credentials?
----------------------------------------------------------------

Okay, time to copy some credentials now!

Click on the following clipboard icons to copy the username and password.

Support Channel
----------

Got any questions? Contact us in the cdp channel on the slack.

Appreciate the art of noticing
--------------

Wouldn’t the world be boring if all we do is copy/paste stuff?. We display the contents of a file or essential facts using a light green color highlight, so you can notice the differences or changes from the previous steps.

```
sast:
  stage: build
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    - docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  artifacts:
    paths: [bandit-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```

> Notice the last line allow_failure: true, its important for DevSecOps.

Refer to a link
----------

The external links like a project’s home page, references, and sources provide more context to the exercise.

These links are shown in the bluish-purple color. You can click them to open in another browser tab.

Project’s homepage: [Click me](https://github.com/PyCQA/bandit) to open a link

Last but not least, we do not add unnecessary information in the labs so please make a note of it as these might be asked in the exam.

> Protip: take lots of notes. You might pass the certification exam because of good notes.


Something went wrong?
--------------------------------

If you feel something is not right or you would like to re-start the exercise, just refresh the page using your browser’s refresh button.

A gentle reminder
----------

In this exercise, you have learned how to make use of this portal.

You explored how tips help you notice important information.

> Always remember to click on the Start the Exercise button!
>
>Always remember to click on the Start the Exercise button!
>
> Always remember to click on the Start the Exercise button!

Nope, it’s not a mistake. We repeated the same note thrice, so you remember this crucial fact.

You can run a command in the terminal by copying and pasting it in the terminal.

We display information that might be of some importance. For e.g.,

```
sast:
  stage: build
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    - docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  artifacts:
    paths: [bandit-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```

Lets move to the next exercise
-----------

To make good use of the available display real estate, we avoid linking to the next exercises. Please go back to the parent module by using the browser’s back button and click on the appropriate exercise.

We are here to help
--------------

Got any questions? Reach out to us in the cdp channel on the slack.

Congratulations, good luck with your DevSecOps Journey.