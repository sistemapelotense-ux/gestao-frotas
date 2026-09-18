param(
    [string]$DbUrl,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Get-RenderUrl {
    if ($DbUrl) { return $DbUrl }
    $envPath = Join-Path $PSScriptRoot '.env.sync'
    if (Test-Path $envPath) {
        foreach ($l in Get-Content $envPath) {
            if ($l -match '^RENDER_DATABASE_URL=(.+)$') { return $Matches[1] }
        }
    }
    if ($env:RENDER_DATABASE_URL) { return $env:RENDER_DATABASE_URL }
    throw "Informe -DbUrl, configure RENDER_DATABASE_URL ou crie scripts\.env.sync"
}

function Ensure-Ssl {
    param([string]$Url)
    return $Url
}

$url = Ensure-Ssl (Get-RenderUrl)

if (-not $Force) {
    Write-Host "Isto vai SUBSTITUIR todo o conteudo do banco no Render pelos dados do banco local." -ForegroundColor Yellow
    $resp = Read-Host "Confirma? Digite SIM para continuar"
    if ($resp -ne 'SIM') { Write-Host "Cancelado."; exit 0 }
}

docker version --format '{{.Server.Version}}' | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Docker nao esta rodando." }

$tmp = Join-Path $env:TEMP 'gestao_sync'
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$stamp = Get-Date -Format 'yyyyMMddHHmmss'
$dumpName = "local_$stamp.pgc"
$dumpHost = Join-Path $tmp $dumpName
$mount = $tmp -replace '\\', '/'

Write-Host "1/4 Gerando dump do banco local..." -ForegroundColor Cyan
docker exec gestao-db pg_dump -U postgres -d gestao_ativos --no-owner --no-privileges -Fc -f "/tmp/$dumpName" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Falha ao gerar o dump local." }
docker cp "gestao-db:/tmp/$dumpName" $dumpHost | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Falha ao copiar o dump." }

Write-Host "2/4 Recriando schema no Render..." -ForegroundColor Cyan
docker run --rm -e PGSSLMODE=require postgres:16-alpine psql $url -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Falha ao recriar o schema no Render." }

Write-Host "3/4 Restaurando dados no Render..." -ForegroundColor Cyan
docker run --rm -e PGSSLMODE=require -v "${mount}:/backup" postgres:16-alpine pg_restore --no-owner --no-privileges -d $url "/backup/$dumpName" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Falha ao restaurar os dados no Render." }

Write-Host "4/4 Verificando contagens..." -ForegroundColor Green
$q = "SELECT 'usuario' t,count(*) FROM usuario UNION ALL SELECT 'obra',count(*) FROM obra UNION ALL SELECT 'ativo',count(*) FROM ativo UNION ALL SELECT 'lancamento_diario',count(*) FROM lancamento_diario UNION ALL SELECT 'notificacao',count(*) FROM notificacao UNION ALL SELECT 'upload',count(*) FROM upload UNION ALL SELECT 'arquivo_de_propriedade',count(*) FROM arquivo_de_propriedade;"
Write-Host "--- LOCAL ---"
docker exec gestao-db psql -U postgres -d gestao_ativos -c $q
Write-Host "--- RENDER ---"
docker run --rm -e PGSSLMODE=require postgres:16-alpine psql $url -c $q

Remove-Item -Force $dumpHost -ErrorAction SilentlyContinue
Write-Host "Sincronizacao concluida. Observacao: no site publicado o login passa a usar as credenciais do banco local." -ForegroundColor Green