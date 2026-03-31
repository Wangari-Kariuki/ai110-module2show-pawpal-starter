"""
Comprehensive Unit Tests for PawPal+ Pet Care Management System
Tests cover all classes, methods, and core functionality
"""

import pytest
from datetime import datetime, timedelta
from pawpal_system import (
    Pet, CareTask, Constraint, DailyPlan, 
    Scheduler, Agent, PetOwner
)


# ============================================================================
# PET CLASS TESTS
# ============================================================================

class TestPet:
    """Test suite for Pet class"""
    
    @pytest.fixture
    def sample_pet(self):
        """Create a sample pet for testing"""
        return Pet(
            name="Buddy",
            pet_id="pet_001",
            age=3,
            med_info="Allergic to chicken",
            physical_attributes={"breed": "Golden Retriever", "weight": 28}
        )
    
    def test_pet_creation(self, sample_pet):
        """Test pet object creation with correct attributes"""
        assert sample_pet.name == "Buddy"
        assert sample_pet.pet_id == "pet_001"
        assert sample_pet.age == 3
        assert sample_pet.med_info == "Allergic to chicken"
        assert sample_pet.physical_attributes["breed"] == "Golden Retriever"
    
    def test_pet_feed(self, sample_pet):
        """Test feeding a pet records the activity"""
        assert sample_pet.last_fed is None
        sample_pet.feed()
        assert sample_pet.last_fed is not None
        assert len(sample_pet.care_history) == 1
        assert sample_pet.care_history[0]["activity"] == "feeding"
    
    def test_pet_grooming(self, sample_pet):
        """Test grooming a pet records the activity"""
        assert sample_pet.last_groomed is None
        sample_pet.grooming()
        assert sample_pet.last_groomed is not None
        assert len(sample_pet.care_history) == 1
        assert sample_pet.care_history[0]["activity"] == "grooming"
    
    def test_pet_treatment(self, sample_pet):
        """Test treatment for a pet records the activity"""
        assert sample_pet.last_vet_visit is None
        sample_pet.treatment("vaccination")
        assert sample_pet.last_vet_visit is not None
        assert len(sample_pet.care_history) == 1
        assert sample_pet.care_history[0]["activity"] == "treatment"
        assert sample_pet.care_history[0]["treatment_type"] == "vaccination"
    
    def test_pet_care_history(self, sample_pet):
        """Test that care history accumulates multiple activities"""
        sample_pet.feed()
        sample_pet.grooming()
        sample_pet.treatment("checkup")
        
        history = sample_pet.get_care_history()
        assert len(history) == 3
        assert history[0]["activity"] == "feeding"
        assert history[1]["activity"] == "grooming"
        assert history[2]["activity"] == "treatment"
    
    def test_pet_multiple_feeds(self, sample_pet):
        """Test multiple feedings update last_fed"""
        sample_pet.feed()
        first_feed_time = sample_pet.last_fed
        
        # Wait a moment and feed again
        import time
        time.sleep(0.01)
        sample_pet.feed()
        second_feed_time = sample_pet.last_fed
        
        assert second_feed_time > first_feed_time
        assert len(sample_pet.care_history) == 2


# ============================================================================
# CARETASK CLASS TESTS
# ============================================================================

