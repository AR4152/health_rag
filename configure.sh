#!/bin/bash
#
# MIT License
# 
# Copyright (c) 2025 Arjun Raj
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# -----------------------------------------------------------------------------
# Script Name: configure.sh
# Description: 
#   This script performs the necessary installation for the health_rag MLHub package.
#   It checks if Ollama is installed on the system. If not, it prompts the user for 
#   permission to install it. Upon successful installation, it downloads the LLaMA 3.2 1B
#   model using Ollama.
#
# Author: Arjun Raj
# Date: 2025-05-30
# Version: 1.0
# Usage: ml health_rag configure

# different level logger function
log_message() {
    local level="$1"
    local message="$2"
    local color_reset="\e[0m"

    case "$level" in
        INFO)
            local color="\e[32m"   # Green
            ;;
        WARNING)
            local color="\e[33m"   # Yellow
            ;;
        ERROR)
            local color="\e[31m"   # Red
            ;;
        DEBUG)
            local color="\e[34m"   # Blue
            ;;
        SUCCESS)
            local color="\e[36m"   # Cyan
            ;;
        *)
            local color="\e[37m"   # Default (White)
            ;;
    esac

    echo -e "${color}[$level]${color_reset} $message"
}

# function to check if Ollama is already installed
check_ollama_installed() {
    if command -v ollama &>/dev/null; then
        log_message "INFO" "Ollama is already installed on your system."
        return 0
    else
        log_message "INFO" "Ollama is not installed. Proceeding with installation."
        return 1
    fi
}

# validate user input
get_user_response() {
    while true; do
        echo "Do you want to proceed with the installation? [yes/no]: "
        read user_response
        case "$user_response" in
            yes|YES|Yes)
                log_message "INFO" "User confirmed installation."
                return 0
                ;;
            no|NO|No)
                log_message "INFO" "Installation aborted by the user."
                exit 0
                ;;
            *)
                log_message "ERROR" "Invalid input. Please enter 'yes' or 'no'."
                ;;
        esac
    done
}

# function to download the LLaMA model
download_llama_model() {
    log_message "INFO" "Downloading the LLaMA model using Ollama..."
    if ollama pull llama3.2:1b; then
        log_message "SUCCESS" "Successfully downloaded the LLaMA model."
    else
        log_message "ERROR" "Failed to download the LLaMA model."
        exit 1
    fi
}

log_message "INFO" "This script will install the Ollama tool on your system."

# check if Ollama is already installed
if check_ollama_installed; then
    log_message "SUCCESS" "No further action is required."
    exit 0
fi

get_user_response

# proceed with installation if user confirmed
log_message "INFO" "Installing Ollama..."
if curl -fsSL https://ollama.com/install.sh | sh; then
    log_message "SUCCESS" "Ollama has been successfully installed."
else
    log_message "ERROR" "Failed to install Ollama. Please check your internet connection or the installation script."
    exit 1
fi

# download LLaMA model
download_llama_model
