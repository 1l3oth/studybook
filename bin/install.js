#!/usr/bin/env node
/*
 * Installer for the "studybook" Claude skill.
 * Copies skill/studybook/ into the target Claude skills directory.
 *
 *   npx github:1l3oth/studybook            -> global (~/.claude/skills, or $CLAUDE_CONFIG_DIR/skills)
 *   npx github:1l3oth/studybook --project  -> this project (./.claude/skills)
 *   npx github:1l3oth/studybook --dir X    -> a skills dir you name
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

function skillsDir() {
  if (dirArg) return path.resolve(dirArg);
  if (has('--project') || has('-p')) return path.join(process.cwd(), '.claude', 'skills');
  const base = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
  return path.join(base, 'skills');
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
  const source = path.join(__dirname, '..', 'skill', 'studybook');
  if (!fs.existsSync(path.join(source, 'SKILL.md'))) {
    console.error('error: skill payload not found at ' + source);
    process.exit(1);
  }
  const target = skillsDir();
  const dest = path.join(target, 'studybook');
  const existed = fs.existsSync(dest);
  copyDir(source, dest);

  console.log((existed ? 'Updated' : 'Installed') + ' the "studybook" skill:');
  console.log('  ' + dest);
  console.log('');
  console.log('Restart Claude Code (or your agent) so it picks up the skill, then just ask:');
  console.log('  "make a studybook unit for <your material>"');
  console.log('  "add a study page to my studybook"');
  console.log('');
  console.log('Sample to copy from: https://1l3oth.github.io/studybook/  (feed: /feed.xml)');
}

main();
