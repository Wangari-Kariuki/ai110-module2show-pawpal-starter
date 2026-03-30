# PawPal+ System UML Class Diagram

```mermaid
classDiagram
    class PetOwner {
        - account: string
        - pets_list: List~Pet~
        - daily_plan: DailyPlan
        + login(): boolean
        + track_pet_activity(pet_id: string, activity: string): void
        + update_pet_info(pet_id: string, info: dict): void
        + get_daily_plan(): DailyPlan
        + view_pet_history(pet_id: string): List
    }
    
    class Pet {
        - name: string
        - pet_id: string
        - age: int
        - med_info: string
        - physical_attributes: dict
        - last_fed: datetime
        - last_groomed: datetime
        - last_vet_visit: datetime
        + treatment(treatment_type: string): void
        + grooming(): void
        + feed(): void
        + get_care_history(): List
    }
    
    class CareTask {
        - task_type: string
        - description: string
        - priority: int
        - last_completed: datetime
        - frequency: string
        - owner_preferences: dict
        + is_completed(): boolean
        + mark_completed(): void
        + get_next_due_date(): datetime
    }
    
    class Constraint {
        - constraint_type: string
        - value: string
        - weight: int
        + evaluate(task: CareTask): boolean
        + get_priority(): int
    }
    
    class DailyPlan {
        - date: string
        - scheduled_tasks: List~CareTask~
        - time_available: int
        + generate_plan(): void
        + get_tasks_for_day(): List
        + get_task_by_type(task_type: string): CareTask
        + reschedule_task(task_id: string, new_time: datetime): void
    }
    
    class Scheduler {
        - constraints: List~Constraint~
        - optimization_method: string
        + schedule_tasks(pet: Pet, available_time: int): DailyPlan
        + optimize_schedule(daily_plan: DailyPlan): DailyPlan
        + check_conflicts(tasks: List~CareTask~): boolean
    }
    
    class Agent {
        - knowledge_base: dict
        + answer_question(question: string): string
        + suggest_next_task(): CareTask
        + get_pet_status(pet_id: string): dict
    }
    
    %% Relationships
    PetOwner "1" --> "*" Pet : owns
    PetOwner "1" --> "1" DailyPlan : has
    PetOwner "1" --> "1" Agent : uses
    Pet "1" --> "*" CareTask : needs
    DailyPlan "*" --> "*" CareTask : contains
    Scheduler --> DailyPlan : generates
    Scheduler "1" --> "*" Constraint : applies
    Agent --> PetOwner : assists
    Agent --> Pet : monitors
```

## System Description

### Core Components

**PetOwner**
- Manages user account and pet collection
- Tracks daily care activities and pet information
- Interacts with AI agent for guidance

**Pet**
- Stores pet information and care history
- Tracks key metrics (last fed, groomed, vet visit)
- Manages breed-specific or individual care protocols

**CareTask**
- Represents individual care activities (feeding, meds, grooming, enrichment)
- Tracks completion history and frequency
- Incorporates owner preferences

**Constraint**
- Enforces scheduling limitations (time available, priority, owner preferences)
- Each constraint has a weight for optimization

**DailyPlan**
- Generates optimized schedule for the day
- Allocates time and tasks based on constraints
- Allows rescheduling and task management

**Scheduler**
- Core logic for task scheduling
- Balances multiple constraints
- Detects and resolves scheduling conflicts

**Agent**
- AI component for answering care questions
- Provides status updates and recommendations
- Learns from user patterns and pet history

