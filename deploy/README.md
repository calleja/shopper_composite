# Deploying shopper-ingest on radish

Project path on the droplet: `/home/lcalleja/shopper_composite`.

Install the crontab yourself; this directory only ships the reference file
`crontab.example`. Keep that file in sync when you change the schedule, and
commit it so the schedule is versioned.

## One-time setup

1. Pull the code:

   ```bash
   cd /home/lcalleja/shopper_composite && git pull
   ```

2. Install the package and console script:

   ```bash
   uv sync
   ```

   This creates `.venv` and registers `shopper-ingest` from `[project.scripts]`
   in `pyproject.toml`.

3. Secrets. Create `/home/lcalleja/shopper_composite/secrets.yaml` (this is the
   default `--secrets` path). Quote the password so YAML does not treat a
   numeric password as an integer:

   ```yaml
   host: "localhost"
   user: "lcalleja2"
   password: "your-password"
   database: "membership_ard"
   port: 3306
   ```

   `secrets.yaml` and `secrets/` are already in `.gitignore`.

4. Logs directory (for cron stdout/stderr):

   ```bash
   mkdir -p /home/lcalleja/shopper_composite/logs
   ```

   The Python log file stays as configured in
   `src/shopper_composite/logging_reference.py` (`log_testing.log`). Because the
   cron line `cd`s into the project first, that file lands in the project root.

5. Smoke test by hand, exactly as cron will run it:

   ```bash
   cd /home/lcalleja/shopper_composite && uv run shopper-ingest; echo "exit=$?"
   ```

   Expect `exit=0`. Then confirm in MySQL: `SELECT MAX(date) FROM shopper_log;`.

6. Find the absolute path to `uv` (cron's PATH is minimal):

   ```bash
   which uv
   ```

   Typically `/home/lcalleja/.local/bin/uv`. If different, edit the path in
   `deploy/crontab.example` before installing.

## Install the crontab

Your crontab starts empty (`crontab -e` reported "no crontab for lcalleja").

**Option A — interactive (nano):**

```bash
crontab -e
```

At the editor prompt, choose `1` (`/bin/nano`). Paste the contents of
`deploy/crontab.example`, then save and exit: `Ctrl+O`, `Enter`, `Ctrl+X`.

**Option B — non-interactive (safe only while the crontab is empty):**

```bash
crontab /home/lcalleja/shopper_composite/deploy/crontab.example
```

`crontab <file>` replaces the entire crontab. Do not use this once you have
other jobs.

## Verify

```bash
crontab -l
systemctl status cron
```

After the first scheduled run (02:15 local time):

```bash
tail /home/lcalleja/shopper_composite/logs/cron.out
grep CRON /var/log/syslog | tail
# or: journalctl -u cron -n 20
```

## Editing later

```bash
crontab -e
```

Save and exit; cron reloads automatically. Mirror any schedule/command change
back into `deploy/crontab.example` and commit it.
