#!/usr/bin/env -S npx tsx
/**
 * Generate the three outer .mod files in the user's CK3 mod directory.
 *
 * Each outer .mod file is the in-folder descriptor.mod plus a
 * `path="<absolute repo path to mod>"` line, which is how the Paradox
 * Launcher discovers mods sourced from outside its mod folder.
 *
 * Usage (from the repo root):
 *   bun .scripts/install-mods.ts                 # default Documents path
 *   bun .scripts/install-mods.ts /custom/path    # override target dir
 *   npx tsx .scripts/install-mods.ts             # if you don't have bun
 */

import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";

const MODS = ["the-crimson-bath", "eclectic-traditions", "vigil-at-the-holy-site"] as const;

const REPO_ROOT = path.resolve(__dirname, "..");

function defaultTargetDir(): string {
	const docs = path.join(
		os.homedir(),
		"Documents",
		"Paradox Interactive",
		"Crusader Kings III",
		"mod",
	);
	return docs;
}

function toForwardSlashes(p: string): string {
	return p.replaceAll(path.sep, "/");
}

function outerModName(mod: string): string {
	return `${mod.replaceAll("-", "_")}.mod`;
}

function buildOuterModContent(mod: string): string {
	const descriptorPath = path.join(REPO_ROOT, mod, "descriptor.mod");
	const descriptor = fs.readFileSync(descriptorPath, "utf8").trimEnd();
	const repoPath = toForwardSlashes(path.join(REPO_ROOT, mod));
	return `${descriptor}\npath="${repoPath}"\n`;
}

function main(): void {
	const target = process.argv[2] ?? defaultTargetDir();

	if (!fs.existsSync(target)) {
		console.error(`Target mod folder does not exist: ${target}`);
		console.error("Pass a different path as the first argument, or create it first.");
		process.exit(1);
	}

	for (const mod of MODS) {
		const descriptorPath = path.join(REPO_ROOT, mod, "descriptor.mod");
		if (!fs.existsSync(descriptorPath)) {
			console.error(`Missing ${descriptorPath} — skipping ${mod}`);
			continue;
		}
		const outerPath = path.join(target, outerModName(mod));
		fs.writeFileSync(outerPath, buildOuterModContent(mod));
		console.log(`Wrote ${outerPath}`);
	}
}

main();
