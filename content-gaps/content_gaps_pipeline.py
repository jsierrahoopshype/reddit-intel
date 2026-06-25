name: NBA content gaps from Reddit

on:
  schedule:
    # 06:30 UTC daily. Madrid is UTC+1 (winter) / UTC+2 (summer), so this lands
    # roughly 07:30-08:30 local. GitHub cron is always UTC and does not adjust
    # for daylight saving; shift this line if you want a fixed local time.
    - cron: "30 6 * * *"
  workflow_dispatch: {}   # lets you trigger a run manually from the Actions tab

jobs:
  content-gaps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: pip install -r content-gaps/requirements.txt

      - name: Run pipeline
        env:
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          REDDIT_USER_AGENT: ${{ secrets.REDDIT_USER_AGENT }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          # Only needed if you switch LLM_PROVIDER to "claude":
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          # Optional overrides:
          LLM_PROVIDER: "gemini"
          # GEMINI_MODEL: "gemini-2.5-flash"
          # TEAM_SUBS: "NBASpurs,torontoraptors"
        run: python content-gaps/content_gaps_pipeline.py
