from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

#--------- Classses -----------------#

# Base Entity
class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class Reporter(BaseEntity):
    def __init__(self, id: int, name: str, email: str, team: str):
        self.id = id
        self.name = name
        self.email = email
        self.team = team
    
    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        
        if '@' not in self.email:
            raise ValueError('Invalid Email')


class Issue(BaseEntity):
    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reported_id = reporter_id
        self.created_at = str(datetime.now())
    
    def validate(self):
        if not self.title:
            raise ValueError('Please provide title for issue')
        if not self.priority or not self.status:
            raise ValueError('Please provide priority or status')
    
    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} - needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} - low priority, handle when free"