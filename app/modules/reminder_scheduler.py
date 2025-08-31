import schedule
import time
import json
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
from app.core.whatsapp_client import whatsapp_client

logger = logging.getLogger(__name__)

class ReminderScheduler:
    def __init__(self, data_file: str = "data/reminders.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.reminders = self._load_reminders()
        self.next_id = self._get_next_id()
        self.scheduler_thread = None
        self.running = False
        
    def _load_reminders(self) -> List[Dict[str, Any]]:
        """Load reminders from JSON file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading reminders: {e}")
            return []
    
    def _save_reminders(self):
        """Save reminders to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.reminders, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving reminders: {e}")
    
    def _get_next_id(self) -> int:
        """Get the next available ID"""
        if not self.reminders:
            return 1
        return max(reminder.get('id', 0) for reminder in self.reminders) + 1
    
    def add_reminder(self, time_str: str, message: str, phone_number: str, 
                    repeat: str = "once", days: List[str] = None) -> Dict[str, Any]:
        """Add a new reminder"""
        reminder = {
            'id': self.next_id,
            'time': time_str,
            'message': message,
            'phone_number': phone_number,
            'repeat': repeat,  # once, daily, weekly
            'days': days or [],  # for weekly reminders
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'last_triggered': None
        }
        
        self.reminders.append(reminder)
        self.next_id += 1
        self._save_reminders()
        
        # Schedule the reminder
        self._schedule_reminder(reminder)
        
        logger.info(f"Added reminder: {time_str} - {message}")
        return reminder
    
    def _schedule_reminder(self, reminder: Dict[str, Any]):
        """Schedule a reminder using the schedule library"""
        try:
            time_str = reminder['time']
            message = reminder['message']
            phone_number = reminder['phone_number']
            repeat = reminder.get('repeat', 'once')
            
            if repeat == 'once':
                # Parse time string (e.g., "18:30" or "2024-01-15 18:30")
                if len(time_str) == 5:  # HH:MM format
                    schedule.every().day.at(time_str).do(
                        self._send_reminder, phone_number, message, reminder['id']
                    )
                else:  # Full datetime format
                    dt = datetime.fromisoformat(time_str)
                    schedule.every().day.at(dt.strftime("%H:%M")).do(
                        self._send_reminder, phone_number, message, reminder['id']
                    )
            
            elif repeat == 'daily':
                schedule.every().day.at(time_str).do(
                    self._send_reminder, phone_number, message, reminder['id']
                )
            
            elif repeat == 'weekly' and reminder.get('days'):
                for day in reminder['days']:
                    day_map = {
                        'monday': schedule.every().monday,
                        'tuesday': schedule.every().tuesday,
                        'wednesday': schedule.every().wednesday,
                        'thursday': schedule.every().thursday,
                        'friday': schedule.every().friday,
                        'saturday': schedule.every().saturday,
                        'sunday': schedule.every().sunday
                    }
                    if day.lower() in day_map:
                        day_map[day.lower()].at(time_str).do(
                            self._send_reminder, phone_number, message, reminder['id']
                        )
            
            logger.info(f"Scheduled reminder {reminder['id']} for {time_str}")
            
        except Exception as e:
            logger.error(f"Error scheduling reminder: {e}")
    
    def _send_reminder(self, phone_number: str, message: str, reminder_id: int):
        """Send reminder via WhatsApp"""
        try:
            # Send the reminder message
            result = whatsapp_client.send_text_message(phone_number, f"⏰ Reminder: {message}")
            
            # Update reminder status
            self._update_reminder_triggered(reminder_id)
            
            logger.info(f"Reminder {reminder_id} sent to {phone_number}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending reminder {reminder_id}: {e}")
    
    def _update_reminder_triggered(self, reminder_id: int):
        """Update reminder last triggered time"""
        for reminder in self.reminders:
            if reminder.get('id') == reminder_id:
                reminder['last_triggered'] = datetime.now().isoformat()
                if reminder.get('repeat') == 'once':
                    reminder['status'] = 'completed'
                self._save_reminders()
                break
    
    def list_reminders(self, status: str = None) -> List[Dict[str, Any]]:
        """List all reminders, optionally filtered by status"""
        if status:
            return [r for r in self.reminders if r.get('status') == status]
        return self.reminders
    
    def get_reminder(self, reminder_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific reminder by ID"""
        for reminder in self.reminders:
            if reminder.get('id') == reminder_id:
                return reminder
        return None
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder"""
        reminder = self.get_reminder(reminder_id)
        if reminder:
            reminder['status'] = 'deleted'
            self._save_reminders()
            logger.info(f"Deleted reminder {reminder_id}: {reminder['message']}")
            return True
        return False
    
    def start_scheduler(self):
        """Start the reminder scheduler in a separate thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            logger.info("Reminder scheduler started")
    
    def stop_scheduler(self):
        """Stop the reminder scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("Reminder scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def format_reminder_list(self, reminders: List[Dict[str, Any]] = None) -> str:
        """Format reminders for WhatsApp display"""
        if reminders is None:
            reminders = self.list_reminders('active')
        
        if not reminders:
            return "⏰ No active reminders found."
        
        result = "⏰ Your reminders:\n\n"
        for reminder in reminders:
            status_emoji = "✅" if reminder.get('status') == 'completed' else "⏰"
            repeat_emoji = {
                'once': '1️⃣',
                'daily': '🔄',
                'weekly': '📅'
            }.get(reminder.get('repeat', 'once'), '1️⃣')
            
            result += f"{status_emoji} {repeat_emoji} {reminder['id']}. {reminder['time']} - {reminder['message']}\n"
            
            if reminder.get('repeat') == 'weekly' and reminder.get('days'):
                result += f"   📅 Days: {', '.join(reminder['days'])}\n"
            
            if reminder.get('last_triggered'):
                result += f"   🔔 Last triggered: {reminder['last_triggered'][:10]}\n"
            
            result += "\n"
        
        return result.strip()
    
    def parse_time_string(self, time_str: str) -> Optional[datetime]:
        """Parse various time string formats"""
        try:
            # Try HH:MM format (for today)
            if len(time_str) == 5 and ':' in time_str:
                hour, minute = map(int, time_str.split(':'))
                now = datetime.now()
                return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Try full datetime format
            return datetime.fromisoformat(time_str)
            
        except Exception as e:
            logger.error(f"Error parsing time string '{time_str}': {e}")
            return None

# Global reminder scheduler instance
reminder_scheduler = ReminderScheduler()