class TestCareTask:
    """Test suite for CareTask class"""
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample care task for testing"""
        return CareTask(
            task_type="feeding",
            description="Feed Buddy",
            priority=1,
            frequency="daily",
            owner_preferences={"time": "8am"}
        )
    
    def test_task_creation(self, sample_task):
        """Test care task creation"""
        assert sample_task.task_type == "feeding"
        assert sample_task.priority == 1
        assert sample_task.frequency == "daily"
    
    def test_task_mark_completed(self, sample_task):
        """Test marking a task as completed"""
        assert sample_task.last_completed is None
        sample_task.mark_completed()
        assert sample_task.last_completed is not None
    
    def test_task_is_completed_never_done(self, sample_task):
        """Test is_completed returns False if task never completed"""
        assert sample_task.is_completed() is False
    
    def test_task_is_completed_recent(self, sample_task):
        """Test is_completed returns True if recently completed"""
        sample_task.mark_completed()
        assert sample_task.is_completed() is True
    
    def test_task_is_completed_overdue(self):
        """Test is_completed returns False if overdue"""
        task = CareTask(
            task_type="feeding",
            description="Feed pet",
            priority=1,
            frequency="daily"
        )
        # Mark as completed a week ago
        task.last_completed = datetime.now() - timedelta(days=8)
        assert task.is_completed() is False
    
    def test_task_next_due_date_never_done(self, sample_task):
        """Test next due date when task never completed"""
        next_due = sample_task.get_next_due_date()
        # Should be close to now (within a few seconds)
        assert (next_due - datetime.now()).total_seconds() < 5
    
    def test_task_next_due_date_daily(self, sample_task):
        """Test next due date calculation for daily task"""
        sample_task.mark_completed()
        next_due = sample_task.get_next_due_date()
        expected = sample_task.last_completed + timedelta(days=1)
        assert next_due == expected
    
    def test_task_next_due_date_weekly(self):
        """Test next due date for weekly task"""
        task = CareTask(
            task_type="grooming",
            description="Groom pet",
            priority=2,
            frequency="weekly"
        )
        task.mark_completed()
        next_due = task.get_next_due_date()
        expected = task.last_completed + timedelta(days=7)
        assert next_due == expected
    
    def test_task_next_due_date_twice_daily(self):
        """Test next due date for twice daily task"""
        task = CareTask(
            task_type="medication",
            description="Give medication",
            priority=1,
            frequency="twice daily"
        )
        task.mark_completed()
        next_due = task.get_next_due_date()
        expected = task.last_completed + timedelta(hours=12)
        assert next_due == expected
    
    def test_task_various_frequencies(self):
        """Test task with various frequency types"""
        frequencies = {
            "daily": timedelta(days=1),
            "weekly": timedelta(days=7),
            "monthly": timedelta(days=30),
            "every 2 days": timedelta(days=2),
            "every 3 days": timedelta(days=3),
        }
        
        for freq, expected_delta in frequencies.items():
            task = CareTask(
                task_type="test",
                description=f"Test {freq}",
                priority=1,
                frequency=freq
            )
            task.mark_completed()
            next_due = task.get_next_due_date()
            assert next_due == task.last_completed + expected_delta


# ============================================================================
# CONSTRAINT CLASS TESTS
# ============================================================================

class TestConstraint:
    """Test suite for Constraint class"""
    
    def test_constraint_creation(self):
        """Test constraint creation"""
        constraint = Constraint("priority", "1", weight=2)
        assert constraint.constraint_type == "priority"
        assert constraint.value == "1"
        assert constraint.weight == 2
    
    def test_constraint_priority_evaluate(self):
        """Test priority constraint evaluation"""
        constraint = Constraint("priority", "1")
        task = CareTask("feeding", "Feed", priority=1, frequency="daily")
        assert constraint.evaluate(task) is True
        
        task_low = CareTask("play", "Play", priority=0, frequency="daily")
        assert constraint.evaluate(task_low) is False
    
    def test_constraint_task_type_evaluate(self):
        """Test task_type constraint evaluation"""
        constraint = Constraint("task_type", "feeding")
        task = CareTask("feeding", "Feed", priority=1, frequency="daily")
        assert constraint.evaluate(task) is True
        
        task_diff = CareTask("grooming", "Groom", priority=1, frequency="daily")
        assert constraint.evaluate(task_diff) is False
    
    def test_constraint_get_priority(self):
        """Test getting constraint priority weight"""
        constraint = Constraint("priority", "1", weight=5)
        assert constraint.get_priority() == 5


# ============================================================================
# DAILYPLAN CLASS TESTS
# ============================================================================

class TestDailyPlan:
    """Test suite for DailyPlan class"""
    
    @pytest.fixture
    def sample_plan(self):
        """Create a sample daily plan"""
        return DailyPlan("2026-03-30", time_available=8)
    
    def test_plan_creation(self, sample_plan):
        """Test daily plan creation"""
        assert sample_plan.date == "2026-03-30"
        assert sample_plan.time_available == 8
        assert len(sample_plan.scheduled_tasks) == 0
    
    def test_plan_add_tasks(self, sample_plan):
        """Test adding tasks to daily plan"""
        task1 = CareTask("feeding", "Feed", priority=1, frequency="daily")
        task2 = CareTask("grooming", "Groom", priority=2, frequency="weekly")
        
        sample_plan.scheduled_tasks.append(task1)
        sample_plan.scheduled_tasks.append(task2)
        
        assert len(sample_plan.scheduled_tasks) == 2
    
    def test_plan_get_tasks_for_day(self, sample_plan):
        """Test getting tasks for the day"""
        task = CareTask("feeding", "Feed", priority=1, frequency="daily")
        sample_plan.scheduled_tasks.append(task)
        
        tasks = sample_plan.get_tasks_for_day()
        assert len(tasks) == 1
        assert tasks[0].task_type == "feeding"
    
    def test_plan_get_task_by_type(self, sample_plan):
        """Test getting a specific task by type"""
        task1 = CareTask("feeding", "Feed", priority=1, frequency="daily")
        task2 = CareTask("grooming", "Groom", priority=2, frequency="weekly")
        
        sample_plan.scheduled_tasks.extend([task1, task2])
        
        feeding_task = sample_plan.get_task_by_type("feeding")
        assert feeding_task is not None
        assert feeding_task.task_type == "feeding"
    
    def test_plan_get_task_by_type_not_found(self, sample_plan):
        """Test getting non-existent task type"""
        result = sample_plan.get_task_by_type("nonexistent")
        assert result is None
    
    def test_plan_reschedule_task(self, sample_plan):
        """Test rescheduling a task"""
        task = CareTask("feeding", "Feed", priority=1, frequency="daily")
        task.task_id = "task_001"
        sample_plan.scheduled_tasks.append(task)
        
        new_time = datetime.now() + timedelta(hours=2)
        sample_plan.reschedule_task("task_001", new_time)
        
        assert "rescheduled_to" in task.owner_preferences


# ============================================================================
# SCHEDULER CLASS TESTS
# ============================================================================

class TestScheduler:
    """Test suite for Scheduler class"""
    
    @pytest.fixture
    def sample_scheduler(self):
        """Create a sample scheduler"""
        return Scheduler(optimization_method="greedy")
    
    def test_scheduler_creation(self, sample_scheduler):
        """Test scheduler creation"""
        assert sample_scheduler.optimization_method == "greedy"
        assert len(sample_scheduler.constraints) == 0
    
    def test_schedule_tasks(self, sample_scheduler):
        """Test creating a daily plan from pet tasks"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        daily_plan = sample_scheduler.schedule_tasks(pet, available_time=8)
        
        assert daily_plan is not None
        assert daily_plan.time_available == 8
    
    def test_optimize_schedule_greedy(self, sample_scheduler):
        """Test greedy optimization sorts by priority"""
        plan = DailyPlan("2026-03-30")
        task1 = CareTask("feeding", "Feed", priority=2, frequency="daily")
        task2 = CareTask("play", "Play", priority=1, frequency="daily")
        task3 = CareTask("grooming", "Groom", priority=3, frequency="weekly")
        
        plan.scheduled_tasks.extend([task1, task2, task3])
        optimized = sample_scheduler.optimize_schedule(plan)
        
        # Should be sorted by priority (highest first)
        assert optimized.scheduled_tasks[0].priority == 3
        assert optimized.scheduled_tasks[1].priority == 2
        assert optimized.scheduled_tasks[2].priority == 1
    
    def test_check_conflicts_no_conflict(self, sample_scheduler):
        """Test conflict checking with no conflicts"""
        task1 = CareTask("feeding", "Feed", priority=1, frequency="daily")
        task2 = CareTask("grooming", "Groom", priority=2, frequency="weekly")
        
        has_conflict = sample_scheduler.check_conflicts([task1, task2])
        assert has_conflict is False
    
    def test_check_conflicts_with_conflict(self, sample_scheduler):
        """Test conflict checking with duplicate task types"""
        task1 = CareTask("feeding", "Feed", priority=1, frequency="daily")
        task2 = CareTask("feeding", "Feed again", priority=1, frequency="daily")
        
        has_conflict = sample_scheduler.check_conflicts([task1, task2])
        assert has_conflict is True


