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
```

2. Creating the hashtags and posting the image onto instagram. This pipeline can be
   triggered through

```
kedro run --pipeline insta_publish
```

## Further Notes

The project was described and explained in more detail on my blog.
