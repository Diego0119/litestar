from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    fullname: Mapped[str]

    items: Mapped[list["TodoItem"]] = relationship(back_populates="assigned_to")
    comments = relationship("Comment", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id},username={self.username},fullname={self.fullname})>"


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    done: Mapped[bool] = mapped_column(default=False, server_default="0")
    assigned_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    assigned_to: Mapped["User"] = relationship(back_populates="items")
    categories: Mapped[list["Category"]] = relationship(
        back_populates="items", secondary="items_categories"
    )
    comments = relationship("Comment", back_populates="todo_item")

    def __repr__(self) -> str:
        return f"<TodoItem(id={self.id},title={self.title},done={self.done})>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    items: Mapped[list["TodoItem"]] = relationship(
        back_populates="categories", secondary="items_categories"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id},name={self.name})>"


class ItemCategory(Base):
    __tablename__ = "items_categories"

    item_id: Mapped[int] = mapped_column(ForeignKey("todoitems.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    todo_item_id = Column(Integer, ForeignKey('todo_items.id'), nullable=False)
    user = relationship("User", back_populates="comments")
    todo_item = relationship("TodoItem", back_populates="comments")