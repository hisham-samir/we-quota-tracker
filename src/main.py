import sys
from datetime import datetime
import re
import logging
import requests
from db import insert_record
from api_client import fetch_quota_data
from utils import tsConv, check_internet_connection


logging.basicConfig(level=logging.INFO)

check_internet_connection()


with requests.Session() as session:
    auth, result = fetch_quota_data(session)

    if auth is None:
        logging.error(result)
        sys.exit(1)

    qoutaBody = result

    offerName = qoutaBody["offerName"]
    totalGB = qoutaBody["total"]
    usedGB = qoutaBody["used"]
    remainGB = qoutaBody["remain"]
    usagePrc = usedGB / totalGB * 100
    renewedDate = tsConv(qoutaBody["effectiveTime"])[0]
    expiryDate = tsConv(qoutaBody["expireTime"], returnUntil=True)
    expDate = expiryDate[0]
    daysUntilExp = expiryDate[1]

    oneDayGB = totalGB / 30
    remainingDays = int(re.search(r'\d+', daysUntilExp).group())
    currentDay = 30 - remainingDays

    atLeastRemain = remainingDays * oneDayGB
    overAllState = "Under" if remainGB >= atLeastRemain else "Over"
    overAllStateGbs = abs(remainGB - atLeastRemain)
    stateDays = overAllStateGbs / oneDayGB

    # Write to DB after successful fetch
    now_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_success, dailyUsage = insert_record(
        now_datetime,
        currentDay,
        remainGB,
        overAllState,
        overAllStateGbs,
        stateDays,
        remainingDays
    )

    if db_success:
        logging.info("─── Quota Record Saved ───────────────────")
        logging.info("  Day            : %d", currentDay)
        logging.info("  Usage Today    : %.1f GB", dailyUsage)
        logging.info("  Remaining      : %.1f / %s GB (%.1f%% used)", remainGB, totalGB, usagePrc)
        logging.info("  Remaining Days : %d", remainingDays)
        logging.info("  Overall State  : %s by %.1f GB (%.1f days)", overAllState, overAllStateGbs, stateDays)
        logging.info("──────────────────────────────────────────")
    else:
        logging.error("Couldn't add record to database. Please check your DB connection and try again.")