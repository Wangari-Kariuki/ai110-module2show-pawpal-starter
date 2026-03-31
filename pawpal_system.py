from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional


@dataclass
class Pet:
    """Represents a pet with care tracking"""
    name: str
    pet_id: str
    age: int
    med_info: str
    physical_attributes: Dict = field(default_factory=dict)
    last_fed: Optional[datetime] = None
    last_groomed: Optional[datetime] = None
    last_vet_visit: Optional[datetime] = None
    care_history: List[Dict] = field(default_factory=list)
    required_tasks: List['CareTask'] = field(default_factory=list)  # Tasks this pet needs
    
    def treatment(self, treatment_type: str) -> None:
        """Record a treatment for the pet"""
        treatment_record = {
            "activity": "treatment",
            "treatment_type": treatment_type,
            "timestamp": datetime.now(),
            "pet_id": self.pet_id
        }
        self.care_history.append(treatment_record)
        self.last_vet_visit = datetime.now()
    
    def grooming(self) -> None:
        """Record grooming activity"""
        grooming_record = {
            "activity": "grooming",
            "timestamp": datetime.now(),
            "pet_id": self.pet_id
        }
        self.care_history.append(grooming_record)
        self.last_groomed = datetime.now()
    
    def feed(self) -> None:
        """Record feeding activity"""
        feeding_record = {
            "activity": "feeding",
            "timestamp": datetime.now(),
            "pet_id": self.pet_id
        }
        self.care_history.append(feeding_record)
        self.last_fed = datetime.now()
    
    def get_care_history(self) -> List[Dict]:
        """Retrieve pet's care history"""
        return self.care_history


@dataclass
class CareTask:
    """Represents a specific care task for a pet"""
    task_type: str
    description: str
    priority: int
    frequency: str
    last_completed: Optional[datetime] = None
    owner_preferences: Dict = field(default_factory=dict)
    task_id: str = field(default_factory=str)
    
    def is_completed(self) -> bool:
        """Check if task has been completed"""
        if self.last_completed is None:
            return False
        
        # Calculate how long ago the task was completed
        time_since_completion = datetime.now() - self.last_completed
        
        # Define frequency intervals
        frequency_intervals = {
            "daily": timedelta(days=1),
            "twice daily": timedelta(hours=12),
            "weekly": timedelta(days=7),
            "monthly": timedelta(days=30),
            "every 2 days": timedelta(days=2),
            "every 3 days": timedelta(days=3),
        }
        
        # Get the interval for this task's frequency
        interval = frequency_intervals.get(self.frequency.lower(), timedelta(days=1))
        
        # Task is considered completed if it was done within the interval
        return time_since_completion <= interval
    
    def mark_completed(self) -> None:
        """Mark task as completed"""
        self.last_completed = datetime.now()
    
    def get_next_due_date(self) -> datetime:
        """Calculate next due date based on frequency"""
        if self.last_completed is None:
            # If never completed, due immediately
            return datetime.now()
        
        # Define frequency intervals
        frequency_intervals = {
            "daily": timedelta(days=1),
            "twice daily": timedelta(hours=12),
            "weekly": timedelta(days=7),
            "monthly": timedelta(days=30),
            "every 2 days": timedelta(days=2),
            "every 3 days": timedelta(days=3),
        }
        
        # Get the interval for this task's frequency
        interval = frequency_intervals.get(self.frequency.lower(), timedelta(days=1))
        
        # Next due date is last completed time plus the interval
        next_due = self.last_completed + interval
        
        return next_due


class Constraint:
    """Represents a scheduling constraint"""
    
    def __init__(self, constraint_type: str, value: str, weight: int = 1):
        self.constraint_type = constraint_type
        self.value = value
        self.weight = weight
    
    def evaluate(self, task: CareTask) -> bool:
        """Evaluate if a task meets this constraint"""
        if self.constraint_type == "priority":
            # Constraint met if task priority is >= constraint value
            return task.priority >= int(self.value)
        elif self.constraint_type == "task_type":
            # Constraint met if task type matches
            return task.task_type.lower() == self.value.lower()
        elif self.constraint_type == "owner_preference":
            # Constraint met if owner preference matches task preferences
            return self.value in task.owner_preferences
        elif self.constraint_type == "urgent":
            # Constraint met if task is overdue
            next_due = task.get_next_due_date()
            return datetime.now() >= next_due
        return True
    
    def get_priority(self) -> int:
        """Get the priority weight of this constraint"""
        return self.weight


