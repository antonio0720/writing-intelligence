// Minimal, dependency-free YAML reader — enough to parse agents/agent_manifest.yaml into JSON.
// Handles: block mappings, block sequences (of scalars and of maps), flow sequences [a, b],
// quoted + bare scalars, booleans, numbers, and the `---` document marker. Not a general
// YAML engine — it covers the manifest's shape and is exercised by the manifest test.
import { readFileSync } from "node:fs";
import { repoPath } from "../paths";

interface Line {
  indent: number;
  text: string;
}

export type YamlValue = string | number | boolean | null | YamlValue[] | { [k: string]: YamlValue };

function toLines(src: string): Line[] {
  const out: Line[] = [];
  for (const raw of src.split(/\r?\n/)) {
    if (raw.trim() === "" || raw.trim() === "---") continue;
    if (/^\s*#/.test(raw)) continue;
    const indent = raw.length - raw.replace(/^\s+/, "").length;
    out.push({ indent, text: stripComment(raw.trim()) });
  }
  return out;
}

// Strip a trailing ` #comment` that is not inside quotes.
function stripComment(s: string): string {
  let inSingle = false, inDouble = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === "'" && !inDouble) inSingle = !inSingle;
    else if (c === '"' && !inSingle) inDouble = !inDouble;
    else if (c === "#" && !inSingle && !inDouble && (i === 0 || s[i - 1] === " ")) {
      return s.slice(0, i).trim();
    }
  }
  return s;
}

export function parseYaml(src: string): YamlValue {
  const lines = toLines(src);
  const [value] = parseBlock(lines, 0, lines.length, lines[0]?.indent ?? 0);
  return value;
}

function parseBlock(lines: Line[], start: number, end: number, indent: number): [YamlValue, number] {
  if (start >= end) return [null, start];
  if (lines[start].text.startsWith("- ")) return parseSequence(lines, start, end, indent);
  return parseMapping(lines, start, end, indent);
}

function parseSequence(lines: Line[], start: number, end: number, indent: number): [YamlValue[], number] {
  const items: YamlValue[] = [];
  let i = start;
  while (i < end && lines[i].indent === indent && lines[i].text.startsWith("- ")) {
    const rest = lines[i].text.slice(2).trim();
    // Find where this item's nested block ends (deeper-indented following lines).
    let j = i + 1;
    while (j < end && lines[j].indent > indent) j++;
    if (rest.includes(":") && !isQuoted(rest)) {
      // Item is a map whose first key is inline. Rebuild a virtual sub-block.
      const virtual: Line[] = [{ indent: indent + 2, text: rest }, ...lines.slice(i + 1, j)];
      const [val] = parseMapping(virtual, 0, virtual.length, indent + 2);
      items.push(val);
    } else if (j > i + 1) {
      const [val] = parseBlock(lines, i + 1, j, lines[i + 1].indent);
      items.push(val);
    } else {
      items.push(scalar(rest));
    }
    i = j;
  }
  return [items, i];
}

function parseMapping(lines: Line[], start: number, end: number, indent: number): [{ [k: string]: YamlValue }, number] {
  const map: { [k: string]: YamlValue } = {};
  let i = start;
  while (i < end && lines[i].indent === indent && !lines[i].text.startsWith("- ")) {
    const line = lines[i].text;
    const colon = splitKey(line);
    if (!colon) { i++; continue; }
    const [key, inlineRaw] = colon;
    const inline = inlineRaw.trim();
    // Find this key's nested block extent.
    let j = i + 1;
    while (j < end && lines[j].indent > indent) j++;
    if (inline === "") {
      if (j > i + 1) {
        const [val] = parseBlock(lines, i + 1, j, lines[i + 1].indent);
        map[key] = val;
      } else {
        map[key] = null;
      }
    } else {
      map[key] = scalar(inline);
    }
    i = j;
  }
  return [map, i];
}

// Split "key: value" respecting quotes; returns null if no top-level colon.
function splitKey(line: string): [string, string] | null {
  let inSingle = false, inDouble = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === "'" && !inDouble) inSingle = !inSingle;
    else if (c === '"' && !inSingle) inDouble = !inDouble;
    else if (c === ":" && !inSingle && !inDouble && (i + 1 >= line.length || line[i + 1] === " ")) {
      return [unquote(line.slice(0, i).trim()), line.slice(i + 1)];
    }
  }
  return null;
}

function isQuoted(s: string): boolean {
  return (s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"));
}

function unquote(s: string): string {
  if (isQuoted(s)) return s.slice(1, -1);
  return s;
}

function scalar(raw: string): YamlValue {
  const s = raw.trim();
  if (s.startsWith("[") && s.endsWith("]")) {
    const inner = s.slice(1, -1).trim();
    if (inner === "") return [];
    return inner.split(",").map((x) => scalar(x.trim()));
  }
  if (isQuoted(s)) return unquote(s);
  if (s === "true") return true;
  if (s === "false") return false;
  if (s === "null" || s === "~") return null;
  if (/^-?\d+$/.test(s)) return Number(s);
  if (/^-?\d+\.\d+$/.test(s)) return Number(s);
  return s;
}

let cached: YamlValue | null = null;
export function loadManifest(): YamlValue {
  if (cached) return cached;
  const text = readFileSync(repoPath("agents", "agent_manifest.yaml"), "utf8");
  cached = parseYaml(text);
  return cached;
}
