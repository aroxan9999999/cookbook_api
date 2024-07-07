from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas


async def get_recipe(db: AsyncSession, recipe_id: int):
    result = await db.execute(
        select(models.Recipe).filter(models.Recipe.id == recipe_id)
    )
    return result.scalar_one_or_none()


async def get_recipes(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Recipe)
        .order_by(models.Recipe.views.desc(), models.Recipe.cook_time)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_recipe(db: AsyncSession, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
