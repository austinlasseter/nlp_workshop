from project.annual_report.report_downloader import AnnualReportDownloader
from project.documents.doc_extractor import extract_document_text
from project.database.db_populator import db_populator


def main():
    # identify and download new annual report (10-K) reports
    annual_report = AnnualReportDownloader(company='southwest-airlines-co')
    annual_report.get_annual_report_urls()
    annual_report.download_annual_reports()

    # extract, structure, and load the document into a database
    for doc in extract_document_text():
        db_populator(doc)


if __name__ == "__main__": main()
