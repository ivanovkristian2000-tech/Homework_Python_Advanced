from click import group
from sqlalchemy import create_engine, Integer, String, ForeignKey, Numeric, select, update, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from typing import Mapping

from sqlalchemy.sql import FROM_LINTING


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    products: Mapped[list['Product']] = relationship(back_populates='category')

    def __repr__(self):
        return (
            f"Category("
            f"id={self.id}, "
            f"name={self.name}, "
            f"description={self.description}"
            f")"
        )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return (
            f"Product("
            f"id={self.id}, "
            f"name={self.name}, "
            f"price={self.price}, "
            f"in_stock={self.in_stock}, "
            f"category_id={self.category_id}"
            f")"
        )


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with (Session() as session):
    electronics = Category(
        name="Электроника",
        description="Гаджеты и устройства."
    )

    books = Category(
        name="Книги",
        description="Печатные книги и электронные книги."
    )

    clothes = Category(
        name="Одежда",
        description="Одежда для мужчин и женщин."
    )

    smartphone = Product(
        name="Смартфон",
        price=299.99,
        in_stock=True,
        category=electronics
    )

    laptop = Product(
        name="Ноутбук",
        price=499.99,
        in_stock=True,
        category=electronics
    )

    sci_fi_book = Product(
        name="Научно-фантастический роман",
        price=15.99,
        in_stock=True,
        category=books
    )

    jeans = Product(
        name="Джинсы",
        price=40.50,
        in_stock=True,
        category=clothes
    )

    t_shirt = Product(
        name="Футболка",
        price=20.00,
        in_stock=True,
        category=clothes
    )
    session.add_all(
        [
            electronics,
            books,
            clothes,
            smartphone,
            laptop,
            sci_fi_book,
            jeans,
            t_shirt
        ]
    )
    session.commit()

    sql = select(Category)
    res = session.scalars(sql)
    for row in res:
        print(row.name)

        for product in row.products:
            print(product.name, product.price)

    sql = select(Product).where(Product.name == "Смартфон")
    product = session.scalars(sql).first()

    if product:
        product.price = 349.99
        session.commit()

    stmt = (
        select(Category.name, func.count(Product.id))
        .select_from(Category)
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.name)
    )

    res = session.execute(stmt).all()

    for category_name, count in res:
        print(category_name, count)

# SELECT c.name,
#           count(p.id)
#    FROM product AS p
#             JOIN
#         categories as c ON p.category_id = c.id
#    GROUP BY c.name

    sql = (
        select(
            Category.name, func.count(Product.id))
        .select_from(Product)
        .outerjoin(Category, Product.category_id == Category.id)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)

    )
    res = session.execute(sql).all()

    for category_name, count in res:
        print(category_name, count)
