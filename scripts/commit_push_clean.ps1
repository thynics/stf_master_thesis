param(
  [Parameter(Mandatory = $true)]
  [string]$Message
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$previewDir = Join-Path $repo '_codex_render'

if (Test-Path -LiteralPath $previewDir) {
  $resolvedPreview = (Resolve-Path -LiteralPath $previewDir).Path
  if (-not ($resolvedPreview.StartsWith($repo + [System.IO.Path]::DirectorySeparatorChar))) {
    throw "Refusing to remove outside repo: $resolvedPreview"
  }
  Remove-Item -LiteralPath $resolvedPreview -Recurse -Force
}

Push-Location $repo
try {
  git diff --check
  git add -A
  git commit -m $Message
  git pull --rebase
  git push
  git status --short
}
finally {
  Pop-Location
}