class DailyPlan:
    """Represents a daily pet care plan"""
    
    def __init__(self, date: str, time_available: int = 24):
        self.date = date
        self.scheduled_tasks: List[CareTask] = []
        self.time_available = time_available
    
    def generate_plan(self) -> None:
        """Generate optimized daily plan"""
        # Clear existing tasks
        self.scheduled_tasks.clear()
        # Note: This will be called by Scheduler with actual pet tasks
        # and constraints to build the plan
    
    def get_tasks_for_day(self) -> List[CareTask]:
        """Get all tasks scheduled for this day"""
        return self.scheduled_tasks
    
    def get_task_by_type(self, task_type: str) -> Optional[CareTask]:
        """Get a specific task by type"""
        for task in self.scheduled_tasks:
            if task.task_type == task_type:
                return task
        return None
    
    def reschedule_task(self, task_id: str, new_time: datetime) -> None:
        """Reschedule a task to a different time"""
        for task in self.scheduled_tasks:
            if task.task_id == task_id:
                # Task rescheduling (in a full implementation, this would store the new time)
                # For now, we just mark it as available for rescheduling
                task.owner_preferences['rescheduled_to'] = new_time
                break


class Scheduler:
    """Handles scheduling logic and optimization  retrieves, organizes and manages tasks acrross pets"""
    
    def __init__(self, optimization_method: str = "greedy"):
        self.constraints: List[Constraint] = []
        self.optimization_method = optimization_method
    
    def schedule_tasks(self, pet: Pet, available_time: int) -> DailyPlan:
        """Create a daily plan for a pet given available time"""
        daily_plan = DailyPlan(datetime.now().strftime("%Y-%m-%d"), available_time)
        # Implementation will go here
        return daily_plan
    
    def optimize_schedule(self, daily_plan: DailyPlan) -> DailyPlan:
        """Optimize an existing schedule"""
        if self.optimization_method == "greedy":
            # Sort tasks by priority (higher priority first)
            daily_plan.scheduled_tasks.sort(key=lambda t: t.priority, reverse=True)
        elif self.optimization_method == "urgent_first":
            # Sort by urgency (tasks that are overdue go first)
            daily_plan.scheduled_tasks.sort(
                key=lambda t: (datetime.now() >= t.get_next_due_date(), t.priority),
                reverse=True
            )
        return daily_plan
    
    def check_conflicts(self, tasks: List[CareTask]) -> bool:
        """Check if tasks have scheduling conflicts"""
        # Check for duplicate task types (can't feed twice at same time)
        task_types = [task.task_type for task in tasks]
        # Conflict exists if same task type appears multiple times for same pet
        return len(task_types) != len(set(task_types))


