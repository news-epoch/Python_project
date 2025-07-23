from sqlalchemy import Column, Text, Integer, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class XiaoluoboInfo(Base):
    __tablename__ = "xiaoluoboInfo"
    id = Column(Text, primary_key=True)
    title = Column(Text)
    locationName = Column(Text)
    attendCount = Column(Integer)
    count = Column(Integer)
    createdAt = Column(Text)
    endAt = Column(Text)
    locationAddress = Column(Text)
    priceItems = Column(Text)   # 报名金额
    targetOrgName = Column(Text)


    def __init__(self, id, title, locationName, attendCount, count, createdAt, endAt, locationAddress, priceItems, targetOrgName):
        # self.description = description
        self.targetOrgName = targetOrgName
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
                    endAt=self.endAt, locationAddress=self.locationAddress, priceItems=self.priceItems, targetOrgName=self.targetOrgName)
