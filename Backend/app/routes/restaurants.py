import secrets
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Restaurant, APIKey
from ..schemas import RestaurantCreate, RestaurantResponse, RestaurantWithKey
from ..dependencies import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/", response_model=RestaurantWithKey)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db)
):
    restaurant = Restaurant(name=payload.name)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    api_key_value = secrets.token_hex(32)

    api_key = APIKey(
        key=api_key_value,
        restaurant_id=restaurant.id
    )

    db.add(api_key)
    db.commit()

    return {
        "restaurant": restaurant,
        "api_key": api_key_value
    }