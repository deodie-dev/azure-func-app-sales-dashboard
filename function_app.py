import logging
import azure.functions as func # type: ignore
from main import get_deal_data

import os
bool_run_on_startup = os.getenv("RUN_ON_STARTUP", "False").lower() in ("true", "1", "t")
bool_use_monitor =os.getenv("USE_MONITOR", "False").lower() in ("true", "1", "t")

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */30 22-23,0-7 * * 1-5", arg_name="myTimer", run_on_startup=bool_run_on_startup, use_monitor=bool_use_monitor)
def retrieve_active_campaign_data(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    get_deal_data()

    logging.info('Python timer trigger function executed.')

