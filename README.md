# Kodi-Sync

Sync's watched libraries between multiple Kodi machines

External library to sync all watched movies & TV shows between multiple Kodi boxes, running multiple versions of Kodi, something a shared library on a mySQL server doesnt support.

Usage:
  Add/Edit servers list to match your environment
  python3 kodiwsync.py
  Optionally configure Cron task to do this repeatedily
  
To Do:
  Tidy code (currently only working proof of concept)
  Allow optional syncing of partial watches (currently only syncs completely)
  Allow options to be passed in via command line
  Support non-standard Kodi username passwords
  