# ============================================================================
# AGENT CLASS TESTS
# ============================================================================

class TestAgent:
    """Test suite for Agent class"""
    
    @pytest.fixture
    def setup_agent_with_owner(self):
        """Setup agent with owner and pets"""
        owner = PetOwner("test_owner")
        pet = Pet("Buddy", "pet_001", 3, "None")
        owner.pets_list.append(pet)
        agent = owner.agent  # Use the agent created with owner
        return agent, owner, pet
    
    def test_agent_creation(self):
        """Test agent creation"""
        agent = Agent()
        assert agent.knowledge_base is not None
    
    def test_agent_answer_question_fed(self, setup_agent_with_owner):
        """Test agent answers feeding questions"""
        agent, owner, pet = setup_agent_with_owner
        
        pet.feed()
        answer = agent.answer_question("Has Buddy been fed?")
        assert "fed" in answer.lower()
        assert "Buddy" in answer
    
    def test_agent_answer_question_not_fed(self, setup_agent_with_owner):
        """Test agent answers when pet not yet fed"""
        agent, owner, pet = setup_agent_with_owner
        
        answer = agent.answer_question("Has Buddy been fed?")
        assert "not been fed" in answer.lower()
    
    def test_agent_answer_question_groomed(self, setup_agent_with_owner):
        """Test agent answers grooming questions"""
        agent, owner, pet = setup_agent_with_owner
        
        pet.grooming()
        answer = agent.answer_question("When was Buddy last groomed?")
        assert "groomed" in answer.lower()
    
    def test_agent_answer_question_vet(self, setup_agent_with_owner):
        """Test agent answers vet visit questions"""
        agent, owner, pet = setup_agent_with_owner
        
        pet.treatment("checkup")
        answer = agent.answer_question("When was the vet visit for Buddy?")
        assert "vet" in answer.lower()
    
    def test_agent_get_pet_status(self, setup_agent_with_owner):
        """Test agent gets pet status"""
        agent, owner, pet = setup_agent_with_owner
        
        pet.feed()
        status = agent.get_pet_status("pet_001")
        
        assert status["name"] == "Buddy"
        assert status["last_fed"] is not None
    
    def test_agent_suggest_next_task(self, setup_agent_with_owner):
        """Test agent suggests next task"""
        agent, owner, pet = setup_agent_with_owner
        
        task = CareTask("feeding", "Feed Buddy", priority=1, frequency="daily")
        pet.required_tasks.append(task)
        
        suggested = agent.suggest_next_task()
        assert suggested is not None


