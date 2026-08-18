# Claude AI Factory — bootstrap para Windows (PowerShell)
# Instala las skills, el subagente y las plantillas de este repo en ~/.claude
# Idempotente: ejecútalo tras cada `git pull` para sincronizar.
$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"

Write-Host "🏭 Claude AI Factory — bootstrap"
Write-Host "   Repo:    $RepoDir"
Write-Host "   Destino: $ClaudeDir"

New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir "skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir "agents") | Out-Null

# Skills y agentes: se copian siempre (el repo es la fuente de verdad)
Get-ChildItem -Directory (Join-Path $RepoDir ".claude\skills") | ForEach-Object {
    $dest = Join-Path $ClaudeDir "skills\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Force (Join-Path $_.FullName "SKILL.md") $dest
    Write-Host "   ✓ skill: /$($_.Name)"
}

Get-ChildItem (Join-Path $RepoDir ".claude\agents\*.md") | ForEach-Object {
    Copy-Item -Force $_.FullName (Join-Path $ClaudeDir "agents")
    Write-Host "   ✓ agente: $($_.BaseName)"
}

# Plantillas: solo si no existen (no pisamos tu configuración personal)
$claudeMd = Join-Path $ClaudeDir "CLAUDE.md"
if (-not (Test-Path $claudeMd)) {
    Copy-Item (Join-Path $RepoDir "setup\CLAUDE.md.plantilla") $claudeMd
    Write-Host "   ✓ creado ~/.claude/CLAUDE.md desde plantilla — personalízalo"
} else {
    Write-Host "   · ~/.claude/CLAUDE.md ya existe — no se toca"
}

$settings = Join-Path $ClaudeDir "settings.json"
if (-not (Test-Path $settings)) {
    Copy-Item (Join-Path $RepoDir "setup\settings.json.plantilla") $settings
    Write-Host "   ✓ creado ~/.claude/settings.json desde plantilla"
} else {
    Write-Host "   · ~/.claude/settings.json ya existe — no se toca"
}

Write-Host "✅ Listo. Abre 'claude' en cualquier carpeta: las skills ya están disponibles."
