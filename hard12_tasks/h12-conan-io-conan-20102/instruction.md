You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[question] Release versioning and package rebuilds

### What is your question?

Hi,

we are currently using the concept of the [CI-Tutorial](https://docs.conan.io/2/ci_tutorial/tutorial.html) for our infrastructure, which is working fine so far for everything related to "main" development.

Whenever a package publishes a new version, we check whether rebuilds of existing consumers are required.

All our products are released in a predefined cycle of a few months. At a certain stage we are freezing development for the release, create a tag for the release in each components repo and allow developers to branch of at this tag to create bug fixes if required.

In order to coordinate the versions between the release branch(es) and main development, we "reserve" a semver patch range for a release branch at the point where the above mentioned tag was created.

```
1.0.0 (tag: freeze/Q1) -> (main) 1.1.0
                       -> (release/Q1) 1.0.1 
 ```

So the main branch bumps its minor version range, so that we can use patch versions for the current release.
Somehow this also fits the the idea of only having patch fixes on release branches ... but of course the reality is different.

From time to time a developer needs to adjust the API of a component on a release branch, either compatible(but rebuild is required) or incompatible.

Especially the compatible case which requires a rebuild is the problem in our setup: as these changes will be published as a semver patch change, the rebuild detection via `conan graph build-order` will not recommend any rebuilds.

How to handle this situation in a sane way?

### Have you read the CONTRIBUTING guide?

- [ ] I've read the CONTRIBUTING guide
