import argparse
import json
from pathlib import Path
from data_ingestion.caiso_api import CAISOAPI
import logging

def setup_logging():
    """Configure logging for the setup process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Set up CAISO API access')
    parser.add_argument('--config', default='config/caiso_config.json',
                      help='Path to the configuration file')
    parser.add_argument('--username', help='CAISO OASIS username')
    parser.add_argument('--password', help='CAISO OASIS password')
    parser.add_argument('--api-key', help='CAISO OASIS API key')
    parser.add_argument('--node-id', help='CAISO pricing node ID')
    parser.add_argument('--zone-id', help='CAISO zone ID')
    
    args = parser.parse_args()
    logger = setup_logging()
    
    # Initialize CAISO API client
    api = CAISOAPI(config_path=args.config)
    
    # Step 1: Check if configuration file exists
    config_path = Path(args.config)
    if not config_path.exists():
        logger.info("Creating new configuration file...")
        api._create_default_config()
    
    # Step 2: Update configuration with provided values
    updates = {}
    if args.username:
        updates['username'] = args.username
    if args.password:
        updates['password'] = args.password
    if args.api_key:
        updates['api_key'] = args.api_key
    if args.node_id:
        updates['node_id'] = args.node_id
    if args.zone_id:
        updates['zone_id'] = args.zone_id
    
    if updates:
        logger.info("Updating configuration...")
        if api.update_config(**updates):
            logger.info("Configuration updated successfully")
        else:
            logger.error("Failed to update configuration")
            return
    
    # Step 3: Guide user through registration process if needed
    current_config = api._load_config()
    if not current_config.get('username') or not current_config.get('password'):
        logger.info("\nCAISO OASIS Registration Required:")
        logger.info("1. Visit https://oasis.caiso.com/mrioasis/logon.do")
        logger.info("2. Click on 'Register' to create a new account")
        logger.info("3. Fill out the registration form")
        logger.info("4. Verify your email address")
        logger.info("5. Log in to your account")
        logger.info("6. Run this script again with your credentials")
        return
    
    # Step 4: Guide user through API key request if needed
    if not current_config.get('api_key'):
        logger.info("\nAPI Key Required:")
        logger.info("1. Log in to your CAISO OASIS account")
        logger.info("2. Navigate to the API access section")
        logger.info("3. Request an API key")
        logger.info("4. Run this script again with your API key")
        return
    
    # Step 5: Guide user through node/zone selection if needed
    if not current_config.get('node_id') or not current_config.get('zone_id'):
        logger.info("\nPricing Node/Zone Selection Required:")
        logger.info("1. Log in to your CAISO OASIS account")
        logger.info("2. Navigate to the pricing nodes/zones section")
        logger.info("3. Select your relevant pricing node and zone")
        logger.info("4. Run this script again with your node and zone IDs")
        return
    
    # Step 6: Test the connection
    logger.info("\nTesting API connection...")
    if api.test_connection():
        logger.info("API connection successful!")
        logger.info("\nYour CAISO API access is now configured.")
        logger.info(f"Configuration file: {args.config}")
    else:
        logger.error("API connection failed. Please check your credentials and try again.")

if __name__ == '__main__':
    main() 