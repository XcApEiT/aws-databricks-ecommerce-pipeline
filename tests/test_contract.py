from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

def test_nine_expected_csvs():
    tree = ast.parse((ROOT / "scripts/profile_olist.py").read_text())
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "EXPECTED" for t in n.targets))
    assert len(ast.literal_eval(node.value)) == 9

def test_raw_data_excluded_from_git():
    ignore = (ROOT / ".gitignore").read_text()
    assert "data/" in ignore and "*.csv" in ignore
