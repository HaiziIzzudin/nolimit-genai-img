git add .
git commit -m "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")"
git push
$remoteCommand = "cd /home/haizi/nolimit-gen-ai-images/ && git pull"
$securePassword = ConvertTo-SecureString "Haizzudin02" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ("haizi", $securePassword)
Invoke-Command -ComputerName "139.162.55.58" -Credential $cred -ScriptBlock { param($remoteCommand) iex $remoteCommand } -ArgumentList $remoteCommand
