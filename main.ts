// News-image entry for make.fun news-image-20261120 (Node 22, stdlib only).
// The image is drawn by draw.py and shipped in this repository as
// entry.png; this program copies it to the grader's output directory.
// It does no network access and writes the same bytes on every run.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

// The image sums up Friday 20 November 2026: the Shenzhen summit of
// Trump, Xi and Putin; Russia's mass strike on Kyiv spilling into
// Poland; the ICJ genocide ruling on Myanmar; a tanker ablaze in the
// Strait of Hormuz; COP31 stalling in Antalya; and the S&P 500's
// 3.7% slide into correction. It is copied byte for byte, so the
// program is deterministic: two runs write identical files.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
