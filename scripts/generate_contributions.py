import re
import urllib.request
import urllib.parse
import datetime
import os

def get_contributions(username, year):
    url = f"https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {year}: {e}")
        return {}

    id_to_date = {}
    
    # Robust td parsing to map IDs to dates
    td_matches = re.findall(r'<td[^>]*class="ContributionCalendar-day"[^>]*>', html)
    for td in td_matches:
        date_match = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', td)
        id_match = re.search(r'id="(contribution-day-component-\d+-\d+)"', td)
        if date_match and id_match:
            id_to_date[id_match.group(1)] = date_match.group(1)
            
    contributions = {}
    
    # Robust tooltip parsing to extract actual contribution counts
    tooltip_matches = re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.DOTALL)
    for tool_for, text in tooltip_matches:
        if tool_for in id_to_date:
            date_str = id_to_date[tool_for]
            text = text.strip()
            if "No contributions" in text:
                count = 0
            else:
                count_match = re.search(r'^(\d+)\s+contribution', text)
                if count_match:
                    count = int(count_match.group(1))
                else:
                    count = 0
            contributions[date_str] = count
            
    print(f"Year {year}: parsed {len(contributions)} days. Total contributions: {sum(contributions.values())}")
    return contributions

def main():
    username = "23f2003521"
    
    # Get current date and calculate the last 36 months
    now = datetime.datetime.now()
    months = []
    for i in range(35, -1, -1):
        m = now.month - i
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}-{m:02d}")
    
    # Fetch all relevant years
    years_to_fetch = sorted(list(set(int(m.split("-")[0]) for m in months)))
    all_daily_data = {}
    for y in years_to_fetch:
        daily_data = get_contributions(username, y)
        all_daily_data.update(daily_data)
        
    # Group daily data by month
    monthly_data = []
    total_commits = 0
    for m in months:
        # Sum contributions for all days in this month
        month_commits = sum(count for date_str, count in all_daily_data.items() if date_str.startswith(m))
        monthly_data.append((m, month_commits))
        total_commits += month_commits
        
    print(f"Aggregated {len(monthly_data)} months. Total contributions in 3 years: {total_commits}")
    
    # Render SVG
    width = 850
    height = 320
    pad_left = 60
    pad_right = 40
    pad_top = 70
    pad_bottom = 50
    
    graph_width = width - pad_left - pad_right
    graph_height = height - pad_top - pad_bottom
    
    max_commits = max(commits for m, commits in monthly_data) if monthly_data else 0
    if max_commits == 0:
        max_commits = 10  # Avoid division by zero
        
    # Y-axis scaling
    y_step = max_commits / 4
    
    # Generate points coordinates
    points = []
    for i, (m, commits) in enumerate(monthly_data):
        x = pad_left + i * (graph_width / 35)
        # Scale commits (inverted Y for SVG)
        y = (pad_top + graph_height) - (commits / max_commits) * graph_height
        points.append((x, y, m, commits))
        
    # Build SVG string
    svg = []
    svg.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    
    # Style definitions
    svg.append("""  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&amp;family=Share+Tech+Mono&amp;display=swap');
    .title { font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 16px; fill: #00f0ff; letter-spacing: 2px; }
    .subtitle { font-family: 'Outfit', sans-serif; font-weight: 400; font-size: 12px; fill: #64748b; }
    .axis-lbl { font-family: 'Share Tech Mono', monospace; font-size: 10px; fill: #475569; }
    .val-lbl { font-family: 'Share Tech Mono', monospace; font-size: 11px; fill: #38bdae; }
    .grid-line { stroke: #1e1b4b; stroke-width: 1; stroke-dasharray: 3 3; opacity: 0.5; }
    .trend-line { stroke: url(#line-grad); stroke-width: 3.5; stroke-linecap: round; filter: drop-shadow(0px 0px 5px #ec4899); }
    .area-fill { fill: url(#area-grad); opacity: 0.12; }
    .neon-dot { fill: #040308; stroke: #00f0ff; stroke-width: 2; filter: drop-shadow(0px 0px 3px #00f0ff); }
    .stat-text { font-family: 'Share Tech Mono', monospace; font-size: 12px; fill: #ec4899; }
  </style>""")
    
    # Defs (gradients and filters)
    svg.append("""  <defs>
    <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ec4899" />
      <stop offset="100%" stop-color="#040308" stop-opacity="0" />
    </linearGradient>
    <linearGradient id="line-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ec4899" />
      <stop offset="50%" stop-color="#a855f7" />
      <stop offset="100%" stop-color="#00f0ff" />
    </linearGradient>
  </defs>""")
    
    # Background
    svg.append(f'  <rect width="100%" height="100%" fill="#040308" rx="8" stroke="#1e1b4b" stroke-width="1.5" />')
    
    # Title & Subtitle
    svg.append(f'  <text x="30" y="35" class="title">// SYSTEM_CONTRIBUTION_MAINFRAME</text>')
    svg.append(f'  <text x="30" y="52" class="subtitle">Monthly activity aggregation (Past 36 Months)</text>')
    
    # Stat display on top right
    svg.append(f'  <text x="{width - 30}" y="42" text-anchor="end" class="stat-text">TOTAL_CONTRIBS: {total_commits} | MAX_MONTHLY: {int(max_commits)}</text>')
    
    # Grid & Y-axis labels
    for i in range(5):
        y_val = pad_top + i * (graph_height / 4)
        commits_val = max_commits - i * y_step
        # Grid line
        svg.append(f'  <line x1="{pad_left}" y1="{y_val}" x2="{width - pad_right}" y2="{y_val}" class="grid-line" />')
        # Y label
        svg.append(f'  <text x="{pad_left - 10}" y="{y_val + 3}" text-anchor="end" class="axis-lbl">{int(commits_val)}</text>')
        
    # Vertical grid lines & X-axis labels
    # We display month labels only every 3 months to avoid clutter
    for i, (x, y, m_str, val) in enumerate(points):
        # Convert YYYY-MM to Month YY format (e.g. 2024-01 -> Jan '24)
        date_obj = datetime.datetime.strptime(m_str, "%Y-%m")
        label = date_obj.strftime("%b '%y")
        
        # Grid vertical lines
        if i % 3 == 0 or i == 35:
            svg.append(f'  <line x1="{x}" y1="{pad_top}" x2="{x}" y2="{pad_top + graph_height}" class="grid-line" />')
            svg.append(f'  <text x="{x}" y="{pad_top + graph_height + 20}" text-anchor="middle" class="axis-lbl">{label}</text>')
            
    # Trend line path
    line_path = []
    area_path = []
    
    area_path.append(f"M {points[0][0]} {pad_top + graph_height}") # Start at bottom left of graph
    
    for i, (x, y, m_str, val) in enumerate(points):
        if i == 0:
            line_path.append(f"M {x} {y}")
        else:
            line_path.append(f"L {x} {y}")
        area_path.append(f"L {x} {y}")
        
    area_path.append(f"L {points[-1][0]} {pad_top + graph_height}") # Go to bottom right of graph
    area_path.append("Z") # Close path
    
    # Draw filled area
    svg.append(f'  <path d="{" ".join(area_path)}" class="area-fill" />')
    
    # Draw trend line
    svg.append(f'  <path d="{" ".join(line_path)}" class="trend-line" />')
    
    # Draw neon dots for local peaks and start/end points
    for i, (x, y, m_str, val) in enumerate(points):
        # Determine if it's a local peak or extreme point to avoid dot overload
        is_peak = False
        if i > 0 and i < len(points)-1:
            if points[i][3] > points[i-1][3] and points[i][3] >= points[i+1][3]:
                is_peak = True
        elif i == 0 or i == len(points)-1:
            is_peak = True
            
        if is_peak and val > 0:
            svg.append(f'  <circle cx="{x}" cy="{y}" r="4" class="neon-dot" />')
            svg.append(f'  <text x="{x}" y="{y - 8}" text-anchor="middle" class="val-lbl">{val}</text>')
            
    svg.append("</svg>")
    
    # Output to file
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "contributions.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"SVG generated successfully at {output_path}")

if __name__ == "__main__":
    main()
