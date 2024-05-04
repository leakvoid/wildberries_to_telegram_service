import datetime
import asyncio

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Float,
    Boolean,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)

def str_to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    def __init__(self, **kwargs):
        kwargs["date"] = str_to_datetime(kwargs["date"])
        kwargs["lastChangeDate"] = str_to_datetime(kwargs["lastChangeDate"])
        kwargs["cancelDate"] = str_to_datetime(kwargs["cancelDate"])
        super(Order, self).__init__(**kwargs)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    date: Mapped[datetime.datetime] = mapped_column(DateTime)
    lastChangeDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    warehouseName: Mapped[str] = mapped_column(String(50))
    countryName: Mapped[str] = mapped_column(String(200))
    oblastOkrugName: Mapped[str] = mapped_column(String(200))
    regionName: Mapped[str] = mapped_column(String(200))
    supplierArticle: Mapped[str] = mapped_column(String(75))
    nmId: Mapped[int] = mapped_column(Integer)
    barcode: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(50))
    subject: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    techSize: Mapped[str] = mapped_column(String(30))
    incomeID: Mapped[int] = mapped_column(Integer)
    isSupply: Mapped[bool] = mapped_column(Boolean)
    isRealization: Mapped[bool] = mapped_column(Boolean)
    totalPrice: Mapped[float] = mapped_column(Float)
    discountPercent: Mapped[int] = mapped_column(Integer)
    spp: Mapped[float] = mapped_column(Float)
    finishedPrice: Mapped[float] = mapped_column(Float)
    priceWithDisc: Mapped[float] = mapped_column(Float)
    isCancel: Mapped[bool] = mapped_column(Boolean)
    cancelDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    orderType: Mapped[str] = mapped_column(String)
    sticker: Mapped[str] = mapped_column(String)
    gNumber: Mapped[str] = mapped_column(String(50))
    srid: Mapped[str] = mapped_column(String) # original pk

class Sale(Base):
    __tablename__ = "sales"

    def __init__(self, **kwargs):
        kwargs["date"] = str_to_datetime(kwargs["date"])
        kwargs["lastChangeDate"] = str_to_datetime(kwargs["lastChangeDate"])
        super(Sale, self).__init__(**kwargs)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    date: Mapped[datetime.datetime] = mapped_column(DateTime)
    lastChangeDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    warehouseName: Mapped[str] = mapped_column(String(50))
    countryName: Mapped[str] = mapped_column(String(200))
    oblastOkrugName: Mapped[str] = mapped_column(String(200))
    regionName: Mapped[str] = mapped_column(String(200))
    supplierArticle: Mapped[str] = mapped_column(String(75))
    nmId: Mapped[int] = mapped_column(Integer)
    barcode: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(50))
    subject: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    techSize: Mapped[str] = mapped_column(String(30))
    incomeID: Mapped[int] = mapped_column(Integer)
    isSupply: Mapped[bool] = mapped_column(Boolean)
    isRealization: Mapped[bool] = mapped_column(Boolean)
    totalPrice: Mapped[float] = mapped_column(Float)
    discountPercent: Mapped[int] = mapped_column(Integer)
    spp: Mapped[float] = mapped_column(Float)
    paymentSaleAmount: Mapped[int] = mapped_column(Integer)
    forPay: Mapped[float] = mapped_column(Float)
    finishedPrice: Mapped[float] = mapped_column(Float)
    priceWithDisc: Mapped[float] = mapped_column(Float)
    saleID: Mapped[str] = mapped_column(String(15)) # original pk
    orderType: Mapped[str] = mapped_column(String)
    sticker: Mapped[str] = mapped_column(String)
    gNumber: Mapped[str] = mapped_column(String(50))
    srid: Mapped[str] = mapped_column(String)

# insert
async def insert_objects(async_session: async_sessionmaker[AsyncSession], objects) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(objects)

# select
async def select_objects(async_session: async_sessionmaker[AsyncSession], obj_type, time_limit) -> None:
    async with async_session() as session:
        result = await session.execute( select(obj_type).filter(obj_type.date >= time_limit) )

        return [u.__dict__ for u in result.scalars()]

# initialize the database
async def main() -> None:
    pass
    # db_credentials = 'user:password@hostname/database_name' # os.getenv['WB_DB_CREDENTIALS']
    # engine = create_async_engine(
    #     "postgresql+asyncpg://{db_credentials}/test",
    #     echo=True,
    # )

if __name__ == "__main__":
    asyncio.run(main())