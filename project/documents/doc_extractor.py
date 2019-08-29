import os
import logging
from logging.config import fileConfig
from configparser import ConfigParser, ExtendedInterpolation
from project.documents.document import Document

# configuration
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../config.ini')
IN_PROGRESS_PATH = config['DOCX']['IN_PROGRESS_PATH']

# logging configuration
fileConfig('logging_config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def extract_document_text():
    num_docs_to_process = len(os.listdir(IN_PROGRESS_PATH))
    logger.info('begin processing {} new annual report(s)'.format(num_docs_to_process))

    for path in os.listdir(IN_PROGRESS_PATH):
        logger.info('start processing: {}'.format(path))

        document = Document(path)
        yield document

        # move document from in_progress dir to completed dir
        # after all file processing is complete
        os.rename(document.path, document.completed_path)

        logger.info('complete processing: {}'.format(document.filename))
