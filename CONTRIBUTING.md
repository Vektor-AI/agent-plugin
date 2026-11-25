# Contributing

Open a pull request for workflow instructions, synthetic examples, or package checks. Describe the operator’s task, the evidence the assistant should inspect, and how you checked the result. Use synthetic freight records and report which host and version you tested.

Edit the shared skill in `skills/`. Keep the name and description useful for automatic discovery. Add a case for a correct outcome and a nearby request or missing-data state that should produce a different result. Update the portable and Claude manifests together when their shared identity, description, or version changes. Run the commands in the [README](README.md) before submitting.

Keep customer details, conversation logs, access tokens, raw freight documents, and internal configuration out of issues and pull requests. Use the [private reporting channel](SECURITY.md) for security findings. Package publication and marketplace configuration are maintainer changes.
