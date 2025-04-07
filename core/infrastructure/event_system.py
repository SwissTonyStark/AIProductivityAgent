"""
Event system module for handling real-time events and notifications.
Implements a pub/sub pattern for asynchronous event processing.
"""
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventPriority(Enum):
    """Event priority levels."""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class Event:
    """Base event class for all system events."""
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    priority: EventPriority = EventPriority.MEDIUM
    source: str = "system"

class EventBus:
    """Central event bus for managing event subscriptions and publishing."""
    
    def __init__(self):
        """Initialize the event bus."""
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._loop = asyncio.get_event_loop()
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Function to call when event occurs
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.info(f"Subscribed to event type: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Function to remove from subscribers
        """
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
            logger.info(f"Unsubscribed from event type: {event_type}")
    
    async def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers asynchronously.
        
        Args:
            event: Event to publish
        """
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        if event.event_type in self._subscribers:
            tasks = []
            for callback in self._subscribers[event.event_type]:
                tasks.append(self._loop.create_task(self._execute_callback(callback, event)))
            
            if tasks:
                await asyncio.gather(*tasks)
    
    async def _execute_callback(self, callback: Callable[[Event], None], event: Event) -> None:
        """
        Execute a callback safely with error handling.
        
        Args:
            callback: Function to execute
            event: Event to pass to callback
        """
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                await self._loop.run_in_executor(None, callback, event)
        except Exception as e:
            logger.error(f"Error in event callback: {str(e)}")
    
    def get_event_history(self, event_type: str = None) -> List[Event]:
        """
        Get event history, optionally filtered by type.
        
        Args:
            event_type: Optional event type to filter by
            
        Returns:
            List of historical events
        """
        if event_type:
            return [e for e in self._event_history if e.event_type == event_type]
        return self._event_history.copy()

# Global event bus instance
event_bus = EventBus()

# Example event types
class EventTypes:
    """Common event types used in the system."""
    EMAIL_RECEIVED = "email_received"
    EMAIL_SENT = "email_sent"
    CALENDAR_EVENT_CREATED = "calendar_event_created"
    CALENDAR_EVENT_UPDATED = "calendar_event_updated"
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    MEETING_STARTED = "meeting_started"
    MEETING_ENDED = "meeting_ended"
    USER_NOTIFICATION = "user_notification"
    SYSTEM_ERROR = "system_error"

# Example usage:
"""
async def handle_email_received(event: Event):
    print(f"New email received: {event.data}")

event_bus.subscribe(EventTypes.EMAIL_RECEIVED, handle_email_received)

await event_bus.publish(Event(
    event_type=EventTypes.EMAIL_RECEIVED,
    timestamp=datetime.now(),
    data={"subject": "Test Email", "sender": "test@example.com"},
    priority=EventPriority.MEDIUM
))
""" 