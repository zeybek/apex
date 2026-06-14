# Client Adapters

The `plugins/apex/skills/` directories are the portable source of truth. Install or symlink those directories into a compatible client's discovery path. Do not maintain separate copies of the skill instructions per client.

The Agent Skills specification defines what is inside a skill, not where each client discovers skills or how it loads always-on instructions.

## Native Plugin Installation

Codex and Claude Code can install the complete `apex` package from the repository marketplaces:

```bash
codex plugin marketplace add zeybek/apex
codex plugin add apex@apex

claude plugin marketplace add zeybek/apex
claude plugin install apex@apex
```

Replace `zeybek/apex` with a local repository path while developing changes.

The native plugins expose all four skills from the shared `plugins/apex/skills/` directory. Use the discovery paths below for clients that support Agent Skills but do not consume either plugin manifest.

## Discovery Matrix

| Client | Project skills | User skills | Always-on instructions |
|---|---|---|---|
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | `AGENTS.md` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `CLAUDE.md` |
| OpenCode | `.agents/skills/`, `.opencode/skills/`, or `.claude/skills/` | `~/.agents/skills/`, `~/.config/opencode/skills/`, or `~/.claude/skills/` | `AGENTS.md` |
| Google Antigravity | `.agents/skills/` | `~/.agents/skills/` | `.agents/rules/` |
| Antigravity CLI | `.agent/skills/` | `~/.gemini/antigravity-cli/skills/` | Client-specific rules |

Client behavior and discovery paths can change. Verify the current client documentation before automating organization-wide installation.

## Install by Symlink

From a target project, replace `/path/to/apex` and `<client-skill-directory>`:

```bash
mkdir -p <client-skill-directory>
for skill in apex-design apex-implement apex-investigate apex-review; do
  ln -s /path/to/apex/plugins/apex/skills/$skill \
    <client-skill-directory>/$skill
done
```

Symlinks keep one source of truth and work well on Unix-like systems. Use copies or another synchronization mechanism where symlinks are unavailable.

## Always-On Constitution

`AGENTS.md` is not an Agent Skill. Merge its content into the client's always-on instruction file only when those rules should apply to every task:

- Codex and OpenCode: merge into project `AGENTS.md`.
- Claude Code: merge into project `CLAUDE.md`.
- Antigravity: place the content in `.agents/rules/senior-engineering.md`.

Keep project-specific build commands, architecture facts, and conventions in the target project's own instructions. The supplied constitution is intentionally general.

## Invocation

- Codex commonly supports explicit `$apex-implement` style mentions.
- Claude Code commonly supports `/apex-implement` style commands.
- Other compatible clients may activate skills automatically from descriptions or expose their own skill picker or tool.

Descriptions are the portable activation interface. Invocation syntax is a client feature.
