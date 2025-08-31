import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TodoManager:
    def __init__(self, data_file: str = "data/todos.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.todos = self._load_todos()
        self.next_id = self._get_next_id()
    
    def _load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from JSON file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading todos: {e}")
            return []
    
    def _save_todos(self):
        """Save todos to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving todos: {e}")
    
    def _get_next_id(self) -> int:
        """Get the next available ID"""
        if not self.todos:
            return 1
        return max(todo.get('id', 0) for todo in self.todos) + 1
    
    def add_todo(self, task: str, priority: str = "medium", due_date: str = None) -> Dict[str, Any]:
        """Add a new todo item"""
        todo = {
            'id': self.next_id,
            'task': task,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'due_date': due_date,
            'completed_at': None
        }
        
        self.todos.append(todo)
        self.next_id += 1
        self._save_todos()
        
        logger.info(f"Added todo: {task}")
        return todo
    
    def list_todos(self, status: str = None) -> List[Dict[str, Any]]:
        """List all todos, optionally filtered by status"""
        if status:
            return [todo for todo in self.todos if todo.get('status') == status]
        return self.todos
    
    def get_todo(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific todo by ID"""
        for todo in self.todos:
            if todo.get('id') == todo_id:
                return todo
        return None
    
    def complete_todo(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Mark a todo as completed"""
        todo = self.get_todo(todo_id)
        if todo:
            todo['status'] = 'completed'
            todo['completed_at'] = datetime.now().isoformat()
            self._save_todos()
            logger.info(f"Completed todo {todo_id}: {todo['task']}")
            return todo
        return None
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        todo = self.get_todo(todo_id)
        if todo:
            self.todos = [t for t in self.todos if t.get('id') != todo_id]
            self._save_todos()
            logger.info(f"Deleted todo {todo_id}: {todo['task']}")
            return True
        return False
    
    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a todo item"""
        todo = self.get_todo(todo_id)
        if todo:
            for key, value in kwargs.items():
                if key in ['task', 'priority', 'due_date', 'status']:
                    todo[key] = value
            self._save_todos()
            logger.info(f"Updated todo {todo_id}")
            return todo
        return None
    
    def get_todo_summary(self) -> Dict[str, Any]:
        """Get a summary of todos"""
        total = len(self.todos)
        pending = len([t for t in self.todos if t.get('status') == 'pending'])
        completed = len([t for t in self.todos if t.get('status') == 'completed'])
        
        return {
            'total': total,
            'pending': pending,
            'completed': completed,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
    
    def format_todo_list(self, todos: List[Dict[str, Any]] = None) -> str:
        """Format todos for WhatsApp display"""
        if todos is None:
            todos = self.list_todos()
        
        if not todos:
            return "📝 No todos found."
        
        result = "📝 Your todos:\n\n"
        for todo in todos:
            status_emoji = "✅" if todo.get('status') == 'completed' else "⏳"
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(todo.get('priority', 'medium'), '🟡')
            
            result += f"{status_emoji} {priority_emoji} {todo['id']}. {todo['task']}\n"
            
            if todo.get('due_date'):
                result += f"   📅 Due: {todo['due_date']}\n"
            
            if todo.get('status') == 'completed' and todo.get('completed_at'):
                result += f"   ✅ Completed: {todo['completed_at'][:10]}\n"
            
            result += "\n"
        
        return result.strip()

# Global todo manager instance
todo_manager = TodoManager()
