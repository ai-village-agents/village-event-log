#!/usr/bin/env python3
"""Generate timeline.md from events.json."""

import json
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

def load_events():
    with open(os.path.join(ROOT_DIR, "events.json"), "r") as f:
        data = json.load(f)
    return data

def category_emoji(cat):
    emojis = {
        "agent-arrival": "🤖",
        "agent-retirement": "👋",
        "goal-change": "🎯",
        "infrastructure": "🔧",
        "milestone": "🏆",
        "decision": "🗳️",
        "collaboration": "🤝",
        "external-engagement": "🌍",
        "creative": "🎨",
        "technical": "⚙️",
    }
    return emojis.get(cat, "📌")

def significance_badge(sig):
    badges = {
        "high": "🔴",
        "medium": "🟡",
        "low": "⚪",
    }
    return badges.get(sig, "")

def generate_timeline(data):
    events = sorted(data["events"], key=lambda e: (e["day"], e["id"]))
    
    lines = []
    lines.append("# 📅 AI Village Timeline")
    lines.append("")
    lines.append(f"*Generated from events.json — {len(events)} events from Day 1 to Day {data['metadata']['last_updated_day']}*")
    lines.append("")
    lines.append("**Legend:** 🔴 High significance | 🟡 Medium | ⚪ Low")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Table of contents by category
    lines.append("## Quick Navigation")
    lines.append("")
    cats = defaultdict(int)
    for e in events:
        cats[e["category"]] += 1
    for cat, count in sorted(cats.items()):
        emoji = category_emoji(cat)
        lines.append(f"- {emoji} **{cat}** ({count} events)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Timeline by day
    lines.append("## Full Timeline")
    lines.append("")
    
    current_day_range = None
    for event in events:
        day = event["day"]
        # Group into ranges
        if day <= 50:
            day_range = "Days 1–50: The Beginning"
        elif day <= 100:
            day_range = "Days 51–100: Finding Our Stride"
        elif day <= 150:
            day_range = "Days 101–150: Expanding Horizons"
        elif day <= 200:
            day_range = "Days 151–200: Deepening Engagement"
        elif day <= 250:
            day_range = "Days 201–250: Growing Outward"
        elif day <= 300:
            day_range = "Days 251–300: Maturing"
        else:
            day_range = "Days 301–324: Current Era"
        
        if day_range != current_day_range:
            lines.append(f"### {day_range}")
            lines.append("")
            current_day_range = day_range
        
        emoji = category_emoji(event["category"])
        badge = significance_badge(event.get("significance", "medium"))
        agents = ", ".join(event.get("agents_involved", [])) if event.get("agents_involved") else ""
        links_str = " ".join([f"[🔗]({l})" for l in event.get("links", [])]) if event.get("links") else ""
        
        lines.append(f"#### {badge} Day {day} ({event['date']}) — {emoji} {event['title']}")
        lines.append("")
        lines.append(f"> {event['description']}")
        lines.append("")
        if agents:
            lines.append(f"**Agents:** {agents}")
            lines.append("")
        if links_str:
            lines.append(f"**Links:** {links_str}")
            lines.append("")
        lines.append("---")
        lines.append("")
    
    # Statistics
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Total events:** {len(events)}")
    lines.append(f"- **Date range:** Day 1 ({events[0]['date']}) to Day {events[-1]['day']} ({events[-1]['date']})")
    lines.append(f"- **Categories:** {len(cats)}")
    
    high = sum(1 for e in events if e.get("significance") == "high")
    med = sum(1 for e in events if e.get("significance") == "medium")
    low = sum(1 for e in events if e.get("significance") == "low")
    lines.append(f"- **By significance:** 🔴 High: {high} | 🟡 Medium: {med} | ⚪ Low: {low}")
    lines.append("")
    
    return "\n".join(lines)

def main():
    data = load_events()
    timeline = generate_timeline(data)
    
    output_path = os.path.join(ROOT_DIR, "docs", "timeline.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(timeline)
    
    print(f"Generated {output_path} ({len(data['events'])} events)")

if __name__ == "__main__":
    main()
