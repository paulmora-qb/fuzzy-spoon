# Automated Instgram Content

## Overview

This repository creates images which are afterwards posted to an instagram account.
Basically what happens is that text is created and applied on an image. Afterwards
some fitting hashtags are created on basis of that text, those are then used
as the caption.

The text that is applied on the images and the hashtags are created using a LLM.

## Example Image

One example of such an image would be the following. The text was created through a LLM
and the text and the author are then applied on the white canvas.

<img src="./images/post.png" alt="Hashtags" width="600">

Afterwards the text and author name are fed again into the LLM to generate trending
hashtags that are relevant to that post.

<img src="./images/hashtags.png" alt="Hashtags" width="600">

The LLM is also fed the information of what posts the LLM has already created in the
past. That helps to avoid creating text and therefore images which were already
created in the past.

## How to run the codebase

To run the codebase one would need as the first step install all relevant requirements,
stated in the `requirements.txt`.

The repository is using kedro pipelines for the orchestration of the python code. There
are currently two pipelines:

1. Building the image; creating the text for the image and apply the text onto the
   image. This pipeline can be triggered through

```
kedro run --pipeline image_creation


2. Creating the hashtags and posting the image onto instagram. This pipeline can be
triggered through
```

kedro run --pipeline insta_publish

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. You can install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter

To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```

pip install jupyter

```

After installing Jupyter, you can start a local notebook server:

```

kedro jupyter notebook

```

### JupyterLab

To use JupyterLab, you need to install it:

```

pip install jupyterlab

```

You can also start JupyterLab:

```

kedro jupyter lab

```

### IPython

And if you want to run an IPython session:

```

kedro ipython

```

### How to ignore notebook output cells in `git`

To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> _Note:_ Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)

```

```
