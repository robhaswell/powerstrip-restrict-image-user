# powerstrip-restrict-image-user
A Powerstrip adapter to restrict Docker to manipulating images published by a given user.

By specifying a `USER` environment variable you can prevent Docker from running any images not provided by a specific user or organization.

## Usage

This image is available as `robhaswell/priu`.
It accepts one configuration envar, `USER`.
This can be any user, e.g. `robhaswell`, or `_` for official images.

A typical Powerstrip configuration would look like:

    version: 1
    endpoints:
      "POST /*/containers/create":
        pre: [priu]
      "POST /*/containers/*/start":
        post: [priu]
    adapters:
      priu: http://priu/

The adapter is started with:

    docker run -d -e USER=someuser --name priu robhaswell/priu
