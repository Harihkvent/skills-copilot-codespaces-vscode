"""
Reminder and Scheduler Service
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.models import Reminder
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for managing reminders and scheduled tasks"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._started = False
    
    def start(self):
        """Start the scheduler"""
        if not self._started:
            self.scheduler.start()
            self._started = True
            logger.info("Reminder scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self._started:
            self.scheduler.shutdown()
            self._started = False
            logger.info("Reminder scheduler shut down")
    
    async def add_reminder(
        self,
        reminder_id: str,
        user_id: str,
        text: str,
        schedule: str,
        next_run: datetime
    ):
        """
        Add a reminder to the scheduler
        
        Args:
            reminder_id: Unique reminder ID
            user_id: User ID
            text: Reminder text
            schedule: Cron expression or ISO datetime
            next_run: Next execution time
        """
        job_id = f"reminder_{reminder_id}"
        
        try:
            # Try to parse as cron expression
            if self._is_cron(schedule):
                trigger = CronTrigger.from_crontab(schedule)
            else:
                # Treat as one-time datetime
                trigger = DateTrigger(run_date=next_run)
            
            self.scheduler.add_job(
                self._execute_reminder,
                trigger=trigger,
                args=[reminder_id, user_id, text],
                id=job_id,
                replace_existing=True
            )
            
            logger.info(f"Added reminder {job_id} for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to add reminder {job_id}: {e}")
            raise
    
    async def remove_reminder(self, reminder_id: str):
        """Remove a reminder from the scheduler"""
        job_id = f"reminder_{reminder_id}"
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed reminder {job_id}")
        except Exception as e:
            logger.warning(f"Failed to remove reminder {job_id}: {e}")
    
    async def _execute_reminder(self, reminder_id: str, user_id: str, text: str):
        """
        Execute a reminder (callback function)
        
        This would typically:
        1. Send a notification to the user
        2. Create a message in the conversation
        3. Update reminder status
        """
        logger.info(f"Executing reminder {reminder_id} for user {user_id}: {text}")
        
        async with AsyncSessionLocal() as db:
            try:
                # Update reminder next_run time if it's recurring
                stmt = select(Reminder).where(Reminder.id == reminder_id)
                result = await db.execute(stmt)
                reminder = result.scalar_one_or_none()
                
                if reminder:
                    # TODO: Send notification to user
                    # TODO: Create a message in conversation
                    logger.info(f"Reminder executed: {text}")
                    
                    # If not recurring, deactivate
                    if not self._is_cron(reminder.schedule):
                        reminder.is_active = False
                        await db.commit()
            except Exception as e:
                logger.error(f"Error executing reminder {reminder_id}: {e}")
    
    async def load_active_reminders(self):
        """Load all active reminders from database and schedule them"""
        async with AsyncSessionLocal() as db:
            stmt = select(Reminder).where(Reminder.is_active == True)
            result = await db.execute(stmt)
            reminders = result.scalars().all()
            
            for reminder in reminders:
                try:
                    await self.add_reminder(
                        reminder_id=str(reminder.id),
                        user_id=str(reminder.user_id),
                        text=reminder.text,
                        schedule=reminder.schedule,
                        next_run=reminder.next_run
                    )
                except Exception as e:
                    logger.error(f"Failed to load reminder {reminder.id}: {e}")
            
            logger.info(f"Loaded {len(reminders)} active reminders")
    
    def _is_cron(self, schedule: str) -> bool:
        """Check if schedule string is a cron expression"""
        # Simple heuristic: cron has spaces and 5-6 fields
        parts = schedule.strip().split()
        return len(parts) in [5, 6] and not schedule.startswith("20")


# Global reminder service instance
reminder_service = ReminderService()


async def init_reminder_service():
    """Initialize and start the reminder service"""
    reminder_service.start()
    await reminder_service.load_active_reminders()


async def shutdown_reminder_service():
    """Shutdown the reminder service"""
    reminder_service.shutdown()
