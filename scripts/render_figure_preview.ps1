param(
  [Parameter(Mandatory = $true)]
  [string]$Macro,

  [Parameter(Mandatory = $true)]
  [string]$Name,

  [string]$PaperWidth = '15cm',
  [string]$PaperHeight = '12cm',
  [double]$Scale = 2.5
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$outDir = Join-Path $repo '_codex_render'
$texPath = Join-Path $outDir "$Name.tex"
$pdfPath = Join-Path $outDir "$Name.pdf"
$pngPath = Join-Path $outDir "$Name.png"

$tectonicCandidates = @(
  (Join-Path $env:USERPROFILE '.cache\codex-tools\tectonic-0.16.9\tectonic.exe'),
  'tectonic.exe'
)

$tectonic = $null
foreach ($candidate in $tectonicCandidates) {
  $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
  if ($cmd) {
    $tectonic = $cmd.Source
    break
  }
}

if (-not $tectonic) {
  throw 'Tectonic was not found. Install it or place tectonic.exe on PATH.'
}

$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
  $python = 'python'
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

@"
\documentclass{article}
\usepackage[paperwidth=$PaperWidth,paperheight=$PaperHeight,margin=4mm]{geometry}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,decorations.markings}
\usepackage{graphicx}
\pagestyle{empty}
\input{../include/MechanismFigures.tex}
\begin{document}
\$Macro
\end{document}
"@ | Set-Content -LiteralPath $texPath -Encoding UTF8

Push-Location $repo
try {
  & $tectonic $texPath --outdir $outDir --keep-logs
  if ($LASTEXITCODE -ne 0) {
    throw "Tectonic failed with exit code $LASTEXITCODE"
  }

  $convertScript = @"
import fitz
pdf_path = r'''$pdfPath'''
png_path = r'''$pngPath'''
scale = float('$Scale')
doc = fitz.open(pdf_path)
pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
pix.save(png_path)
print(png_path)
print(f"{pix.width}x{pix.height}")
"@
  $convertScript | & $python -
  if ($LASTEXITCODE -ne 0) {
    throw "PDF-to-PNG conversion failed with exit code $LASTEXITCODE"
  }
}
finally {
  Pop-Location
}
