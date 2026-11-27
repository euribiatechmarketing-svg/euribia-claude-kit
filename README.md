# Euribia Claude kit

The skills, agents and content playbooks the Euribia team uses with Claude Code,
plus setup steps for T3 Code. For macOS.

## What's inside

| Folder | What it is |
|---|---|
| `skills/` | 31 skills: `contento` (content orchestrator), copywriting, social, SEO/AEO (`seo-audit`, `ai-seo`, `schema`, `eudigital-aeo`), design (`impeccable`, `frontend-design`, `taste-skill`, `awesome-design-md`, `brandkit`, `gift-tube`, `figma-perspective` …), `llm-council`, `playwright-cli` |
| `agents/` | 7 contento agents: ads, articles, clickup, content, presentation, research, visual |
| `contento/` | Playbooks (posts, articles, ads, design system, PostFlow), brand assets, blog-cover tools |
| `fonts/` | Mulish + Azeret Mono (brand fonts, OFL licence) |
| `install.sh` | Copies everything into `~/.claude` and installs the plugins |

Plugins the installer adds: **superpowers** and **ui-ux-pro-max**.

## Setup on a new Mac

### 1. Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude            # sign in with your own Claude account once, then /exit
```

### 2. This kit

```bash
mkdir -p ~/Developer/projects && cd ~/Developer/projects
gh repo clone euribiatechmarketing-svg/euribia-claude-kit   # or git clone the URL
cd euribia-claude-kit
./install.sh
```

Then open `~/.config/euribia/api-keys.env` and paste the `POSTFLOW_API_TOKEN` (ask Dimitar).

### 3. T3 Code

```bash
brew install --cask t3-code
```

Or download the `.dmg` from <https://github.com/pingdotgg/t3code/releases> (pick Apple Silicon or Intel).

Open T3 Code, choose **Claude** as the provider. It uses the Claude Code you installed in step 1,
so the skills from this kit show up there too. Add a project with **Add project** → pick a folder
(for example `~/Developer/projects`).

### 4. Connectors (each person does this once)

Several skills call Figma, ClickUp, Google Drive and Higgsfield. These are connected per Claude
account, not copied by this kit: go to **claude.ai → Settings → Connectors** and connect
Figma, ClickUp, Google Drive and Higgsfield with your own login.

### 5. Check it works

In T3 Code (or `claude`), type `/contento` or ask "what skills do you have?".

## Updating

```bash
cd ~/Developer/projects/euribia-claude-kit && git pull && ./install.sh
```

The installer backs up anything it replaces to `~/.claude/backups/kit-<date>/`.

## Not included on purpose

- Personal memory, `CLAUDE.md`, API keys
- The recurring publishing engine's schedule and ledger (`contento/state/ledger.json`, scheduled tasks).
  It runs on one machine only, so posts don't get published twice.
- Large asset folders (carousel exports, inbox). Ask for files you need.

Some playbooks point to folders on Dimitar's Mac (`~/Documents/01-Euribia/...`). If a skill
asks for one of those files, save outputs to your own matching folder or ask for the file.

## Maintainer: refresh the kit from your Mac

Copy changed skills from `~/.claude/skills/` into `skills/`, replace `/Users/<you>/` with `~/`,
commit and push.
