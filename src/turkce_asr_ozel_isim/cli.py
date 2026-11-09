"""Command line tool for Whisper / WhisperX JSON files with word timestamps."""
import argparse
import json
import sys

from .core import Lexicon, apply_candidates, find_candidates, select_candidates


def load_words(data):
    """Flatten segments so a name split across two segments is still found."""
    words = []
    for index, segment in enumerate(data["segments"]):
        for word in segment.get("words") or []:
            if word.get("start") is not None and word.get("end") is not None:
                words.append({**word, "_segment": index})
    return words


def rebuild(data, words):
    out = {**data, "segments": [dict(s) for s in data["segments"]]}
    grouped = {}
    for word in words:
        word = dict(word)
        grouped.setdefault(word.pop("_segment"), []).append(word)
    for index, segment in enumerate(out["segments"]):
        if index in grouped:
            segment["words"] = grouped[index]
            segment["text"] = " ".join(w["word"].strip() for w in grouped[index])
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(prog="turkce-asr-ozel-isim", description=__doc__)
    parser.add_argument("input", help="JSON with segments[].words[].word/start/end")
    parser.add_argument("-o", "--output", help="write the corrected JSON here")
    parser.add_argument("--selector", choices=("none", "all", "claude"), default="none",
                        help="none: only list candidates; all: accept every candidate; "
                             "claude: let the Claude API choose")
    parser.add_argument("--lexicon", help="your own lexicon JSON instead of the bundled one")
    args = parser.parse_args(argv)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    clips = {"transcript": load_words(data)}
    lexicon = Lexicon.from_file(args.lexicon) if args.lexicon else Lexicon.default()
    candidates = find_candidates(clips, lexicon)
    if args.selector == "claude":
        from .claude import claude_selector
        accepted = select_candidates(candidates, claude_selector()) if candidates else set()
    elif args.selector == "all":
        accepted = {c["number"] for c in candidates}
    else:
        accepted = set()
    for c in candidates:
        mark = "+" if c["number"] in accepted else " "
        print(f"{mark} {c['old']} -> {' '.join(c['new'])}  [{c['kind']}]  {c['context']}")
    print(f"{len(candidates)} candidates, {len(accepted)} applied", file=sys.stderr)
    if args.output:
        fixed = apply_candidates(clips, [c for c in candidates if c["number"] in accepted])
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(rebuild(data, fixed["transcript"]), f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
