import logging
import pyodbc 
import os

from util import parse_date

# Database connection parameters from environment variables
server = os.environ["SQL_SERVER"]
database = os.environ["SQL_DATABASE"]
username = os.environ["SQL_USERNAME"]
password = os.environ["SQL_PASSWORD"]
driver = os.environ["SQL_DRIVER"]

# Function to connect to the SQL database
def connect_to_sql():
    try:
        connection_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
        conn = pyodbc.connect(connection_str)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        logging.error(f"Error connecting to SQL database: {e}")
        return None, None


# Function to insert a deal into the database
def insert_deal(conn, deal):

    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO tblDeals (deal_id, hash, owner, contact, organization, [group], 
        stage, title, description, [percent], cdate, mdate, nextdate, nexttaskid, 
        value, currency, winProbability, winProbabilityMdate, status, activitycount, 
        nextdealid, edate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (
            deal['id'],
            deal['hash'],
            deal['owner'],
            deal['contact'],
            deal['organization'],
            deal['group'],
            deal['stage'],
            deal['title'],
            deal['description'],
            deal['percent'],
            parse_date(deal['cdate']),
            parse_date(deal['mdate']),
            parse_date(deal['nextdate']),
            deal['nexttaskid'],
            deal['value'],
            deal['currency'],
            deal['winProbability'],
            parse_date(deal['winProbabilityMdate']),
            deal['status'],
            deal['activitycount'],
            deal['nextdealid'],
            deal['edate']
        ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting deal {deal.get('id')}: {e}")
        return False


def insert_deal_activity(conn, cursor, activity):

    try:
        insert_query = """
            INSERT INTO tblDealActivities (
                d_id, d_stageid, userid, dataId, dataType, dataAction, dataOldval,
                cdate, sortdate, isAddtask, deleted, seriesid, id, deal, stage, [user], automation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (
            activity.get("d_id"),
            activity.get("d_stageid"),
            activity.get("userid"),
            activity.get("dataId"),
            activity.get("dataType"),
            activity.get("dataAction"),
            activity.get("dataOldval"),
            parse_date(activity.get("cdate")),
            parse_date(activity.get("sortdate")),
            activity.get("isAddtask"),
            activity.get("deleted"),
            activity.get("seriesid"),
            activity.get("id"),
            activity.get("deal"),
            activity.get("stage"),
            activity.get("user"),
            activity.get("automation"),
        ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting deal activity {activity.get('id')}: {e}")
        return False
    

def insert_contact_automation(conn, cursor, ca):

    try:
        insert_query = """
            INSERT INTO tblContactAutomations (
                contact, seriesid, startid, status, batchid, adddate, remdate,
                timespan, lastblock, lastlogid, lastdate, in_als,
                completedElements, totalElements, completed, completeValue, id, automation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (
            ca.get("contact"),
            ca.get("seriesid"),
            ca.get("startid"),
            ca.get("status"),
            ca.get("batchid"),
            parse_date(ca.get("adddate")),
            parse_date(ca.get("remdate")),
            ca.get("timespan"),
            ca.get("lastblock"),
            ca.get("lastlogid"),
            parse_date(ca.get("lastdate")),
            ca.get("in_als"),
            ca.get("completedElements"),
            ca.get("totalElements"),
            ca.get("completed"),
            ca.get("completeValue"),
            ca.get("id"),
            ca.get("automation"),
        ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting contact automation {ca.get('id')}: {e}")
        return False
    

def update_deal (cursor, conn, deal):
    try:
        update_sql = f"""
            UPDATE tblDeals
            SET owner = ?, contact = ?, organization = ?, stage = ?, title = ?, description = ?, 
            [percent] = ?, cdate = ?, mdate = ?, nextdate = ?, nexttaskid = ?, value = ?, 
            currency = ?, winProbability = ?, winProbabilityMdate = ?, status = ?, 
            activitycount = ?, nextdealid = ?, edate = ?
            WHERE deal_id = ? """
        cursor.execute(update_sql, (deal['owner'], deal['contact'], deal['organization'], deal['stage'], deal['title'], deal['description'], deal['percent'], parse_date(deal['cdate']), parse_date(deal['mdate']), parse_date(deal['nextdate']), deal['nexttaskid'], deal['value'], deal['currency'], deal['winProbability'], parse_date(deal['winProbabilityMdate']), deal['status'], deal['activitycount'], deal['nextdealid'], deal['edate'], deal['id']) )
        
        conn.commit()
        return True
    
    except Exception as sql_execution_error:
        logging.error(f"Error while updating event {deal['id']} in the database: {sql_execution_error}")
        return False


def get_deals_list(conn, cursor):

    try:
        select_query = "SELECT deal_id FROM tblDeals"
        cursor.execute(select_query)
        deals = [row[0] for row in cursor.fetchall()]

        deals_list = []
        for deal in deals:
            deals_list.append(deal)
        logging.info(f"Total Number of deals: {len(deals_list)}")

        return deals_list
    except Exception as e:
        logging.error(f"Error fetching deals list: {e}")
        return []


def get_deal_activities_max_id(conn, cursor):

    select_query = """
        SELECT d_id, MAX(id) AS max_id
        FROM tblDealActivities
        GROUP BY d_id
    """
    cursor.execute(select_query)
    deals_dict = {row[0]: row[1] for row in cursor.fetchall()}
    # logging.info(deals_dict)
    return deals_dict

# git test
def get_deal_automation_max_id(conn, cursor):

    select_query = """
        SELECT contact, MAX(id) AS max_id
        FROM tblContactAutomations
        GROUP BY contact
    """
    cursor.execute(select_query)
    deals_dict = {row[0]: row[1] for row in cursor.fetchall()}
    # logging.info(deals_dict)
    return deals_dict