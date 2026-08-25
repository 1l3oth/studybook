#!/usr/bin/env node
/*
 * Installer for the "studybook" Claude skill + the /teach-me command.
 * Copies skill/studybook/ -> <base>/skills/studybook and command/teach-me.md -> <base>/commands/teach-me.md.
 *
 *   npx github:1l3oth/studybook            -> global   (~/.claude, or $CLAUDE_CONFIG_DIR)
 *   npx github:1l3oth/studybook --project  -> project  (./.claude)
 *   npx github:1l3oth/studybook --dir X    -> a .claude directory you name
 *
 * No dependencies; runs on any Node >= 14.
 */
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');

const args = process.argv.slice(2);
const has = (f) => args.includes(f);
const dirArg = (() => { const i = args.indexOf('--dir'); return i >= 0 ? args[i + 1] : null; })();

function claudeBase() {
  if (dirArg) return path.resolve(dirArg);
  if (has('--project') || has('-p')) return path.join(process.cwd(), '.claude');
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function main() {
  const root = path.join(__dirname, '..');
  const skillSrc = path.join(root, 'skill', 'studybook');
  const cmdSrc = path.join(root, 'command', 'teach-me.md');
  if (!fs.existsSync(path.join(skillSrc, 'SKILL.md'))) {
    console.error('error: skill payload not found at ' + skillSrc);
    process.exit(1);
  }

  const base = claudeBase();
  const skillDest = path.join(base, 'skills', 'studybook');
  const cmdDest = path.join(base, 'commands', 'teach-me.md');
  const existed = fs.existsSync(skillDest);

  copyDir(skillSrc, skillDest);
  fs.mkdirSync(path.dirname(cmdDest), { recursive: true });
  fs.copyFileSync(cmdSrc, cmdDest);

  console.log((existed ? 'Updated' : 'Installed') + ' studybook:');
  console.log('  skill:   ' + skillDest);
  console.log('  command: ' + cmdDest);
  console.log('');
  console.log('Restart Claude Code so it loads them, then just type:');
  console.log('  /teach-me                 (it will ask what you want to learn)');
  console.log('  /teach-me <topic>         or paste your text / a link after it');
  console.log('');
  console.log('Sample to copy from: https://1l3oth.github.io/studybook/  (feed: /feed.xml)');
}

main();
