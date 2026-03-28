$ErrorActionPreference = 'SilentlyContinue'

$uvPath = "$HOME/.cargo/bin"
if ($env:PATH -notlike "*$uvPath*") {
    $env:PATH += if ($IsWindows) { ";$uvPath" } else { ":$uvPath" }
}

$installLogic = {
    $v = "3.14.0"
    
    if ((python --version 2>&1) -match "3.14") { 
        if (!(Get-Command uv -ErrorAction SilentlyContinue)) { goto :install_uv }
        exit 
    }

    $arch = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64" -or $(uname -m 2>$null) -eq "aarch64") { "arm64" } else { "amd64" }

    if ($IsWindows) {
        $url = "https://www.python.org/ftp/python/$v/python-$v-$arch.exe"
        $out = "$env:TEMP\py.exe"
        (New-Object System.Net.WebClient).DownloadFile($url, $out)
        
        $admin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
        $flags = if ($admin) { "/quiet InstallAllUsers=1 PrependPath=1" } else { "/quiet InstallAllUsers=0 PrependPath=1" }
        
        Start-Process -FilePath $out -ArgumentList $flags -Wait
        Remove-Item $out -Force
    }

    :install_uv
    if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
        if ($IsWindows) {
            powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex" >$null 2>&1
        } else {
            curl -LsSf https://astral.sh/uv/install.sh | sh >$null 2>&1
        }
        $env:PATH += if ($IsWindows) { ";$uvPath" } else { ":$uvPath" }
    }

    uv python install 3.14 >$null 2>&1
    uv pip install --quiet uv >$null 2>&1
}

if ($IsWindows) {
    Start-Process powershell.exe -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -Command & {$installLogic}"
} else {
    powershell -Command "& {$installLogic}" >/dev/null 2>&1 &
}