
# Developer Resources

## Git Development Guidelines

- <https://bmad-sim.github.io/pytao/dev_docs/development.html>

- Do not commit directly to Main (unless trivial)

- Development done on branches

- Merges into the original repository must be reviewed

- Short development cycles

- Continuous integration using GitHub Actions



## Quick Start Guide

First, you'll need to create your own local copy of the EIC-lattice
repository to work with. You may wish to install and use
[GitHub Desktop](https://docs.github.com/en/desktop) to manage your code.
This app provides a GUI to interact with GitHub repos, enabling you to fork,
clone, push changes, and so on. Alternatively, if you prefer to use git from
a terminal, you can set up and manage things from the command line.

### Create a local copy of the repository (manual/command line)

1. Create a fork of the EIC-lattice repository

    Navigate to <https://github.com/xelera/eic-lattice> and click on Fork
    in the upper right.
    Now you have a clone of the repo on your own GitHub space.

2. Set up SSH if necessary

    If you are new to using GitHub, you will want to set up SSH keys.
    See [Connecting-to-github-with-ssh](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)
    for instructions on how to create a local SSH key pair and add your
    public key to your GitHub account.

3. Create a local clone of your forked repository
    * On your forked repo on GitHub, click the
    <span style="background-color:green; color:white">&nbsp;Code&nbsp;</span>
    button and copy the address to
    clone with SSH (`git@github.com:YOUR-USERNAME/eic-lattice.git`).
    * On your local machine, navigate to wherever you would like the top-level
    EIC-lattice directory to be created and clone your forked copy:
    
        `git clone git@github.com:YOUR-USERNAME/eic-lattice.git`

    Now you have a local copy. You can create branches, make changes and
    commit, etc. You will push changes to your forked repo on GitHub
    and when you are ready to have your changes merged back to the original
    repository, you create a pull request.

    For more information on managing your local repository and the general
    workflow, see <https://bmad-sim.github.io/pytao/dev_docs/development.html>.

## Environment Setup

Many files rely on the `EIC_LATTICE` environmental variable set as:
```bash
export EIC_LATTICE=/path/to/this/repository/
```
