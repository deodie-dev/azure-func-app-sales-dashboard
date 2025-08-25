import logging
import requests
import time, datetime
import os

AC_API_TOKEN = os.environ["AC_API_TOKEN"]
AC_HEADERS = { "accept": "application/json", "Api-Token": AC_API_TOKEN }

from sql_functions import *

def get_stage_IDs():

    url = "https://theoutperformer.api-us1.com/api/3/dealGroups/8/stages"  # Stages
    try:
        response = requests.get(url, headers=AC_HEADERS)
        response.raise_for_status()

        data = response.json()
        deals = data.get("dealStages", [])
        stage_IDs = []
        for deal in deals:
            logging.info(f"{deal.get('id')}: {deal.get('title')}")
            stage_IDs.append(deal.get("id"))
        return stage_IDs
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []



def get_contact_automations(conn, cursor, contact_id, max_id=None):
    offset = 0
    has_more = True
    should_update_deal = False

    while has_more:
        url = f"https://theoutperformer.api-us1.com/api/3/contacts/{contact_id}/contactAutomations?limit=100&offset={offset}"
        response = requests.get(url, headers=AC_HEADERS)
        # time.sleep(1)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        automations = data.get("contactAutomations", [])

        if not automations:
            print("No more contact automations found.")
            break
        
        for ca in automations:
            mID = int(ca.get('id'))
            print(f"AUTOMATION - API: {mID} | SQL Max ID: {max_id}")
            if max_id:
                if mID > max_id:
                    should_update_deal = True
                    insert_contact_automation(conn, cursor, ca)
                    print(f"Inserted automation ID: {ca.get('id')} for contact {contact_id}. Adddate is {ca.get('adddate')}")
            else:
                insert_contact_automation(conn, cursor, ca)
                print(f"Inserted automation ID: {ca.get('id')} for contact {contact_id}. Adddate is {ca.get('adddate')}")

        if len(automations) < 100:
            has_more = False
        else:
            offset += len(automations)

    return should_update_deal


def get_deal_activities(conn, cursor, deal_id, max_id=None):
    offset = 0
    has_more = True
    should_update_deal = False

    while has_more:
        url = f"https://theoutperformer.api-us1.com/api/3/deals/{deal_id}/dealActivities?limit=100&offset={offset}"
        response = requests.get(url, headers=AC_HEADERS)
        # time.sleep(1)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        activities = data.get("dealActivities", [])

        if not activities:
            print("No activities found.")
            break

        for activity in activities:
            mID = int(activity.get('id'))
            print(f"ACTIVITIES - API: {mID} | SQL Max ID: {max_id}")
            if max_id:
                if mID > max_id:
                    should_update_deal = True
                    insert_deal_activity(conn, cursor, activity)
                    print(f"Inserted activity ID: {activity.get('id')} for deal {deal_id}. Cdate is {activity.get('cdate')}")
            else:
                insert_deal_activity(conn, cursor, activity)
                print(f"Inserted activity ID: {activity.get('id')} for deal {deal_id}. Cdate is {activity.get('cdate')}")
                

        # Pagination check
        if len(activities) < 100:
            has_more = False
        else:
            offset += len(activities)

    return should_update_deal
