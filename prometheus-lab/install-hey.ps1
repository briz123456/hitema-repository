New-Item -ItemType Directory -Force "$HOME\tools\hey" | Out-Null
Invoke-WebRequest `
  -Uri "https://storage.googleapis.com/hey-releases/hey_windows_amd64" `
  -OutFile "$HOME\tools\hey\hey.exe"

& "$HOME\tools\hey\hey.exe" -h
