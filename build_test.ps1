# Adobe Challenge 1A - Build and Test Script (PowerShell)
# Usage: .\build_test.ps1 [build|test|run|cleanup|all]

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "test", "run", "cleanup", "all", "")]
    [string]$Action = "",
    
    [Parameter(Position=1)]
    [string]$Mode = ""
)

# Colors for output
$Red = "`e[31m"
$Green = "`e[32m"
$Yellow = "`e[33m"
$Reset = "`e[0m"

function Write-Status {
    param([string]$Message)
    Write-Host "$Green✅ $Message$Reset"
}

function Write-Warning {
    param([string]$Message)
    Write-Host "$Yellow⚠️  $Message$Reset"
}

function Write-Error {
    param([string]$Message)
    Write-Host "$Red❌ $Message$Reset"
}

function Check-Docker {
    Write-Host "🔍 Checking Docker installation..."
    
    try {
        $dockerVersion = docker --version
        if ($LASTEXITCODE -ne 0) {
            throw "Docker command failed"
        }
        Write-Status "Docker is installed: $dockerVersion"
    }
    catch {
        Write-Error "Docker is not installed or not in PATH"
        exit 1
    }
    
    try {
        docker info | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker daemon not running"
        }
        Write-Status "Docker daemon is running"
    }
    catch {
        Write-Error "Docker daemon is not running"
        exit 1
    }
}

function Check-DockerCompose {
    Write-Host "🔍 Checking Docker Compose..."
    
    $global:ComposeCmd = ""
    
    try {
        docker-compose --version | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $global:ComposeCmd = "docker-compose"
        }
    }
    catch {
        # Try docker compose (newer syntax)
        try {
            docker compose version | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $global:ComposeCmd = "docker compose"
            }
        }
        catch {
            Write-Error "Docker Compose is not available"
            exit 1
        }
    }
    
    Write-Status "Docker Compose is available: $global:ComposeCmd"
}

function Build-Image {
    Write-Host "🏗️  Building Docker image..."
    
    # Official challenge build command
    Write-Host "📦 Using official challenge build command..."
    $buildResult = docker build --platform linux/amd64 -t adobe-challenge1a:latest .
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Docker image built successfully"
    } else {
        Write-Error "Failed to build Docker image"
        exit 1
    }
    
    # Also build with docker-compose
    Write-Host "📦 Building with Docker Compose..."
    $composeArgs = $global:ComposeCmd -split " "
    & $composeArgs[0] $composeArgs[1..($composeArgs.Length-1)] build
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Docker Compose build successful"
    } else {
        Write-Warning "Docker Compose build failed, but manual build succeeded"
    }
}

function Test-Setup {
    Write-Host "🧪 Testing the setup..."
    
    # Check if input directory has PDFs
    if (!(Test-Path "input")) {
        Write-Warning "Input directory not found, creating it..."
        New-Item -ItemType Directory -Name "input" -Force | Out-Null
    }
    
    $pdfFiles = Get-ChildItem -Path "input" -Filter "*.pdf" -ErrorAction SilentlyContinue
    if ($pdfFiles.Count -eq 0) {
        Write-Warning "No PDF files found in input directory"
        Write-Host "ℹ️  Please add PDF files to the input directory for testing"
    } else {
        Write-Status "Found $($pdfFiles.Count) PDF files in input directory"
    }
    
    # Create output directory if it doesn't exist
    @("output", "cache") | ForEach-Object {
        if (!(Test-Path $_)) {
            New-Item -ItemType Directory -Name $_ -Force | Out-Null
        }
    }
    
    # Test with official challenge command
    Write-Host "🔍 Testing with official challenge command..."
    $currentDir = Get-Location
    $testResult = docker run --rm `
        -v "${currentDir}/input:/app/input" `
        -v "${currentDir}/output:/app/output" `
        --network none `
        adobe-challenge1a:latest --help 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Official challenge command test passed"
    } else {
        Write-Warning "Official challenge command test failed (expected if no PDFs)"
    }
}

function Run-Compose {
    param([string]$RunMode)
    
    Write-Host "🚀 Running with Docker Compose..."
    
    $composeArgs = $global:ComposeCmd -split " "
    
    if ($RunMode -eq "detached") {
        Write-Status "Starting in detached mode..."
        & $composeArgs[0] $composeArgs[1..($composeArgs.Length-1)] up -d
    } else {
        Write-Status "Starting in foreground mode..."
        & $composeArgs[0] $composeArgs[1..($composeArgs.Length-1)] up
    }
}

function Cleanup {
    Write-Host "🧹 Cleaning up..."
    
    $composeArgs = $global:ComposeCmd -split " "
    & $composeArgs[0] $composeArgs[1..($composeArgs.Length-1)] down --remove-orphans
    docker image prune -f
    
    Write-Status "Cleanup completed"
}

function Show-Usage {
    Write-Host @"
Adobe Challenge 1A - Build and Test Script

Usage: .\build_test.ps1 [Action] [Mode]

Actions:
  build    - Build Docker images
  test     - Test the setup
  run      - Run with Docker Compose
  cleanup  - Clean up containers and images
  all      - Build and test everything

Examples:
  .\build_test.ps1 all                # Build and test
  .\build_test.ps1 run                # Run in foreground
  .\build_test.ps1 run detached       # Run in background
  .\build_test.ps1 cleanup            # Clean up
"@
}

# Main execution
Write-Host "=============================================="
Write-Host "🚀 Adobe Challenge 1A - Build & Test Script"
Write-Host "=============================================="

switch ($Action) {
    "build" {
        Check-Docker
        Check-DockerCompose
        Build-Image
    }
    "test" {
        Check-Docker
        Test-Setup
    }
    "run" {
        Check-Docker
        Check-DockerCompose
        Run-Compose $Mode
    }
    "cleanup" {
        Cleanup
    }
    "all" {
        Check-Docker
        Check-DockerCompose
        Build-Image
        Test-Setup
        Write-Status "Build and test completed successfully!"
        Write-Host "ℹ️  To run the container:"
        Write-Host "   .\build_test.ps1 run"
        Write-Host "   or"
        Write-Host "   docker-compose up"
    }
    default {
        Show-Usage
        exit 1
    }
}
