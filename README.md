# QuickBooks QODBC → MySQL pipeline

## Client machine (QuickBooks + QODBC)

1. Install [Git](https://git-scm.com/download/win) if needed.
2. Clone this repository (use a **private** repo URL from GitHub):

   ```bash
   git clone <your-repo-url>
   cd workforce-data-automation
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   copy .env.example .env
   ```

   Edit `.env` with the client’s QODBC DSN/driver and MySQL settings. Do **not** commit `.env`.

5. Run a job:

   ```bash
   python main.py --job usa_inventory_evaluation_summary
   ```

## Updating the code on the client

After you push changes from your dev machine:

```bash
git pull
```

Re-run `pip install -r requirements.txt` only if `requirements.txt` changed.

## Pushing from your dev machine (first time)

1. On GitHub: **New repository** → name it (e.g. `workforce-data-automation`) → **Private** → create **without** README (this project already has files).
2. In the project folder:

   ```bash
   git remote add origin https://github.com/<your-org-or-user>/<repo>.git
   git branch -M main
   git push -u origin main
   ```

Use SSH remote URLs if you prefer: `git@github.com:...`
