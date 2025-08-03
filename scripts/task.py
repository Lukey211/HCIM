from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Requirement:
    """Represents a single requirement for a task."""
    # e.g., 'skill', 'quest', 'item'
    type: str
    # e.g., 'attack', 'Cook's Assistant', 'Pot of flour'
    name: str
    # e.g., 5 (for level), 1 (for quest completion), 1 (for item quantity)
    quantity: int

@dataclass
class Task:
    """Represents a single, atomic action in the game."""
    task_id: int
    name: str
    # e.g., 'QUEST_STEP', 'SKILLING', 'ITEM_GATHER'
    task_type: str
    # A list of Requirement objects needed to start this task
    requirements: List[Requirement] = field(default_factory=list)
    # The world coordinates for the task
    location: Dict[str, int] = field(default_factory=dict)
    # Optional: A link back to the parent quest or activity
    parent_activity: Optional[str] = None