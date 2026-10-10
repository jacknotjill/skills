# Third-party skills

These skills come from other people's repositories under the MIT licence. Each
is copied unchanged, with the upstream `LICENSE` added inside the skill folder
so the licence travels with it when installed.

| Skill | Upstream | Commit |
| --- | --- | --- |
| `show-me` | [humanlayer/skills](https://github.com/humanlayer/skills) `plugins/show-me/skills/show-me` | `653b641` |
| `visual-pr` | [humanlayer/skills](https://github.com/humanlayer/skills) `plugins/visual-pr/skills/visual-pr` | `653b641` |
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) `skills/productivity/grill-me` | `49dd158` |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) `skills/productivity/grilling` | `49dd158` |

`grill-me` is the entry point you type (`/grill-me`); it hands over to
`grilling`, which runs the interview, so the two ship together.

## Updating

Don't edit these folders by hand, because the next refresh would undo it.
Run `scripts/vendor.sh latest` to pull each upstream's current version, review
the diff, then update the commits in `scripts/vendor.sh` and in the table above.
`scripts/vendor.sh` on its own restores the pinned versions.

To change how one of these behaves, write your own skill that builds on it
rather than editing the copy.
