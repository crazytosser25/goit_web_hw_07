"""Module to generate database tables and fill them vith random data"""
import logging
from sqlalchemy import create_engine
from creator.structure import create_structure
from creator.datum import generate_data


logging.basicConfig(
    level=logging.INFO,
    format='line_num: %(lineno)s > %(message)s'
)

def main():
    database = 'postgresql://postgres:mysecretpassword@localhost:5432'
    engine = create_engine(database, echo=True)

    create_structure(engine)
    logging.info('Structure created.')
    generate_data(engine)
    logging.info('Data generated.')


if __name__ == "__main__":
    main()
