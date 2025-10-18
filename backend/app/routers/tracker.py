from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import Goal, GoalCreate, GoalUpdate
from app.models.database import get_db, GoalDB
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/tracker", tags=["Tracker"])


@router.post("/goals", response_model=Goal)
async def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    """
    Create a new career goal

    Args:
        goal: Goal details
        db: Database session

    Returns:
        Created goal
    """
    try:
        db_goal = GoalDB(
            title=goal.title,
            description=goal.description,
            target_date=goal.target_date,
            status="pending",
            created_at=datetime.now().isoformat()
        )

        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)

        return Goal(
            id=db_goal.id,
            title=db_goal.title,
            description=db_goal.description,
            target_date=db_goal.target_date,
            status=db_goal.status,
            created_at=db_goal.created_at
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating goal: {str(e)}")


@router.get("/goals", response_model=List[Goal])
async def get_goals(db: Session = Depends(get_db)):
    """Get all career goals"""
    try:
        goals = db.query(GoalDB).all()
        return [
            Goal(
                id=goal.id,
                title=goal.title,
                description=goal.description,
                target_date=goal.target_date,
                status=goal.status,
                created_at=goal.created_at
            )
            for goal in goals
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goals: {str(e)}")


@router.get("/goals/{goal_id}", response_model=Goal)
async def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get a specific goal by ID"""
    try:
        goal = db.query(GoalDB).filter(GoalDB.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        return Goal(
            id=goal.id,
            title=goal.title,
            description=goal.description,
            target_date=goal.target_date,
            status=goal.status,
            created_at=goal.created_at
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goal: {str(e)}")


@router.put("/goals/{goal_id}", response_model=Goal)
async def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session = Depends(get_db)):
    """Update a goal"""
    try:
        goal = db.query(GoalDB).filter(GoalDB.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        # Update fields if provided
        if goal_update.title is not None:
            goal.title = goal_update.title
        if goal_update.description is not None:
            goal.description = goal_update.description
        if goal_update.target_date is not None:
            goal.target_date = goal_update.target_date
        if goal_update.status is not None:
            goal.status = goal_update.status

        db.commit()
        db.refresh(goal)

        return Goal(
            id=goal.id,
            title=goal.title,
            description=goal.description,
            target_date=goal.target_date,
            status=goal.status,
            created_at=goal.created_at
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating goal: {str(e)}")


@router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a goal"""
    try:
        goal = db.query(GoalDB).filter(GoalDB.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        db.delete(goal)
        db.commit()

        return {"message": "Goal deleted successfully", "id": goal_id}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting goal: {str(e)}")


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get tracker statistics"""
    try:
        total_goals = db.query(GoalDB).count()
        pending_goals = db.query(GoalDB).filter(GoalDB.status == "pending").count()
        in_progress_goals = db.query(GoalDB).filter(GoalDB.status == "in_progress").count()
        completed_goals = db.query(GoalDB).filter(GoalDB.status == "completed").count()

        return {
            "total_goals": total_goals,
            "pending": pending_goals,
            "in_progress": in_progress_goals,
            "completed": completed_goals,
            "completion_rate": round((completed_goals / total_goals * 100), 2) if total_goals > 0 else 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")
