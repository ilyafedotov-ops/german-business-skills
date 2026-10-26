# Complete workspace backup and recovery

Use a full workspace backup before changing real records through a new interface,
upgrading protected record formats, or moving computers. A document archive is a
separate delivery artifact; it omits workspace state and is not a recovery copy.

The assistant performs the commands and explains the result. Ask the user to
choose a protected backup location outside the working workspace, source checkout
and installed skill. Use an existing local parent directory and a new destination
name. These utilities require no network or service connection. They copy private
business data in readable files; storage encryption, Windows ACLs, off-site
retention and access controls must be chosen and checked separately.

## Windows without Python

Run these examples from the installed skill directory with Windows PowerShell 5.1,
or use the script’s absolute path. Do not install another runtime or bypass
execution policy for this workflow.

```powershell
& .\scripts\recovery.ps1 -Action backup -Root 'C:\Users\NAME\Documents\Business' -Destination 'D:\Protected backups\Business-2026-10-26'
& .\scripts\recovery.ps1 -Action verify -Backup 'D:\Protected backups\Business-2026-10-26'
& .\scripts\recovery.ps1 -Action restore -Backup 'D:\Protected backups\Business-2026-10-26' -Root 'C:\Users\NAME\Documents\Business-restored'
& .\scripts\windows.ps1 -Action verify -Root 'C:\Users\NAME\Documents\Business-restored'
```

## An existing supported Python runtime

Run from the skill directory, or use absolute script paths.

```sh
python3 -B scripts/recovery.py backup --root '/private/Business' --destination '/protected/Business-2026-10-26'
python3 -B scripts/recovery.py verify --backup '/protected/Business-2026-10-26'
python3 -B scripts/recovery.py restore --backup '/protected/Business-2026-10-26' --root '/private/Business-restored'
python3 -B scripts/workspace.py doctor --root '/private/Business-restored'
```

The directory format is shared by both runtimes. A backup contains
`manifest.json` and `files/`, which holds the complete workspace tree, including
hidden metadata, original documents, the language descriptor, journal and filing
records, evidence, history, notes and empty directories. The manifest lists each
relative file path, byte size and SHA-256, all directories, a backup ID and creation
time. Only the active root `.workspace.lock` is excluded. Do not move individual
members, edit the manifest, or combine two backups.

## What counts as complete

1. Backup obtains the normal workspace lock, copies every member, checks that the
   source tree did not change, and verifies the saved tree before returning
   `status: verified`. An active or stale lock stops the operation; investigate it
   rather than deleting it automatically.
2. Verification rejects missing, extra, altered, linked, unsafe or colliding
   members. A portable backup cannot contain Windows-reserved names or paths that
   differ only by case. Unsupported source paths cause an explicit stop; they are
   never silently omitted.
3. Restore verifies the backup before creating the destination and writes only
   to a new private directory. It refuses an existing destination. It checks the
   restored bytes and workspace identity, then reports original integrity. The
   Python route also returns the existing workspace diagnostics.
4. Inspect the restored overview, profile, selected documents, latest records and
   diagnostics before resuming. Preserve the backup and old workspace. Do not
   delete either because a copy or hash check succeeded.

`verified` confirms the saved bytes and paths, not tax correctness, completeness
of the underlying accounting period, or authenticity against a trusted signed
source. A damaged workspace can be preserved faithfully; restoration does not
repair its original evidence or grant filing approval. If copying fails, retain
the partial destination for inspection and retry under a new name. A directory
without a successfully verified manifest is not a completed backup.
