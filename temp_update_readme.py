from pathlib import Path
p = Path(r'c:\Users\hp\OneDrive\Desktop\ipl project\README.md')
text = p.read_text(encoding='utf-16')
old = "## What you can explore in the dashboard\n\n- Overview of completed matches and team performance\n- Player stats such as top run scorers and wicket takers\n- Venue analysis\n- Trends such as toss decisions and run patterns\n\n## Notes\n"
new = "## What you can explore in the dashboard\n\n- Overview of completed matches and team performance\n- Player stats such as top run scorers and wicket takers\n- Venue analysis\n- Trends such as toss decisions and run patterns\n- Season-aware filters so teams and venues update based on the selected seasons\n- Simple guidance messages when filters return no data or when the app needs a better selection\n- Clear explanations for run-over charts and estimated total runs\n\n## Notes\n"
if old not in text:
    raise SystemExit('Target block not found in README.md')
p.write_text(text.replace(old, new), encoding='utf-16')
print('updated')
