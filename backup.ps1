$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$backupFile = "backups/backup_$timestamp.sql"

docker compose exec -T db pg_dump `
    -U postgres `
    -d images_db `
    > $backupFile

if ($LASTEXITCODE -eq 0) {

    $logMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') INFO Backup created successfully: $backupFile"

    $logPath = "logs/app.log"

    $stream = [System.IO.FileStream]::new(
        $logPath,
        [System.IO.FileMode]::OpenOrCreate,
        [System.IO.FileAccess]::Write,
        [System.IO.FileShare]::ReadWrite
    )

    $stream.Seek(0, [System.IO.SeekOrigin]::End)

    $writer = [System.IO.StreamWriter]::new($stream)
    $writer.WriteLine($logMessage)
    $writer.Close()
    $stream.Close()

    Write-Host "Backup created successfully: $backupFile"

} else {

    $logMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ERROR Backup failed"

    $logPath = "logs/app.log"

    $stream = [System.IO.FileStream]::new(
        $logPath,
        [System.IO.FileMode]::OpenOrCreate,
        [System.IO.FileAccess]::Write,
        [System.IO.FileShare]::ReadWrite
    )

    $stream.Seek(0, [System.IO.SeekOrigin]::End)

    $writer = [System.IO.StreamWriter]::new($stream)
    $writer.WriteLine($logMessage)
    $writer.Close()
    $stream.Close()

    Write-Host "Backup failed"

    exit 1
}