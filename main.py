"""
PawPal+ Main Application
Demonstrates a fully functional pet care management system
"""

from pawpal_system import PetOwner, Pet, CareTask, Constraint, DailyPlan, Scheduler
from datetime import datetime, timedelta


def main():
    """Main application demonstrating PawPal+ system"""
    
    print("=" * 60)
    print("PawPal+ Pet Care Management System")
    print("=" * 60)
    print()
    
    # ============================================
    # 1. CREATE PET OWNER
    # ============================================
    print("1. Creating Pet Owner Account...")
    owner = PetOwner("sarah_smith")
    print(f"   Account: {owner.account}")
    print(f"   Login successful: {owner.login()}")
    print()
    
    # ============================================
    # 2. CREATE PETS WITH UNIQUE ATTRIBUTES
    # ============================================
    print("2. Creating Pets with Unique Attributes...")
    
    # Pet 1: Golden Retriever - active, needs frequent exercise
    buddy = Pet(
        name="Buddy",
        pet_id="pet_001",
        age=3,
        med_info="Allergic to chicken",
        physical_attributes={
            "breed": "Golden Retriever",
            "weight": 28,
            "color": "golden",
            "activity_level": "high"
        }
    )
    owner.pets_list.append(buddy)
    print(f"   ✓ {buddy.name} (ID: {buddy.pet_id})")
    print(f"     - Breed: {buddy.physical_attributes['breed']}")
    print(f"     - Weight: {buddy.physical_attributes['weight']}lbs")
    print(f"     - Medical: {buddy.med_info}")
    
    # Pet 2: Cat - independent, needs grooming
    whiskers = Pet(
        name="Whiskers",
        pet_id="pet_002",
        age=5,
        med_info="Diabetic - insulin shots daily",
        physical_attributes={
            "breed": "Persian Cat",
            "weight": 8,
            "color": "white",
            "activity_level": "low"
        }
    )
    owner.pets_list.append(whiskers)
    print(f"   ✓ {whiskers.name} (ID: {whiskers.pet_id})")
    print(f"     - Breed: {whiskers.physical_attributes['breed']}")
    print(f"     - Medical: {whiskers.med_info}")
    
    # Pet 3: Rabbit - special diet needs
    cotton = Pet(
        name="Cotton",
        pet_id="pet_003",
        age=2,
        med_info="None",
        physical_attributes={
            "breed": "Holland Lop Rabbit",
            "weight": 4,
            "color": "white with brown spots",
            "diet": "timothy hay and vegetables"
        }
    )
    owner.pets_list.append(cotton)
    print(f"   ✓ {cotton.name} (ID: {cotton.pet_id})")
    print(f"     - Breed: {cotton.physical_attributes['breed']}")
    print(f"     - Diet: {cotton.physical_attributes.get('diet', 'Standard')}")
    print()
    
    # ============================================
    # 3. CREATE CARE TASKS FOR EACH PET
    # ============================================
    print("3. Setting Up Care Tasks...")
    
    # Buddy's tasks
    buddy_feeding = CareTask(
        task_type="feeding",
        description="Feed Buddy with fish-based dog food (no chicken)",
        priority=1,
        frequency="twice daily",
        owner_preferences={"preferred_time": "8am and 6pm"}
    )
    buddy_feeding.task_id = "task_b1"
    
    buddy_exercise = CareTask(
        task_type="exercise",
        description="Take Buddy for a walk/run",
        priority=1,
        frequency="daily",
        owner_preferences={"duration": "45 minutes", "preferred_time": "morning"}
    )
    buddy_exercise.task_id = "task_b2"
    
    buddy_grooming = CareTask(
        task_type="grooming",
        description="Brush Buddy's coat",
        priority=2,
        frequency="every 3 days",
        owner_preferences={"duration": "20 minutes"}
    )
    buddy_grooming.task_id = "task_b3"
    
    buddy.required_tasks.extend([buddy_feeding, buddy_exercise, buddy_grooming])
    print(f"   ✓ {buddy.name}: 3 tasks assigned")
    
    # Whiskers' tasks
    whiskers_feeding = CareTask(
        task_type="feeding",
        description="Feed Whiskers high-protein cat food",
        priority=1,
        frequency="twice daily",
        owner_preferences={"preferred_time": "7am and 7pm"}
    )
    whiskers_feeding.task_id = "task_w1"
    
    whiskers_insulin = CareTask(
        task_type="medication",
        description="Give Whiskers insulin injection",
        priority=1,
        frequency="twice daily",
        owner_preferences={"critical": True, "before_meals": True}
    )
    whiskers_insulin.task_id = "task_w2"
    
    whiskers_grooming = CareTask(
        task_type="grooming",
        description="Brush Whiskers' long fur",
        priority=2,
        frequency="daily",
        owner_preferences={"duration": "10 minutes"}
    )
    whiskers_grooming.task_id = "task_w3"
    
    whiskers.required_tasks.extend([whiskers_feeding, whiskers_insulin, whiskers_grooming])
    print(f"   ✓ {whiskers.name}: 3 tasks assigned (1 critical)")
    
    # Cotton's tasks
    cotton_feeding = CareTask(
        task_type="feeding",
        description="Feed Cotton timothy hay and fresh vegetables",
        priority=1,
        frequency="daily",
        owner_preferences={"vegetables": ["carrots", "lettuce", "kale"]}
    )
    cotton_feeding.task_id = "task_c1"
    
    cotton_water = CareTask(
        task_type="water_change",
        description="Change Cotton's water",
        priority=1,
        frequency="daily",
        owner_preferences={"temperature": "room temperature"}
    )
    cotton_water.task_id = "task_c2"
    
    cotton_cage = CareTask(
        task_type="cleaning",
        description="Clean Cotton's cage",
        priority=2,
        frequency="every 3 days",
        owner_preferences={"duration": "30 minutes"}
    )
    cotton_cage.task_id = "task_c3"
    
    cotton.required_tasks.extend([cotton_feeding, cotton_water, cotton_cage])
    print(f"   ✓ {cotton.name}: 3 tasks assigned")
    print()
    
    # ============================================
    # 4. TRACK PET ACTIVITIES
    # ============================================
    print("4. Recording Pet Care Activities...")
    
    # Track some activities
    owner.track_pet_activity("pet_001", "feeding")
    print(f"   ✓ Recorded: Buddy fed at {datetime.now().strftime('%H:%M:%S')}")
    
    owner.track_pet_activity("pet_002", "medication: insulin")
    print(f"   ✓ Recorded: Whiskers given insulin")
    
    owner.track_pet_activity("pet_003", "water_change")
    print(f"   ✓ Recorded: Cotton's water changed")
    print()
    
    # ============================================
    # 5. UPDATE PET INFORMATION
    # ============================================
    print("5. Updating Pet Information...")
    
    owner.update_pet_info("pet_001", {
        "age": 4,
        "physical_attributes": {"weight": 29, "fitness": "excellent"}
    })
    print(f"   ✓ Updated {buddy.name}: age {buddy.age}, weight {buddy.physical_attributes['weight']}lbs")
    print()
    
    # ============================================
    # 6. USE AGENT TO ANSWER QUESTIONS
    # ============================================
    print("6. AI Agent - Answering Pet Care Questions...")
    
    questions = [
        "Has Buddy been fed?",
        "When was Whiskers last groomed?",
        "When was the last vet visit for Cotton?"
    ]
    
    for question in questions:
        answer = owner.agent.answer_question(question)
        print(f"   Q: {question}")
        print(f"   A: {answer}")
        print()
    
    # ============================================
    # 7. GET PET STATUS
    # ============================================
    print("7. Pet Status Report...")
    
    for pet in owner.pets_list:
        status = owner.agent.get_pet_status(pet.pet_id)
        print(f"   {status['name']}:")
        print(f"      - Last Fed: {status['last_fed']}")
        print(f"      - Last Groomed: {status['last_groomed']}")
        print(f"      - Last Vet Visit: {status['last_vet_visit']}")
    print()
    
    # ============================================
    # 8. VIEW CARE HISTORY
    # ============================================
    print("8. Care History...")
    
    buddy_history = owner.view_pet_history("pet_001")
    print(f"   {buddy.name}'s Recent Activities:")
    for activity in buddy_history[-3:] if buddy_history else []:
        print(f"      - {activity['activity']}: {activity['timestamp']}")
    print()
    
    # ============================================
    # 9. CREATE AND OPTIMIZE DAILY PLAN
    # ============================================
    print("9. Creating Daily Plan...")
    
    daily_plan = DailyPlan(
        date=datetime.now().strftime("%Y-%m-%d"),
        time_available=8  # 8 hours available
    )
    
    # Add all urgent tasks to the plan
    for pet in owner.pets_list:
        for task in pet.required_tasks[:2]:  # Add first 2 tasks per pet
            daily_plan.scheduled_tasks.append(task)
    
    print(f"   Plan Date: {daily_plan.date}")
    print(f"   Time Available: {daily_plan.time_available} hours")
    print(f"   Tasks Scheduled: {len(daily_plan.scheduled_tasks)}")
    
    # Optimize the schedule
    optimized_plan = owner.scheduler.optimize_schedule(daily_plan)
    print(f"\n   Optimized Task Priority:")
    for i, task in enumerate(optimized_plan.scheduled_tasks, 1):
        print(f"      {i}. {task.task_type} (Priority: {task.priority}) - {task.description}")
    print()
    
    # ============================================
    # 10. SUGGEST NEXT TASK
    # ============================================
    print("10. Suggesting Next Task...")
    
    next_task = owner.agent.suggest_next_task()
    if next_task:
        print(f"   Recommended: {next_task.task_type}")
        print(f"   Description: {next_task.description}")
        print(f"   Priority Level: {next_task.priority}")
    print()
    
    # ============================================
    # 11. DISPLAY SUMMARY
    # ============================================
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Owner Account: {owner.account}")
    print(f"Total Pets: {len(owner.pets_list)}")
    print(f"Total Tasks: {sum(len(pet.required_tasks) for pet in owner.pets_list)}")
    print(f"Daily Plan Created: {daily_plan.date}")
    print(f"Scheduler Optimization Method: {owner.scheduler.optimization_method}")
    print("=" * 60)


if __name__ == "__main__":
    main()