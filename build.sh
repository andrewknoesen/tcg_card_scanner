#!/bin/bash

# Function to build all services
build_all() {
    echo "Building all services..."
    docker-compose up -d --build
}

# Function to show interactive menu
show_menu() {
    # Get list of services from docker-compose.yml
    services=$(docker compose config --services)

    # Convert services into array
    IFS=$'\n' read -r -d '' -a service_array <<< "$services"

    echo "Available services:"
    echo "0) All services"

    # Display available services
    for i in "${!service_array[@]}"; do
        echo "$((i+1))) ${service_array[i]}"
    done

    # Prompt for service selection
    read -p "Select service to build (0-${#service_array[@]}): " selection

    # Build selected service
    if [ "$selection" -eq 0 ]; then
        build_all
    else
        selected_service=${service_array[$((selection-1))]}
        echo "Building service: $selected_service"
        docker-compose up -d --build "$selected_service"
    fi
}

# Check for command line arguments
if [ $# -eq 0 ]; then
    # No arguments, show interactive menu
    show_menu
else
    # Check for --all argument
    case "$1" in
        --all|-a)
            build_all
            ;;
        --help|-h)
            echo "Usage: $0 [OPTION]"
            echo "Options:"
            echo "  --all, -a    Build all services"
            echo "  --help, -h   Show this help message"
            echo "  (no options) Show interactive menu"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
fi
