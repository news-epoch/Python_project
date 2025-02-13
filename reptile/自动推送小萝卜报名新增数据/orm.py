from sqlalchemy import Column, String, Integer, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class XiaoluoboInfo(Base):
    __tablename__ = "xiaoluoboInfo"
    id = Column(String(254), primary_key=True)
    title = Column(String(254))
    locationName = Column(String(254))
    attendCount = Column(Integer)
    count = Column(Integer)
    createdAt = Column(DateTime)
    endAt = Column(DateTime)
    locationAddress = Column(String(254))
    priceItems = Column(String(254))   # 报名金额


    def __init__(self, id, title, locationName, attendCount, count, createdAt, endAt, locationAddress, priceItems):
        # self.description = description
        self.locationAddress = locationAddress
        self.endAt = endAt
        self.createdAt = createdAt
        self.count = count
        self.attendCount = attendCount
        self.locationName = locationName
        self.id = id
        self.title = title
        self.priceItems = priceItems

    def to_dict(self):
        return dict(id=self.id, title=self.title, locationName=self.locationName,
                    attendCount=self.attendCount, count=self.count, createdAt=self.createdAt,
                    endAt=self.endAt, locationAddress=self.locationAddress, priceItems=self.priceItems)