# ============================================================================
# PETOWNER CLASS TESTS
# ============================================================================

class TestPetOwner:
    """Test suite for PetOwner class"""
    
    @pytest.fixture
    def sample_owner(self):
        """Create a sample pet owner"""
        return PetOwner("sarah_smith")
    
    def test_owner_creation(self, sample_owner):
        """Test pet owner creation"""
        assert sample_owner.account == "sarah_smith"
        assert len(sample_owner.pets_list) == 0
        assert sample_owner.agent is not None
        assert sample_owner.scheduler is not None
    
    def test_owner_login(self, sample_owner):
        """Test owner login"""
        assert sample_owner.login() is True
    
    def test_owner_add_pet(self, sample_owner):
        """Test adding pets to owner"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        assert len(sample_owner.pets_list) == 1
        assert sample_owner.pets_list[0].name == "Buddy"
    
    def test_owner_track_pet_activity_feeding(self, sample_owner):
        """Test tracking feeding activity"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        sample_owner.track_pet_activity("pet_001", "feeding")
        assert pet.last_fed is not None
    
    def test_owner_track_pet_activity_grooming(self, sample_owner):
        """Test tracking grooming activity"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        sample_owner.track_pet_activity("pet_001", "grooming")
        assert pet.last_groomed is not None
    
    def test_owner_track_pet_activity_treatment(self, sample_owner):
        """Test tracking treatment activity"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        sample_owner.track_pet_activity("pet_001", "treatment: vaccination")
        assert pet.last_vet_visit is not None
    
    def test_owner_update_pet_info(self, sample_owner):
        """Test updating pet information"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        sample_owner.update_pet_info("pet_001", {
            "age": 4,
            "physical_attributes": {"weight": 30}
        })
        
        assert pet.age == 4
        assert pet.physical_attributes["weight"] == 30
    
    def test_owner_get_daily_plan(self, sample_owner):
        """Test getting daily plan"""
        plan = DailyPlan("2026-03-30")
        sample_owner.daily_plan = plan
        
        retrieved_plan = sample_owner.get_daily_plan()
        assert retrieved_plan.date == "2026-03-30"
    
    def test_owner_view_pet_history(self, sample_owner):
        """Test viewing pet care history"""
        pet = Pet("Buddy", "pet_001", 3, "None")
        sample_owner.pets_list.append(pet)
        
        pet.feed()
        pet.grooming()
        
        history = sample_owner.view_pet_history("pet_001")
        assert len(history) == 2
        assert history[0]["activity"] == "feeding"
        assert history[1]["activity"] == "grooming"
    
    def test_owner_view_pet_history_nonexistent(self, sample_owner):
        """Test viewing history for nonexistent pet"""
        history = sample_owner.view_pet_history("pet_999")
        assert history == []


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple classes"""
    
    def test_complete_workflow(self):
        """Test complete pet care workflow"""
        # Create owner
        owner = PetOwner("jane_doe")
        assert owner.login() is True
        
        # Create pet
        pet = Pet("Fluffy", "pet_001", 2, "None", 
                  physical_attributes={"breed": "Siamese"})
        owner.pets_list.append(pet)
        
        # Create tasks
        feeding_task = CareTask("feeding", "Feed Fluffy", priority=1, frequency="daily")
        grooming_task = CareTask("grooming", "Groom Fluffy", priority=2, frequency="weekly")
        
        pet.required_tasks.extend([feeding_task, grooming_task])
        
        # Track activities
        owner.track_pet_activity("pet_001", "feeding")
        assert pet.last_fed is not None
        
        # Create plan and optimize
        plan = DailyPlan("2026-03-30")
        plan.scheduled_tasks.extend([feeding_task, grooming_task])
        
        optimized = owner.scheduler.optimize_schedule(plan)
        assert optimized.scheduled_tasks[0].priority == 2  # Grooming (higher priority)
        
        # Use agent
        answer = owner.agent.answer_question("Has Fluffy been fed?")
        assert "Fluffy" in answer
    
    def test_multiple_pets_workflow(self):
        """Test workflow with multiple pets"""
        owner = PetOwner("multi_pet_owner")
        
        # Add multiple pets
        pet1 = Pet("Dog", "pet_001", 3, "None")
        pet2 = Pet("Cat", "pet_002", 5, "None")
        owner.pets_list.extend([pet1, pet2])
        
        # Track activities
        owner.track_pet_activity("pet_001", "feeding")
        owner.track_pet_activity("pet_002", "grooming")
        
        # Check both were tracked
        assert pet1.last_fed is not None
        assert pet2.last_groomed is not None
        
        # Check history
        history1 = owner.view_pet_history("pet_001")
        history2 = owner.view_pet_history("pet_002")
        
        assert len(history1) > 0
        assert len(history2) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
