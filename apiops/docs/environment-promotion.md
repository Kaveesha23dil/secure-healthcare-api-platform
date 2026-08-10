# Environment promotion

```text
feature branch -> pull request -> CI validation -> develop
  -> controlled development deployment -> smoke tests
  -> manual approval -> staging -> acceptance testing
  -> release approval -> production
```

Pull requests validate only and never deploy. A merge to `develop` may deploy to development through an internal self-hosted runner. Staging uses manual workflow dispatch plus GitHub Environment approval. Promote the same reviewed API contract and immutable application image; vary only controlled environment parameters and secrets.

The OpenAPI definition uses a server variable. `BACKEND_URL` and a version-compatible `apictl` parameter file provide the environment endpoint. Do not maintain divergent contracts. Breaking v1 changes require review and usually a new `/2.x` API rather than silent v1 mutation.

Production deployment remains documentation-only for this student/demo project.
