---
layout: post
title:  "My Git Workflow"
date: 2018-02-26 12:00:00 +0100
has_code: true
time_to_read: 5
---

I find my current [Git](https://git-scm.com/) workflow pretty productive and robust, so I decided to document it to help others out and to see how my workflow changes over time.

### Branching
Everything I do, I do on a [feature branch](https://git-scm.com/docs/git-branch). Whether I’m fixing bugs, resolving [merge](https://git-scm.com/docs/git-merge) conflicts or even if I’m working on a forked copy of another repository. I always work on feature branches and never [commit](https://git-scm.com/docs/git-commit) on master. I normally set the upstream branch to master, unless I’m working off another feature branch (but I rarely do this).

{% highlight bash %}
git checkout master
git pull origin/master
git checkout -b <TICKET_NUMBER>_<DESCRIPTIVE_BRANCH_NAME>
{% endhighlight %}

### Naming
Currently, I always prepend the name/number of my [Jira](https://www.atlassian.com/software/jira) ticket in the name of my branches. This is highly dependent on my current work environment and internal tooling, but I feel like I would continue this practice wherever I go (as long as I’m allowed). Commits or branch names often don’t have enough context for _why_ something was done, and I find tickets are the right place to add this context. Including the ticket number in the branch name makes it easy to find these tickets! I do not include my username in my branch names as git logs contain this information.

### Deleting Branches
After I merge in a branch, I usually wait a week (or however long until I feel like it won’t be reverted) and then delete it from my origin and local machine. This clears up space. Simple.

{% highlight bash %}
git push --delete origin <BRANCH_NAME>
git branch -d <BRANCH_NAME>
{% endhighlight %}

### Commits
I strongly believe that every commit in a git history should be in a working state. In other words, I should be able to [revert](https://git-scm.com/docs/git-revert) or rollback to a certain commit and have the code work (compile or run without errors). This gives me confidence that if something breaks on master, someone can just pick a random commit and revert to it without having to figure out that it works.

That doesn’t mean that each feature branch just has one commit, it just means that each commit works in it’s own right. This also doesn’t stop me from committing often, I just tend to amend my previous commit until I’m happy with it. I’m ok [“changing history”](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) on feature branches as no one really cares about their history. On the other hand, I never (and I mean never) amend a commit on master. This goes back to my point of never committing on the master branch.

**Warning:** Be careful _force_ pushing these amended commits!

### Rebasing
Often, when working on a feature branch, something on the [upstream branch](https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches) will change and the feature branch will conflict. In this case, I tend to prefer [rebasing](https://git-scm.com/docs/git-rebase) instead of merging. The saves my feature branch being littered with merge commits that become confusing when the feature branch is merged into master. It also means when the feature branch is merged into master, it’s commits are located closely together and close to the top of the git log. I find all of these things useful when reading master’s git log.

One downside of this approach is that you have to solve potentially multiple conflicts as you rebase each commit on your feature branch. But I think this is well worth it for a clear and concise git log.

{% highlight bash %}
git fetch origin
git rebase origin/master
{% endhighlight %}

### Merging into Master
When I’m finished working on a feature branch, it’s time to merge it into master. I try to remember to always merge my feature branch without fast-forward'ing (`--no-ff`) so that a merge commit is always constructed. This makes it easy to revert many changes from a feature branch in one go (just revert the merge commit!) and makes me feel safe deploying code.

{% highlight bash %}
git merge --no-ff <BRANCH_NAME>
{% endhighlight %}

And... that's about it. I hope this overview of my workflow was helpful!
