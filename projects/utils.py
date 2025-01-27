from collections import defaultdict, deque
from datetime import timedelta

def topological_sort(tasks):
    """Sort tasks using Kahn's Algorithm."""
    indegree = {task.id: 0 for task in tasks}
    graph = defaultdict(list)

    # Build the graph
    for task in tasks:
        for dep in task.dependencies.all():
            graph[dep.id].append(task.id)
            indegree[task.id] += 1

    # Perform topological sort
    sorted_tasks = []
    queue = deque([task.id for task in tasks if indegree[task.id] == 0])

    while queue:
        current = queue.popleft()
        sorted_tasks.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_tasks) != len(tasks):
        raise ValueError("Cyclic dependency detected!")
    return sorted_tasks

def calculate_schedule(tasks, collaborators):
    """
    Calculate a schedule based on task durations and dependencies.
    """
    # Group tasks by collaborators
    user_tasks = defaultdict(list)
    for task in tasks:
        user_tasks[task.assigned_to.id].append(task)

    # Sort tasks for each user by topological order
    schedules = {}
    for user, tasks in user_tasks.items():
        sorted_task_ids = topological_sort(tasks)
        start_date = None
        schedules[user] = []
        for task_id in sorted_task_ids:
            task = next(t for t in tasks if t.id == task_id)
            if not start_date:
                start_date = task.start_date or timedelta(days=0)
            else:
                start_date += timedelta(days=1)  # Sequential scheduling
            task.start_date = start_date
            task.end_date = start_date + timedelta(days=task.duration_days)
            schedules[user].append(task)
    return schedules
