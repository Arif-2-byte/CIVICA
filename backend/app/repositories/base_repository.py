from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ):
        return (
            db.query(self.model)
            .filter(self.model.id == obj_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
    ):
        return db.query(self.model).all()

    def create(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.commit()
        db.refresh(obj)
        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.delete(obj)
        db.commit()