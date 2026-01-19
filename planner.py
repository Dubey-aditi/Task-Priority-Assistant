from energy_classifier import classify_energy


def prioritize_tasks(tasks):
    """Simple prioritization: you can expand this with deadlines, importance, etc."""
    return tasks


def group_by_energy(tasks):
    """Group tasks by energy level and include classification details."""
    grouped = {"low": [], "medium": [], "high": []}
    task_details = []

    for task in tasks:
        classification = classify_energy(task)
        # Normalize energy key to lowercase for grouping
        energy = classification["energy"].lower()
        grouped[energy].append(
            {
                "task": task,
                "energy": classification["energy"],
                "position": classification["position"],
                "reason": classification["reason"],
            }
        )
        task_details.append(classification)

    return grouped, task_details


def sort_by_position(tasks_with_details):
    """Sort tasks within each energy group by suggested position."""
    position_order = {"FIRST": 0, "MIDDLE": 1, "LAST": 2}
    return sorted(
        tasks_with_details, key=lambda x: position_order.get(x["position"], 1)
    )


def create_day_plan(tasks):
    """Create a day plan with energy-based grouping and smart ordering."""
    prioritized = prioritize_tasks(tasks)
    grouped, task_details = group_by_energy(prioritized)

    # Flatten all tasks with details into a single list
    all_tasks = []
    for energy_level in ["low", "medium", "high"]:
        all_tasks.extend(grouped[energy_level])

    # Sort by suggested position: FIRST, SECOND, THIRD, MIDDLE, LATE, LAST, etc.
    position_order = {
        "FIRST": 0,
        "SECOND": 1,
        "THIRD": 2,
        "MIDDLE": 3,
        "LATE": 4,
        "LAST": 5,
    }

    def get_position_order(pos):
        return position_order.get(pos, 99)

    all_tasks_sorted = sorted(
        all_tasks, key=lambda x: get_position_order(x["position"])
    )

    # Prepare table rows
    table = []
    for task in all_tasks_sorted:
        table.append(
            {
                "Task": task["task"],
                "Energy": task.get("energy", ""),
                "Suggested position": task.get("position", ""),
                "Why": task.get("reason", ""),
            }
        )
    return table
