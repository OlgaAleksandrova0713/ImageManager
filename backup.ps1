$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$backupFile = "backups/backup_$timestamp.sql"

docker compose exec -T db pg_dump `
    -U postgres `
    -d images_db `
    > $backupFile

Write-Host "Backup created successfully: $backupFile"