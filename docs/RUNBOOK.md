# Developer runbook

> **Status:** Commands derived from inspected manifests and repository layout. They are not evidence of a successful installation or running application.

## Development setup

```powershell
cd eda-webapp/backend
python -m venv .venv
python -m pip install -r requirements.txt
python app.py
```

## Additional service / build commands

```powershell
cd eda-webapp/frontend
npm ci
npm run dev
```

Run commands in the indicated project directory. Use separate terminals for services when appropriate. On Windows PowerShell, `cd` changes the working directory; return to the repository root before starting another subproject. Where a command depends on a previous directory, ensure that directory is selected.

## Prerequisites and limitations

Activate the Python virtual environment before installing packages. Confirm API URL in frontend/src/api.js.

Install supported runtime versions, use the repository lockfile where available, and configure local environment variables with **dummy or personal development credentials only**. Do not copy real secrets into GitHub or screenshots.

## Verification checklist

- [ ] Record the commit SHA and OS/runtime versions.
- [ ] Install dependencies successfully; note warnings.
- [ ] Start every required service; record actual startup output.
- [ ] Confirm the UI or API is reachable on the **actual** reported port (do not assume a port).
- [ ] Exercise a happy-path workflow and a controlled failure case with synthetic data.
- [ ] Run existing tests and record exact commands/results; mark missing tests explicitly.
- [ ] Capture real screenshots with sensitive content removed.
- [ ] Confirm README links, screenshot captions and architecture notes match observed behavior.

## Troubleshooting

- **Missing runtime:** Check `node --version`, `npm --version`, `python --version` or `dotnet --info` as applicable.
- **Dependency errors:** Check lockfile compatibility, native build prerequisites and package-manager versions.
- **Database or service unavailable:** Check local service state, connection strings and firewall settings; never paste secrets into logs.
- **Frontend loads but API fails:** Confirm API URL, CORS and backend process status.
- **No screenshot:** If the application did not start, document the blocker rather than using an invented image.

## Security gate before publishing

Use synthetic datasets for screenshots and test uploads.

**Do not merge or deploy if credentials may still be active and exposed.** Rotate/revoke credentials at their providers, remove sensitive files from tracking and evaluate Git history cleanup. History rewriting can affect collaborators and must be coordinated.

## Evidence status

| Activity | Result |
|---|---|
| Source/manifest inspection | Completed |
| Runtime installation | Not performed |
| Startup | Not verified |
| Functional testing | Not performed |
| Screenshots | Not captured |
