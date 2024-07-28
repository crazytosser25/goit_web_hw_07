"""Module to generate database tables and fill them vith random data"""
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from creator.structure import create_structure
from creator.datum import generate_data


logging.basicConfig(
    level=logging.INFO,
    format='line_num: %(lineno)s > %(message)s'
)


DBSession = sessionmaker()

def main():
    """Main function to set up the database structure and generate data.
    """
    load_dotenv()
    database = os.getenv("DATABASE")
    engine = create_engine(
        url=database,
        echo=False
    )
    session = DBSession(bind=engine)

    create_structure(engine)
    logging.info('Structure created.')
    generate_data(session)
    logging.info('Data generated.')


if __name__ == "__main__":
    main()
