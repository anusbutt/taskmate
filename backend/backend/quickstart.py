#!/usr/bin/env python3
# [Task]: T124 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Backend quickstart validation script.
Verifies database connection, runs migrations, and optionally seeds test data.
"""
import asyncio
import sys
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, create_db_and_tables, async_session_maker
from app.models.user import User
from app.models.task import Task
from app.services.user_service import create_user
from app.services.task_service import create_task
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate


async def verify_database_connection():
    """Verify database connection is working."""
    print("🔍 Verifying database connection...")
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(1))
            result.scalar_one()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def verify_migrations():
    """Verify database tables exist."""
    print("\n🔍 Verifying database migrations...")
    try:
        await create_db_and_tables()
        async with async_session_maker() as session:
            # Check if users table exists
            await session.execute(select(User).limit(1))
            # Check if tasks table exists
            await session.execute(select(Task).limit(1))
        print("✅ Database tables verified")
        return True
    except Exception as e:
        print(f"❌ Database tables verification failed: {e}")
        print("   Run: alembic upgrade head")
        return False


async def seed_test_data():
    """Seed test user and tasks."""
    print("\n🌱 Seeding test data...")
    try:
        async with async_session_maker() as session:
            # Check if test user already exists
            result = await session.execute(
                select(User).where(User.email == "test@example.com")
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print("⚠️  Test user already exists, skipping seed")
                return True

            # Create test user
            test_user = await create_user(
                session,
                UserCreate(
                    email="test@example.com",
                    name="Test User",
                    password="password123"
                )
            )
            print(f"✅ Created test user: {test_user.email}")

            # Create test tasks
            test_tasks = [
                TaskCreate(title="Buy groceries", description="Milk, eggs, bread"),
                TaskCreate(title="Finish project", description="Complete Phase 2 implementation"),
                TaskCreate(title="Exercise", description="Go for a 30-minute run"),
            ]

            for task_data in test_tasks:
                task = await create_task(session, task_data, test_user.id)
                print(f"✅ Created test task: {task.title}")

            print("\n✅ Test data seeded successfully")
            print("\n📋 Test credentials:")
            print("   Email: test@example.com")
            print("   Password: password123")
            return True

    except Exception as e:
        print(f"❌ Failed to seed test data: {e}")
        return False


async def main():
    """Main validation workflow."""
    print("🚀 Backend Quickstart Validation\n")
    print("=" * 50)

    # Step 1: Verify database connection
    if not await verify_database_connection():
        print("\n❌ Setup failed: Cannot connect to database")
        print("   Check DATABASE_URL in .env file")
        sys.exit(1)

    # Step 2: Verify migrations
    if not await verify_migrations():
        print("\n❌ Setup failed: Database tables not found")
        sys.exit(1)

    # Step 3: Ask if user wants to seed test data
    print("\n" + "=" * 50)
    print("\n🤔 Do you want to seed test data? (y/n): ", end="")
    response = input().lower()

    if response in ['y', 'yes']:
        if not await seed_test_data():
            print("\n⚠️  Warning: Failed to seed test data")
        else:
            print("\n" + "=" * 50)
            print("\n✨ Setup complete! You can now:")
            print("   1. Start the backend: uvicorn app.main:app --reload")
            print("   2. Visit API docs: http://localhost:8000/docs")
            print("   3. Login with test credentials")
    else:
        print("\n✅ Skipped test data seeding")

    print("\n" + "=" * 50)
    print("\n🎉 Backend quickstart validation complete!")


if __name__ == "__main__":
    asyncio.run(main())
