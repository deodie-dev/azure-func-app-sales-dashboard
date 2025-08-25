import logging
import requests, time # type: ignore
import os

from sql_functions import *
from api_ac_functions import *

AC_API_TOKEN = os.environ["AC_API_TOKEN"]
AC_HEADERS = { "accept": "application/json", "Api-Token": AC_API_TOKEN }


def get_deal_data():

    conn, cursor = connect_to_sql()

    stage_ID_list = get_stage_IDs()
    deals_list = get_deals_list(conn, cursor)
    deals_last_cdate_dict = get_deal_activities_max_id(conn, cursor)
    deals_last_adddate_dict = get_deal_automation_max_id(conn, cursor)
    
    for stage_ID in stage_ID_list:
        # if stage_ID != '67': continue
        logging.info(f"------------------------------------------------------------- Processing stage: {stage_ID}")
        offset = 0
        has_more = True

        while has_more:
            url = f"https://theoutperformer.api-us1.com/api/3/deals?filters[group]=8&filters[stage]={stage_ID}&limit=100&offset={offset}"
            time.sleep(.5)
            response = requests.get(url, headers=AC_HEADERS)
            if response.status_code != 200:
                logging.error(f"Error: {response.status_code} - {response.text}")
                break

            try:
                data = response.json()
                deals = data.get("deals", [])

                if not deals:
                    logging.info("No deals found.")
                    break

                for deal in deals:

                    deal_id = deal['id']
                    contact_id = deal['contact']
                    deal_title = deal.get('title')

                    if int(deal_id) in deals_list:
                        logging.info(f"Checking deal ID: {deal_id}: {deal_title}")

                        max_activity_id = deals_last_cdate_dict.get(int(deal_id))
                        need_to_update_a = get_deal_activities(cursor, conn, deal_id, max_activity_id)

                        max_automation_id = deals_last_adddate_dict.get(int(contact_id))
                        need_to_update_b = get_contact_automations(cursor, conn, contact_id, max_automation_id)

                        if need_to_update_a or need_to_update_b:
                            logging.info(f"Updating deal ID: {deal_id}: {deal_title}")
                            update_deal(cursor, conn, deal)

                    else:
                        logging.info(f"Inserting deal with ID: {deal_id}: {deal_title}")
                        insert_deal(conn, deal)

                        get_deal_activities(cursor, conn, deal_id)
                        get_contact_automations(cursor, conn, contact_id)

            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                break

            # Check if we've reached the end
            if len(deals) < 100:
                has_more = False
            else:
                offset += len(deals)

    cursor.close()
    conn.close()



