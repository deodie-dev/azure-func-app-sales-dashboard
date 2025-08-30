# ActiveCampaign Azure PowerBI Integration

This project automates the extraction, synchronization, and storage of ActiveCampaign sales data into Azure SQL Database for PowerBI analytics. Built using Azure Functions, the solution periodically fetches deals, deal activities, and contact automations from ActiveCampaign, processes them, and updates the SQL database for downstream reporting.

---

## Tech Stack

- **ActiveCampaign API** – Fetches deals, deal activities, and contact automations.
- **Azure Function App** – Automates scheduled data synchronization.
- **Azure SQL Database** – Stores sales and automation data.
- **Python** – Primary programming language for all logic.
- **pyodbc** – SQL Server connectivity.
- **requests** – HTTP requests to ActiveCampaign API.

---

## Project Structure

```plaintext
.
├── function_app.py          # Azure Function timer trigger entry point
├── main.py                  # Orchestrates data sync logic
├── api_ac_functions.py      # ActiveCampaign API interaction logic
├── sql_functions.py         # SQL Server connection and data manipulation
├── util.py                  # Utility functions (e.g., date parsing)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

### `function_app.py`
- Main Azure Function trigger.
- Orchestrates the scheduled pipeline by calling `get_deal_data()`.

### `main.py`
- Connects to SQL Server.
- Fetches stage IDs, deals, activities, and automations.
- Determines whether to insert or update records.

### `api_ac_functions.py`
- Handles all ActiveCampaign API calls:
  - Get deal stages
  - Retrieve deal activities and contact automations (with pagination)

### `sql_functions.py`
- Connects to Azure SQL Server.
- Inserts and updates records in `tblDeals`, `tblDealActivities`, and `tblContactAutomations`.

### `util.py`
- Utility functions, such as robust date parsing.

---

## Workflow Overview

1. **Trigger**  
   Azure Function App triggers `function_app.py` on a schedule (every 30 minutes during specified hours, Mon-Fri).

2. **Fetch Stage IDs**  
   `api_ac_functions.get_stage_IDs()` pulls all deal stage IDs from ActiveCampaign.

3. **Process Deals**  
   For each stage, `main.get_deal_data()` fetches deals and determines if they should be inserted or updated in SQL.

4. **Sync Activities & Automations**  
   For each deal, fetches and syncs related activities and automations.

5. **Update Azure SQL Database**  
   `sql_functions.py` handles all insert and update operations.

---

## Environment Variables

Set the following environment variables in your Azure Function App settings or `.env` file for local testing:

```env
SQL_SERVER=
SQL_DATABASE=
SQL_USERNAME=
SQL_PASSWORD=
SQL_DRIVER={ODBC Driver 17 for SQL Server}
AC_API_TOKEN=
RUN_ON_STARTUP=False
USE_MONITOR=False
```

---

## Requirements

```bash
pip install -r requirements.txt
```

> Make sure to include `pyodbc`, `requests`, and `azure-functions`.

---

## Sample SQL Table Structures

```sql
CREATE TABLE tblDeals (
    deal_id INT PRIMARY KEY,
    hash NVARCHAR(255),
    owner NVARCHAR(255),
    contact INT,
    organization NVARCHAR(255),
    [group] NVARCHAR(255),
    stage NVARCHAR(255),
    title NVARCHAR(255),
    description NVARCHAR(MAX),
    [percent] FLOAT,
    cdate DATETIME,
    mdate DATETIME,
    nextdate DATETIME,
    nexttaskid INT,
    value FLOAT,
    currency NVARCHAR(10),
    winProbability FLOAT,
    winProbabilityMdate DATETIME,
    status NVARCHAR(50),
    activitycount INT,
    nextdealid INT,
    edate NVARCHAR(255)
);

CREATE TABLE tblDealActivities (
    d_id INT,
    d_stageid INT,
    userid INT,
    dataId INT,
    dataType NVARCHAR(50),
    dataAction NVARCHAR(50),
    dataOldval NVARCHAR(255),
    cdate DATETIME,
    sortdate DATETIME,
    isAddtask BIT,
    deleted BIT,
    seriesid INT,
    id INT PRIMARY KEY,
    deal INT,
    stage NVARCHAR(255),
    [user] NVARCHAR(255),
    automation NVARCHAR(255)
);

CREATE TABLE tblContactAutomations (
    contact INT,
    seriesid INT,
    startid INT,
    status NVARCHAR(50),
    batchid INT,
    adddate DATETIME,
    remdate DATETIME,
    timespan NVARCHAR(50),
    lastblock NVARCHAR(255),
    lastlogid INT,
    lastdate DATETIME,
    in_als BIT,
    completedElements INT,
    totalElements INT,
    completed BIT,
    completeValue FLOAT,
    id INT PRIMARY KEY,
    automation NVARCHAR(255)
);
```

---

## Deployment

All Python files are deployed inside an **Azure Function App**, which runs automatically on a timer trigger. Environment variables (e.g., SQL and API credentials) are stored securely in the Azure Function configuration settings.

---

## Logging

All critical steps and errors are logged using Python's `logging` module and can be viewed in Azure Function App logs.

---

## License

This project is for internal use. Please customize according to your organization’s policies.

---

## Author

Built by Deodie Picson as part of a sales analytics automation initiative. For inquiries or support, please contact deodie.dev@gmail.com.