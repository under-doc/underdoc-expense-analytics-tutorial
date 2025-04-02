from underdoc import underdoc_client, ExpenseExtractionBatchResponse
from model import MyExpense
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Running configurations
IMAGE_FILE_PATTERN = "receipt-images/*.*"
DB_FILE = "metabase-data/underdoc.db"

def extract_expense_data_from_images() -> ExpenseExtractionBatchResponse:
    logger.info("Extracting expense data from images - will take some time")
    # Remember to set the API key in the environment variable (export UNDERDOC_API_KEY=<your_api_key>)
    client = underdoc_client.Client()

    response = client.expense_image_batch_extract(
        file_name_pattern=IMAGE_FILE_PATTERN
    )

    logger.info(f"Extracted expense data from images completed successfully")

    return response

def extract_expense_data_to_db():
    logger.info("Extracting expense data and persist to DB")

    expense_batch_response = extract_expense_data_from_images()

    # Save expense data to DB
    engine = create_engine(f"sqlite:///{DB_FILE}")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for expense_with_source in expense_batch_response.expense_data_list:
            # Handle empty date
            if expense_with_source.expense_data.expense.date == '':
                expense_date = datetime.now()
            else:
                expense_date=datetime.fromisoformat(expense_with_source.expense_data.expense.date.replace("Z", "+00:00"))
            expense_data = MyExpense(
                date=expense_date,
                expense_type=expense_with_source.expense_data.image_type,
                shop_name=expense_with_source.expense_data.expense.shop_name,
                shop_address=expense_with_source.expense_data.expense.shop_address,
                expense_category=expense_with_source.expense_data.expense.expense_category,
                currency=expense_with_source.expense_data.expense.currency,
                total_amount=expense_with_source.expense_data.expense.total_amount,
                source_file_name=expense_with_source.source_file_name
            )
            session.add(expense_data)
        
        session.commit()

    logger.info("Expense data saved to DB")

if __name__ == "__main__":
    logger.info("UnderDoc Tutorial - Extract expense data from imagesand persist to DB")
    extract_expense_data_to_db()
