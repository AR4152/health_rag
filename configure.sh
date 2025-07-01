# Script Name: configure.sh
# Description:
#   This script performs the necessary installation for the health_rag MLHub package.
#   It checks if Ollama is installed on the system. If not, it prompts the user for
#   permission to install it. Upon successful installation, it downloads the LLaMA 3.2 1B
#   and nomic-embed-text models using Ollama. Similarly, Tesseract OCR is installed.
#
# Usage: ml configure health_rag


####################
# Helper functions #
####################

# different level logger function
log_message() {
    local level="$1"
    local message="$2"
    local color_reset="\e[0m"

    case "$level" in
        INFO) local color="\e[32m" ;; # Green
        WARNING) local color="\e[33m" ;; # Yellow
        ERROR) local color="\e[31m" ;; # Red
        DEBUG) local color="\e[34m" ;; # Blue
        SUCCESS) local color="\e[36m" ;; # Cyan
        *) local color="\e[37m" ;; # Default (White)
    esac

    echo -e "${color}[$level]${color_reset} $message"
}

# generic function to check if a command exists
is_installed() {
    command -v "$1" &>/dev/null
}

# get user confirmation
prompt_user() {
    local prompt_message="$1"
    while true; do
        echo -n "$prompt_message [yes/no]: "
        read response
        case "$response" in
            yes|YES|Yes)
                return 0
                ;;
            no|NO|No)
                return 1
                ;;
            *)
                log_message "ERROR" "Invalid input. Please enter 'yes' or 'no'."
                ;;
        esac
    done
}

# ollama installation
install_ollama() {
    log_message "INFO" "Installing Ollama..."
    local temp_script="/tmp/ollama_install.sh"
    if curl -fsSL https://ollama.com/install.sh -o "$temp_script"; then
        log_message "INFO" "Downloaded Ollama installation script."
        if bash "$temp_script" 2>&1; then
            log_message "SUCCESS" "Ollama installed successfully."
        else
            log_message "ERROR" "Ollama installation failed."
            exit 1
        fi
    else
        log_message "ERROR" "Failed to download Ollama installation script."
        exit 1
    fi
}

# tesseract installation
install_tesseract() {
    log_message "INFO" "Installing Tesseract OCR..."
    if sudo apt-get update && sudo apt-get install -y tesseract-ocr; then
        log_message "SUCCESS" "Tesseract OCR installed successfully."
    else
        log_message "ERROR" "Failed to install Tesseract OCR."
        log_message "INFO" "Manual install: https://tesseract-ocr.github.io/tessdoc/Installation.html"
        exit 1
    fi
}

# ensure dependency is installed. if not, prompt to install
ensure_dependency() {
    local name="$1"
    local install_function="$2"
    if is_installed "$name"; then
        log_message "SUCCESS" "$name is already installed."
    else
        log_message "INFO" "$name is not installed."
        if prompt_user "Do you want to install $name now?"; then
            "$install_function"
        else
            log_message "WARNING" "$name installation skipped. You may need to install it manually."
        fi
    fi
}

# check if Ollama model is downloaded
model_downloaded() {
    local model_name="$1"
    ollama list | grep -q "$model_name"
}

# download Ollama model if missing
ensure_model() {
    local model_name="$1"
    if model_downloaded "$model_name"; then
        log_message "SUCCESS" "Model '$model_name' is already available."
    else
        log_message "INFO" "Downloading model '$model_name'..."
        if ollama pull "$model_name" 2>&1; then
            log_message "SUCCESS" "Model '$model_name' downloaded."
        else
            log_message "ERROR" "Failed to download model '$model_name'."
            exit 1
        fi
    fi
}

# clean up temp files on exit
cleanup() {
    if [[ -f /tmp/ollama_install.sh ]]; then
        rm -f /tmp/ollama_install.sh
        log_message "DEBUG" "Removed temporary Ollama install script."
    fi
}
trap cleanup EXIT

#################
# Main workflow #
#################

log_message "INFO" "Starting health_rag environment configuration."

# ensure ollama
ensure_dependency "ollama" install_ollama

# download required models
models=(
    "llama3.2:1b"
    "nomic-embed-text"
)
for model in "${models[@]}"; do
    ensure_model "$model"
done

# ensure Tesseract OCR
ensure_dependency "tesseract" install_tesseract

log_message "SUCCESS" "Environment configuration completed successfully."
log_message "INFO" "If you skipped any installation, please install manually as needed."
