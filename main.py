from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import Base, engine, get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/recipes", response_model=list[schemas.Recipe])
async def read_recipes(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    recipes = await crud.get_recipes(db, skip=skip, limit=limit)
    return recipes


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def read_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    db_recipe = await crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@app.post("/recipes", response_model=schemas.Recipe)
async def create_recipe(
    recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_recipe(db=db, recipe=recipe)
