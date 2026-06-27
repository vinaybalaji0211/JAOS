from logs.logger import logger


class GoalConflictResolver:

    @staticmethod
    def detect_conflict(goal_a, goal_b):
        conflicts = []

        if goal_a.get("resource") == goal_b.get("resource"):
            conflicts.append(
                f"Resource conflict: both need {goal_a.get('resource')}"
            )

        if goal_a.get("focus_required") and goal_b.get("interrupts_focus"):
            conflicts.append(
                "Focus conflict: one goal interrupts focused work"
            )

        if goal_a.get("priority") != goal_b.get("priority"):
            conflicts.append(
                "Priority conflict: goals have different priorities"
            )

        logger.info("Goal conflict check completed.")

        return conflicts

    @staticmethod
    def show_conflicts(goal_a, goal_b):
        conflicts = GoalConflictResolver.detect_conflict(
            goal_a,
            goal_b
        )

        print("\nGoal Conflict Resolver:\n")

        if not conflicts:
            print("No conflicts detected.")
            return

        for index, conflict in enumerate(conflicts, start=1):
            print(f"{index}. {conflict}")