class Agent:
    """AI agent for pet care guidance and questions"""
    
    def __init__(self, owner: Optional['PetOwner'] = None):
        self.knowledge_base: Dict = {}
        self.owner = owner  # Reference to PetOwner for accessing pet data
    
    def answer_question(self, question: str) -> str:
        """Answer a user's question about pet care"""
        if not self.owner:
            return "No pet owner data available."
        
        question_lower = question.lower()
        
        # Check for pet status questions
        if "been fed" in question_lower or "fed" in question_lower:
            pet_name = self._extract_pet_name(question)
            if pet_name:
                pet = self._find_pet_by_name(pet_name)
                if pet:
                    if pet.last_fed:
                        return f"Yes, {pet.name} was last fed at {pet.last_fed}"
                    else:
                        return f"No, {pet.name} has not been fed yet."
            return "Could not identify which pet you're asking about."
        
        # Check for grooming questions
        elif "groomed" in question_lower or "grooming" in question_lower:
            pet_name = self._extract_pet_name(question)
            if pet_name:
                pet = self._find_pet_by_name(pet_name)
                if pet:
                    if pet.last_groomed:
                        return f"{pet.name} was last groomed at {pet.last_groomed}"
                    else:
                        return f"{pet.name} has not been groomed yet."
            return "Could not identify which pet you're asking about."
        
        # Check for vet questions
        elif "vet" in question_lower or "vet visit" in question_lower:
            pet_name = self._extract_pet_name(question)
            if pet_name:
                pet = self._find_pet_by_name(pet_name)
                if pet:
                    if pet.last_vet_visit:
                        return f"{pet.name}'s last vet visit was at {pet.last_vet_visit}"
                    else:
                        return f"{pet.name} has not had a vet visit recorded yet."
            return "Could not identify which pet you're asking about."
        
        # Default response
        return "I'm here to help with pet care questions. Ask about feeding, grooming, or vet visits."
    
    def suggest_next_task(self) -> Optional[CareTask]:
        """Suggest the next task to perform"""
        if not self.owner or not self.owner.pets_list:
            return None
        
        # Find all tasks across all pets that are overdue
        overdue_tasks = []
        for pet in self.owner.pets_list:
            for task in pet.required_tasks:
                if datetime.now() >= task.get_next_due_date():
                    overdue_tasks.append(task)
        
        if overdue_tasks:
            # Return the highest priority overdue task
            return max(overdue_tasks, key=lambda t: t.priority)
        
        # If no overdue tasks, find next task due soonest
        upcoming_tasks = []
        for pet in self.owner.pets_list:
            upcoming_tasks.extend(pet.required_tasks)
        
        if upcoming_tasks:
            return min(upcoming_tasks, key=lambda t: t.get_next_due_date())
        
        return None
    
    def _extract_pet_name(self, question: str) -> Optional[str]:
        """Extract pet name from question"""
        if not self.owner:
            return None
        # Simple extraction: check if any pet name is in the question
        for pet in self.owner.pets_list:
            if pet.name.lower() in question.lower():
                return pet.name
        return None
    
    def _find_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name"""
        if not self.owner:
            return None
        for pet in self.owner.pets_list:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None
    
    def get_pet_status(self, pet_id: str) -> Dict:
        """Get current status of a pet"""
        if self.owner:
            for pet in self.owner.pets_list:
                if pet.pet_id == pet_id:
                    return {
                        "pet_id": pet.pet_id,
                        "name": pet.name,
                        "last_fed": pet.last_fed,
                        "last_groomed": pet.last_groomed,
                        "last_vet_visit": pet.last_vet_visit
                    }
        return {}


class PetOwner:
    """Represents a pet owner and their account"""
    
    def __init__(self, account: str):
        self.account = account
        self.pets_list: List[Pet] = []
        self.daily_plan: Optional[DailyPlan] = None
        self.agent = Agent(owner=self)  # Agent can access pet data through owner
        self.scheduler = Scheduler()
    
    def login(self) -> bool:
        """Authenticate user login"""
        # Simple authentication - in a real system, this would check against a database
        return bool(self.account)
    
    def track_pet_activity(self, pet_id: str, activity: str) -> None:
        """Record a pet activity"""
        for pet in self.pets_list:
            if pet.pet_id == pet_id:
                activity_lower = activity.lower()
                if "feed" in activity_lower or "feeding" in activity_lower:
                    pet.feed()
                elif "groom" in activity_lower or "grooming" in activity_lower:
                    pet.grooming()
                elif "treat" in activity_lower or "treatment" in activity_lower:
                    # Extract treatment type if available
                    treatment_type = activity.split(":")[-1].strip() if ":" in activity else "general"
                    pet.treatment(treatment_type)
                else:
                    # Generic activity tracking
                    record = {
                        "activity": activity,
                        "timestamp": datetime.now(),
                        "pet_id": pet_id
                    }
                    pet.care_history.append(record)
                return
    
    def update_pet_info(self, pet_id: str, info: Dict) -> None:
        """Update pet information"""
        for pet in self.pets_list:
            if pet.pet_id == pet_id:
                # Update allowed fields
                if "name" in info:
                    pet.name = info["name"]
                if "age" in info:
                    pet.age = info["age"]
                if "med_info" in info:
                    pet.med_info = info["med_info"]
                if "physical_attributes" in info:
                    pet.physical_attributes.update(info["physical_attributes"])
                return
    
    def get_daily_plan(self) -> Optional[DailyPlan]:
        """Retrieve today's daily plan"""
        return self.daily_plan
    
    def view_pet_history(self, pet_id: str) -> List[Dict]:
        """View the care history of a pet"""
        for pet in self.pets_list:
            if pet.pet_id == pet_id:
                return pet.get_care_history()
        return []


# Example usage
if __name__ == "__main__":
    # Create a pet owner
    owner = PetOwner("john_doe")
    
    # Create a pet
    pet = Pet(
        name="Buddy",
        pet_id="pet_001",
        age=3,
        med_info="None",
        physical_attributes={"breed": "Golden Retriever", "weight": 25}
    )
    
    # Add pet to owner
    owner.pets_list.append(pet)
    
    # Create care tasks
    feeding_task = CareTask(
        task_type="feeding",
        description="Feed Buddy with dog food",
        priority=1,
        frequency="twice daily"
    )
    
    grooming_task = CareTask(
        task_type="grooming",
        description="Brush Buddy's coat",
        priority=2,
        frequency="weekly"
    )
    
    # Create a daily plan
    daily_plan = DailyPlan("2026-03-30")
    daily_plan.scheduled_tasks.append(feeding_task)
    daily_plan.scheduled_tasks.append(grooming_task)
    
    owner.daily_plan = daily_plan
