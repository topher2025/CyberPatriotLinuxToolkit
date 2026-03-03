# Remove read-only attribute from all files (including .git directory)
Get-ChildItem -Path . -Recurse -File -Force | ForEach-Object { if ($_.IsReadOnly) { $_.IsReadOnly = $false } }

# Remove read-only attribute from all directories (including .git)
Get-ChildItem -Path . -Recurse -Directory -Force | ForEach-Object { $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly) }
