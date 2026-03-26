# we-quota-tracker

A Python automation tool that tracks your **WE (Telecom Egypt) home internet quota** daily and logs usage data to a PostgreSQL database. Can be run locally or fully automated via GitHub Actions.

---

## Table of Contents

- [How it works](#how-it-works)
- [Automated Daily Runs](#automated-daily-runs)
- [How to Run Locally](#how-to-run-locally)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## How it works

1. Authenticates with the WE API using your landline credentials.
2. Fetches your current quota details.
3. Calculates your daily usage and whether you are over or under your expected overall usage.
4. Logs a row to a PostgreSQL `quota_log` table.
5. Runs automatically every day via GitHub Actions scheduled workflow.

> **Note:** On the 1st day of every cycle, the table is automatically cleared for a fresh monthly log.

| Column           | Type     | Description                              |
| ---------------- | -------- | ---------------------------------------- |
| `id`             | SERIAL        | Auto-incremented primary key             |
| `date_time`      | TIMESTAMP     | Timestamp of the record                  |
| `day`            | INT           | Current day in the quota cycle (1–30)    |
| `usage_gbs`      | NUMERIC(10,1) | GBs used in this day                     |
| `remaining_gbs`  | NUMERIC(10,1) | Remaining quota at time of record        |
| `overall_state`  | VARCHAR(50)   | `Under` or `Over` expected overall usage |
| `state_gbs`      | NUMERIC(10,1) | How many GBs under or over               |
| `state_days`     | NUMERIC(10,1) | How many days ahead or behind your expected usage pace |
| `remaining_days` | INT           | Days left until quota renewal            |

---

## Automated Daily Runs

### 1. Fork or push the repo to GitHub

### 2. Set up a PostgreSQL database

You can use any PostgreSQL database you already have. If you don't have one, you'll need a cloud-hosted database so the script can connect to it from GitHub Actions.

**My recommendation: [Neon](https://neon.tech)**

Neon is a free cloud-hosted PostgreSQL database. Since both GitHub Actions and Neon are on the cloud, the script runs fully automatically with nothing running on your machine — no local database, no local server, nothing to worry about.

Here's how to get started with Neon:

1. Go to [neon.tech](https://neon.tech) and create a free account.
2. Click **New Project** and give it a name.
3. Once created, go to **Connection Details**.
4. Copy the connection string — it looks like:

   ```
   postgresql://user:password@host/dbname?sslmode=require
   ```

5. Use this as your `DATABASE_URL` in the next step.

### 3. Add your secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add each of the following:

| Secret Name    | Description                        |
| -------------- | ---------------------------------- |
| `LND_NUMBER`   | Your WE landline number            |
| `LND_PASS`     | Your WE password                   |
| `START_GB`     | Your total monthly quota in GB     |
| `DATABASE_URL` | Your PostgreSQL connection string  |

> **Note:** Secret names are case-sensitive. They must match exactly as shown above.

### 4. You're all set!

That's everything — the workflow is ready to go. It will run automatically every day at **9 PM Cairo time (UTC+2)** without any further setup.

To test it or trigger it manually at any time, go to the **Actions** tab → **Daily Quota Tracker** → **Run workflow**.

---

## How to Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Kareem74x/we-quota-tracker.git
cd we-quota-tracker
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create a `.env` file** in the project root with the following variables:

```env
# WE account credentials
LND_NUMBER=0123456789       # Your WE landline number
LND_PASS=yourpassword       # Your WE password

# Quota settings
START_GB=100                # Your quota size in GB

# PostgreSQL connection string
# Works with any PostgreSQL provider: Neon, Supabase, Railway, or self-hosted
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

**4. Run the script**

```bash
python main.py
```

Logs will print to the console and a record will be inserted into your database.

---

## Acknowledgements

The API request and authentication logic in this project was adapted from [TE-QuotaCheck](https://github.com/karimawi/TE-QuotaCheck) by [karimawi](https://github.com/karimawi).

---

## License

This project is licensed under the [MIT License](LICENSE).