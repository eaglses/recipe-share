from pydantic import BaseModel
from typing import Optional, List
from queries.pool import pool
from .user_queries import BasicUserOut
from fastapi import HTTPException
from datetime import datetime

class Member(BaseModel)
    user_id: int

class NewGroup(BaseModel)
    ownerId: int

