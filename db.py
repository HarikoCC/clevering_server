from sqlalchemy import Column, create_engine, DATETIME, BIGINT, Integer as INTEGER, String as VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base

from const import Mysql_addr, Mysql_user, Mysql_pass, Mysql_db

Base = declarative_base()


# 用户信息表
class UserInformation(Base):
    __tablename__ = 'user_info'
    user_id = Column(BIGINT, primary_key=True, nullable=False, index=True)
    user_name = Column(VARCHAR(50), primary_key=False, nullable=False)
    user_type = Column(INTEGER, primary_key=False, nullable=False)
    user_phone = Column(BIGINT, primary_key=False, nullable=True)
    user_password = Column(VARCHAR(50), primary_key=False, nullable=False)


# 用户状态报告表
class UserReport(Base):
    __tablename__ = 'user_report'
    report_id = Column(BIGINT, primary_key=True, nullable=False, index=True)
    user_id = Column(BIGINT, primary_key=False, nullable=False, index=True)
    report_path = Column(VARCHAR(50), primary_key=False, nullable=False)
    create_time = Column(DATETIME, primary_key=False, nullable=False)


# 设备绑定表
class UserDevice(Base):
    __tablename__ = 'user_device'
    binding_id = Column(INTEGER, primary_key=True, nullable=False, index=True)
    user_id = Column(BIGINT, primary_key=False, nullable=False, index=True)
    device_id = Column(BIGINT, primary_key=False, nullable=False, index=True)
    device_name = Column(VARCHAR(50), primary_key=False, nullable=False)


# 用户实时状态表
class UserStatus(Base):
    __tablename__ = 'user_status'
    user_id = Column(BIGINT, primary_key=True, nullable=False, index=True)
    heart_rate = Column(INTEGER, primary_key=False, nullable=True)
    hrv = Column(INTEGER, primary_key=False, nullable=True)
    blood_oxygen = Column(INTEGER, primary_key=False, nullable=True)
    concentration = Column(INTEGER, primary_key=False, nullable=True)
    modify_time = Column(DATETIME, primary_key=False, nullable=True)


# 用户状态日志表
class StatusRecord(Base):
    __tablename__ = 'status_record'
    record_id = Column(BIGINT, primary_key=True, nullable=False, index=True)
    user_id = Column(BIGINT, primary_key=False, nullable=False, index=True)
    heart_rate = Column(INTEGER, primary_key=False, nullable=True)
    hrv = Column(INTEGER, primary_key=False, nullable=True)
    blood_oxygen = Column(INTEGER, primary_key=False, nullable=True)
    concentration = Column(INTEGER, primary_key=False, nullable=True)
    timestamp = Column(DATETIME, primary_key=False, nullable=False)


# 文件信息表
class FileInfo(Base):
    __tablename__ = 'file_info'
    file_id = Column(INTEGER, primary_key=True, nullable=False)
    file_name = Column(VARCHAR(50), primary_key=False, nullable=False, index=True)
    user_id = Column(BIGINT, primary_key=True, nullable=False)
    create_time = Column(DATETIME, primary_key=False, nullable=False)
    modify_time = Column(DATETIME, primary_key=False, nullable=False)


# 用户组表
class UserGroup(Base):
    __tablename__ = 'user_group'
    group_id = Column(INTEGER, primary_key=True, nullable=False, index=True)
    group_name = Column(VARCHAR(50), primary_key=False, nullable=False)
    user_id = Column(BIGINT, primary_key=False, nullable=False, index=True)


# 文件授权表
class FileGroup(Base):
    __tablename__ = 'file_group'
    file_id = Column(INTEGER, primary_key=True, nullable=False)
    group_id = Column(INTEGER, primary_key=False, nullable=False, index=True)
    permission = Column(INTEGER, primary_key=False, nullable=True)


link = f"mysql+pymysql://{Mysql_user}:{Mysql_pass}@{Mysql_addr}/{Mysql_db}"


def init_db():
    engine = create_engine(
        link,
        echo=True
    )
    Base.metadata.create_all(engine)


class DbSession:
    def __init__(self):
        engine = create_engine(link)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_session(self):
        return self.session

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    init_db()
