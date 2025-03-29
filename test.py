from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db import sqlLink, FileInformation, UserInformation
from serializer.file_manager import all_file_dict_list


class DbSession:
    def __init__(self):
        engine = create_engine(sqlLink)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

        async def get_session(self) -> AsyncSession:
            return self.session()

        async def close(self):
            await self.engine.dispose()

if __name__ == "__main__":
    db=DbSession()
    result = db.session.query(FileInformation, UserInformation).join(UserInformation,
                                                                            FileInformation.user_id == UserInformation.user_id).all()
    print(all_file_dict_list(result))