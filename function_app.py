import logging
import azure.functions as func # type: ignore
from main import get_deal_data

app = func.FunctionApp()

# @app.timer_trigger(schedule="0 */15 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=True) 
@app.timer_trigger(schedule="0 */10 22-23,0-7 * * 1-5", arg_name="myTimer", run_on_startup=True, use_monitor=False) # Set to TRUE
def retrieve_active_campaign_data(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    get_deal_data()

    logging.info('Python timer trigger function executed.')

