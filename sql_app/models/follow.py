from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from database import Base


class Follow(Base):
    __tablename__ = 'followage'

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    followee_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(Time)

    user_follower = relationship('User', back_populates='following')
    user_followee = relationship('User', back_populates='followers')

# Follow
# id (primary key)
# follower_id (foreign key to User)
# following_id (foreign key to User)
# created_at
