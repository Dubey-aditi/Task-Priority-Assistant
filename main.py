from agent import SuperAssistantAgent


def main():
    todo_list = [
        "Order medication",
        "Calendar design updates",
        "Humana PDF parsing using claude agent skills",
        "Fix sources issues where stale manual date got reverted",
        "Leetcode medium Question",
        "Plan Calendar launch next steps",
        "Singing practice",
        "Python basics revision",
        "Order groceries",
        "Messages replies",
    ]
    agent = SuperAssistantAgent()
    table = agent.organize_day(todo_list)
    print(table)
    # Save as a markdown table in a .md file
    if table:
        headers = ["Task", "Energy", "Suggested position", "Why"]
        md_lines = []
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")
        for row in table:
            md_lines.append(
                f"| {row['Task']} | {row['Energy']} | {row['Suggested position']} | {row['Why']} |"
            )
        with open("task_table.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print("Saved table as task_table.md")


if __name__ == "__main__":
    main()
