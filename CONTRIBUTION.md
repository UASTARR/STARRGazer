# How to Contribute
To contribute to this repo first make sure you are a part of the STARRGazer Organization. An easy check for this is to click the green code button on the repo page and make sure you can see an `ssh` tab

## Cloning the repo
You should clone the repo via ssh using the link under the code button we stated earlier. Then in a terminal such as windows terminal on windows navigate to the directory (folder) want to download the code to. To do this, use the command `cd <path>` to get there.

To actually clone the repo we use the command `git clone <link>` where the link is the one you coppied earlier from the code button.

If you get an error, there is a chance you haven't set up an ssh key for github for which you should google "How to set up an ssh key for github on <Insert Operating System>". If you have set up your ssh key then you may still not be in the organization and in that case follow the troubleshooting procedure at the end of this document.

## Writing Code and Branches
When writing code, we must **NEVER** write in the main branch. To check which branch you are on, run the `git branch` command and it will highlight your current branch.

Create a new branch for each feature you plan on implement and keep it small (i.e. instead of "ground-station-ui" name it "live-telemetry-graphs" to reduce scope creep in branches). To create a new branch just run the command `git branch <name>`.

Once you have finished creating a branch to actually switch to it, we use the command `git switch <branch-name>`. From here you may start writing code. For every small minor feature change, try to make a commit. This won't be covered here but feel free to ask a software team member how to do this in the slack or look up a tutorial on git at this point.

If multiple people are working on a given branch, anytime before you write any new code, run the command `git pull origin <branch-name>`. If you add the flag `--set-upstream` after the command when running it for the first time, you will not need to specify origin nor the branch name (this holds for all branches you or others make)

## Pushing to Remote
Once you have made your commits and changes, make sure you push to remote. This allows anyone to see and contribute to your changes. To do this you want to first make sure all your changes have been commited (look up a git tutorial for that), then run the command `git push origin <branch-name>`

The same `--set-upstream` flag works here and only requires you to type `git push` after the first run. It may ask you if you want to create your branch on the github repo if it is a new branch, which you can say yes to. After that your changes should be reflected to everyone else working on the repository.

It is best practice that you make small incremental changes to the codebase, then *commit* them to your local repo and *push* them to the remote repo all in one go. This means everyone has an up to date copy of your code. At the very least, push your code at the end of a worksession so it is backed up and others can see it. Theres no harm pushing late as your entire commit history will be pushed so feel free to make multiple commits before pushing.

## Pull Requests.
Pull requests allow branches to be combined in a simple and effective way. This allows us to keep main as the final polished codebase.

You can look up online for how to make a pull request on github, but simply put go onto github and open the repository. There should be a pull request tab you can click and a new button to create a new pull request. Base should be set to main and compare is set to your branch. Then title it appropriately on what you are contributing to main (name it the feature your branch adds) then add a detailed description outlining the changes you made to the code and what they accomplish. Someone then will review your changes and either give you feedback to improve upon said changes or merge it to the main repo. 

## Troubleshooting
If for whatever reason you arent able to contribute or run a command. First things first, google it. Sometimes theres a really simple fix like you typed the command wrong. AI may be able to help but be a bit more weary of its responses. 

If you aren't sure what may be the issue and searching any answers isn't helping, take a screenshot of the command output/issue and ping a software lead on slack so we can help troubleshoot. Include the command you ran in your message so we can try to reproduce the error and or better troubleshoot the problem.
