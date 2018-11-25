# Contributing

I love to work together with people so if you have a great idea for a feature, improvements or maybe you found 
some bug, please, don't hesitate in adding an issue, so we can discuss and find a good solution together.

So if you would like to contribute, the first thing you can do is to install the framework and give it a go. It
is super easy to install (you can use pip) and there is also a CLI that can help you creating your first
application.

If you are ready to write some code:

1. Fork the project
2. Create a new branch from the development branch
3. Hack away
4. When you are ready, submit the pull request

## branch guidelines

Try to create name the branch with something that gives an idea what the changes in that is about, for instance,
if you are adding static type check (mypy) the branch could be named `static-type`. Plus, to help me out with the process of going through the pull requests, include the prefix `feat` on the branch name, 
like so: `feat-static-type`.

Before sending your pull request, there are some things to check:

- Is this feature tested in different systems (Linux/MacOSX/Windows)?
- PEP8 compliant?
- Unit-tests?
- Well-formatted?

The same pattern is valid for bugfixes and improvements, see `Prefixes for branches and commits` for more details.

## Commits

When it comes to committing your changes, if it is possible to add less commits as possible or before sending me to pull request
squash the related commits together that I will facilitate the code-review work, I will do before accepting 
your changes.

Also, please include the issue number in the pull request message. **Pull requests without an issue number
won't be accepted.**

Let's say you added unit tests for the RouteResolver class and the issue for this feature is #123, a good
pull request message would be `(feat) - add unit tests for the RouteResolver` as a title and the body
`Resolve issue #123`

### Prefixes for branches and commits

|prefix|description|
|---   |---   |
|feat| New features
|improv| New improvements in existing features|
|bug| Prex for bug fixes|

## Helpful links

https://www.python.org/dev/peps/pep-0008/

http://mypy-lang.org/

http://nose.readthedocs.io/en/latest/

