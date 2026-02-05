import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard" / "leaderboard.md"
HTML_PATH = ROOT / "docs" / "leaderboard.html"  # Assuming you want it in docs/

def read_rows():
    if not CSV_PATH.exists():
        return []
    
    with CSV_PATH.open("r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        
        f.seek(0)
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            row = {
                'team': r.get('team', '').strip(),
                'model': r.get('model', '').strip(),
                'score': r.get('score', '').strip(),
                'timestamp_utc': r.get('timestamp_utc', '').strip() or r.get('timestamp', '').strip(),
                'notes': r.get('notes', '').strip()
            }
            if row['team']:
                rows.append(row)
        return rows

def generate_html_table(rows):
    """Generate just the table HTML for the existing page"""
    if not rows:
        return '<tbody><tr><td colspan="6" style="text-align:center;padding:20px;">No submissions yet.</td></tr></tbody>'
    
    html = []
    html.append('<tbody>')
    for i, r in enumerate(rows, start=1):
        team = r.get("team", "").strip()
        model = r.get("model", "").strip()
        score = r.get("score", "").strip()
        ts = r.get("timestamp_utc", "").strip()
        notes = r.get("notes", "").strip()
        
        # Format timestamp
        try:
            ts_display = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        except:
            ts_display = ts
        
        html.append(f'''
        <tr>
            <td class="rank" data-key="rank">{i}</td>
            <td data-key="team">{team}</td>
            <td data-key="model">{model}</td>
            <td class="score" data-key="score">{score}</td>
            <td data-key="timestamp_utc">{ts_display}</td>
            <td data-key="notes">{notes}</td>
        </tr>''')
    html.append('</tbody>')
    return '\n'.join(html)

def generate_full_html(rows):
    """Generate a complete HTML page"""
    table_html = generate_html_table(rows)
    
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Leaderboard</title>
  <link rel="stylesheet" href="leaderboard.css" />
</head>
<body>
  <header class="wrap">
    <div class="title-row">
      <h1>Leaderboard</h1>
      <p class="sub">Search, filter, and compare submissions. Scores are computed on the hidden test set by the official evaluator.</p>
    </div>
  </header>

  <main class="wrap">
    <section class="controls card">
      <div class="control">
        <label for="search">Search</label>
        <input id="search" type="search" placeholder="Search team, model, notes…" />
      </div>

      <div class="control">
        <label for="modelFilter">Model</label>
        <select id="modelFilter">
          <option value="all">All</option>
        </select>
      </div>

      <div class="control">
        <label for="dateFilter">Date</label>
        <select id="dateFilter">
          <option value="all">All</option>
          <option value="last30">Last 30 days</option>
          <option value="last180">Last 180 days</option>
        </select>
      </div>

      <div class="control">
        <label>Columns</label>
        <div class="checks" id="columnToggles"></div>
      </div>
    </section>

    <section class="card">
      <div class="table-wrap">
        <table id="tbl">
          <thead>
            <tr>
              <th data-key="rank" data-sort="number">Rank</th>
              <th data-key="team" data-sort="string">Team</th>
              <th data-key="model" data-sort="string">Model</th>
              <th data-key="score" data-sort="number">Score</th>
              <th data-key="timestamp_utc" data-sort="string">Date (UTC)</th>
              <th data-key="notes" data-sort="string">Notes</th>
            </tr>
          </thead>
          {table_html}
        </table>
      </div>
      <div class="foot">
        <span id="status">Loading leaderboard…</span>
      </div>
    </section>
  </main>

  <script src="leaderboard.js"></script>
</body>
</html>'''

def main():
    rows = read_rows()
    
    # Sort rows
    def score_key(r):
        try:
            return float(r.get("score", "-inf"))
        except:
            return float("-inf")
    
    def ts_key(r):
        ts_str = r.get("timestamp_utc", "")
        try:
            ts_str = ts_str.replace("Z", "+00:00")
            return datetime.fromisoformat(ts_str)
        except:
            return datetime.fromtimestamp(0)
    
    rows.sort(key=lambda r: (score_key(r), ts_key(r)), reverse=True)

    # 1. Update markdown
    lines = []
    lines.append("# Leaderboard\n")
    lines.append("This leaderboard is **auto-updated** when a submission PR is merged.\n\n")
    
    lines.append("| Rank | Team | Model | Score | Date (UTC) | Notes |\n")
    lines.append("|---:|---|---|---:|---|---|\n")
    
    for i, r in enumerate(rows, start=1):
        team = r.get("team", "").strip()
        model = r.get("model", "").strip()
        score = r.get("score", "").strip()
        ts = r.get("timestamp_utc", "").strip()
        notes = r.get("notes", "").strip()
        
        model_disp = f"`{model}`" if model else ""
        
        try:
            ts_display = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        except:
            ts_display = ts
        
        lines.append(f"| {i} | {team} | {model_disp} | {score} | {ts_display} | {notes} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")
    
    # 2. Update HTML (if you want static HTML)
    # Make sure docs directory exists
    HTML_PATH.parent.mkdir(exist_ok=True)
    
    # Option A: Generate full HTML page
    full_html = generate_full_html(rows)
    HTML_PATH.write_text(full_html, encoding="utf-8")
    
    # Option B: Just copy your existing HTML (if you want to keep JS functionality)
    # shutil.copy("path/to/your/existing.html", HTML_PATH)
    
    print(f"Updated leaderboard.md and leaderboard.html with {len(rows)} entries")

if __name__ == "__main__":
    main()