# Releasing the plugin

People get the plugin from this repository or from a plugin directory that serves its own copy. A merge reaches existing installs only when the version changes.

## Release a change

1. Raise `version` in `.claude-plugin/plugin.json` and `plugin.json` together. Use a minor version for a new or changed workflow and a patch version for a wording fix.
2. Add a `## <version>` entry to [the changelog](CHANGELOG.md) that says what changes for operators.
3. Run `PLUGIN_BASE_REF=origin/master make check validate`. The check fails when a skill, manifest or the icon changed since the branch you merge into without a higher version.
4. If another release merged after the checks ran, update the branch from `master` and let the checks run again. They compare with the branch as it was when they ran.
5. Merge. Installs from this repository pick up the new version the next time the assistant updates its plugins.

## Copies served by a directory

A directory listing follows the branch or tag chosen when the plugin was submitted. Check that the listing shows the new version after its review. Installs from a directory update from that copy, not from this repository.

## Check an update

In a clean Claude Code profile, install the previous release, then run `claude plugin update vektor@vektor-plugins` and confirm the new version and its workflows with `claude plugin details vektor`.
