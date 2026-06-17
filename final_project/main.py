"""
Final project implementation.
"""

# pylint: disable=unused-import
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from lab_6_pipeline.pipeline import UDPipeAnalyzer


def main(corpus_path: Path, dist_path: Path) -> None:
    """
    Generate conllu file for provided corpus of texts.

    Args:
        corpus_path (Path): Path to folder containing text files.
        dist_path (Path): Path to folder for saving auto_annotated.conllu.
    """
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus folder not found: {corpus_path}")

    txt_files = list(corpus_path.glob("*_raw.txt"))
    if not txt_files:
        raise ValueError(f"No .txt files found in: {corpus_path}")

    dist_path.mkdir(parents=True, exist_ok=True)

    merged_file = dist_path / "merged_corpus.txt"
    with open(merged_file, 'w', encoding='utf-8') as out_f:
        for txt_file in sorted(txt_files):
            with open(txt_file, 'r', encoding='utf-8') as in_f:
                out_f.write(in_f.read())
                out_f.write('\n\n')

    analyzer = UDPipeAnalyzer(language="russian")
    result = analyzer.analyze(merged_file)

    if not result:
        raise ValueError("UDPipeAnalyzer.analyze() returned empty result")

    output_file = dist_path / "auto_annotated.conllu"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
        if not result.endswith('\n'):
            f.write('\n')


if __name__ == "__main__":
    main(Path(__file__).parent / "assets" / "articles", Path(__file__).parent / "dist")
