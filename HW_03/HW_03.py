from sqlalchemy import create_engine, Integer, String, ForeignKey, Numeric, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped["Category"] = relationship(back_populates="products")


    def __repr__(self):
        return (
            f"Product("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"price={self.price}, "
            f"in_stock={self.in_stock}, "
            f"category_id={self.category_id}"
            f")"
        )


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list["Product"]] = relationship(back_populates="category")


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    new_category1 = Category(name='Phone', description='new super duper Phones buy it please')
    new_category2 = Category(name='Headphones', description='new super duper Headphones buy it please')
    new_product1 = Product(name='iPhon15', price=600, in_stock=True, category=new_category1)
    new_product2 = Product(name='Airpods', price=80, in_stock=True, category=new_category2)
    new_product3 = Product(name='iPhon16', price=700, in_stock=True, category=new_category1)
    session.add_all([new_category1, new_category2, new_product1, new_product2, new_product3])
    session.commit()

    sql = select(Product)
    rows = session.scalars(sql).all()
    for product in rows:
        print(product)
