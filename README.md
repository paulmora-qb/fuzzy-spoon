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

The codebase is using `kedro` for managing the pipelines. It is also making us
of [dynamic pipelines](https://getindata.com/blog/kedro-dynamic-pipelines/).

For all pipelines it is needed to define a `topic` that the post is generally trying to
do, for example the generation of `quotes`. The second step is then to define
the subtopics such as `life`, `love`, `breakup`. Those are then defined in the `config`
files.

To run the `quote` pipeline for example, one needs to write:

```bash
kedro run --pipeline quote_pipeline
```

The above will create images for all subtopics that were defined.

```
## Further Notes

The project was described and explained in more detail on my blog.
```
