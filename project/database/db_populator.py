from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser, ExtendedInterpolation
from project.database.models import Documents, Sections

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../config.ini')
PROJECT_DB_PATH = config['DATABASES']['PROJECT_DB_PATH']

# create object to query database
engine = create_engine(PROJECT_DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()


def db_populator(doc):
    # insert a document (one for each annual report)
    doc_row = Documents(
          path=doc.path
        , filename=doc.filename
        , year = int(doc.filename.split('_')[-1].replace('.docx',''))
        , document_text=doc.text
        , table_text=doc.table_text
        , author=doc.author
        , last_modified_by=doc.last_modified_by
        , created=doc.created
        , revision=doc.revision
        , num_tables=doc.num_tables
    )
    session.add(doc_row)

    # insert each document section
    sections = doc.get_sections_dict()
    for section_name, section_data in sections.items():
        section = Sections(
              filename=doc.filename
            , section_name=section_name
            , criteria=section_data['criteria']
            , section_text=section_data['text']
            , section_length=len(section_data['text'])
        )
        session.add(section)

    # commit (save) all annual report documents and sections to the database
    session.commit()
