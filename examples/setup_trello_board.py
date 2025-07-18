"""
Setup Trello Board

This script sets up your Trello board with the necessary lists and labels for the MCP system.
"""

import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from trello import TrelloClient
from trello.exceptions import ResourceUnavailable

# Load environment variables
load_dotenv()

def setup_trello_board():
    """Set up the Trello board with necessary lists and labels."""
    print("🔧 Setting up Trello Board")
    print("=" * 40)
    
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    if not all([trello_api_key, trello_token, trello_board_id]):
        print("❌ Trello credentials not found!")
        return False
    
    try:
        # Initialize Trello client
        client = TrelloClient(api_key=trello_api_key, token=trello_token)
        
        # Extract board ID if it's a URL
        if trello_board_id.startswith('http'):
            import re
            match = re.search(r'/b/([a-zA-Z0-9]+)', trello_board_id)
            if match:
                trello_board_id = match.group(1)
        
        # Get the board
        board = client.get_board(trello_board_id)
        print(f"✅ Connected to board: {board.name}")
        
        # Define lists to create
        lists_to_create = [
            "To Do",
            "Bugs", 
            "Enhancements",
            "High Priority",
            "Critical",
            "Suggestions",
            "Summary"
        ]
        
        # Create lists
        print("\n📋 Creating lists...")
        created_lists = []
        existing_lists = [lst.name for lst in board.list_lists()]
        
        for list_name in lists_to_create:
            if list_name not in existing_lists:
                try:
                    new_list = board.add_list(list_name)
                    created_lists.append(list_name)
                    print(f"✅ Created list: {list_name}")
                except Exception as e:
                    print(f"❌ Failed to create list '{list_name}': {e}")
            else:
                print(f"ℹ️  List already exists: {list_name}")
        
        # Define labels to create
        labels_to_create = [
            ("security", "red"),
            ("bug", "red"),
            ("enhancement", "blue"),
            ("documentation", "green"),
            ("testing", "yellow"),
            ("performance", "orange"),
            ("code-quality", "purple"),
            ("suggestion", "sky"),
            ("summary", "lime"),
            ("mcp", "black")
        ]
        
        # Create labels
        print("\n🏷️  Creating labels...")
        created_labels = []
        existing_labels = [label.name for label in board.get_labels()]
        
        for label_name, color in labels_to_create:
            if label_name not in existing_labels:
                try:
                    new_label = board.add_label(label_name, color)
                    created_labels.append(label_name)
                    print(f"✅ Created label: {label_name} ({color})")
                except Exception as e:
                    print(f"❌ Failed to create label '{label_name}': {e}")
            else:
                print(f"ℹ️  Label already exists: {label_name}")
        
        # Create a test card
        print("\n📝 Creating test card...")
        try:
            # Get the first list (or create one if none exist)
            lists = board.list_lists()
            if lists:
                test_list = lists[0]
                test_card = test_list.add_card(
                    name="🎉 Trello Board Setup Complete!",
                    desc="Your Trello board has been set up for the MCP GitHub Repository Analyzer.\n\nThis card was created automatically during setup."
                )
                
                # Add some labels
                labels = board.get_labels()
                if labels:
                    test_card.add_labels([labels[0].id])
                
                print(f"✅ Test card created: {test_card.url}")
            else:
                print("⚠️  No lists available to create test card")
        except Exception as e:
            print(f"❌ Failed to create test card: {e}")
        
        # Summary
        print("\n📊 Setup Summary")
        print("=" * 20)
        print(f"Board: {board.name}")
        print(f"Lists created: {len(created_lists)}")
        print(f"Labels created: {len(created_labels)}")
        print(f"Board URL: {board.url}")
        
        if created_lists:
            print(f"\n✅ New lists: {', '.join(created_lists)}")
        if created_labels:
            print(f"✅ New labels: {', '.join(created_labels)}")
        
        print("\n✨ Trello board setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Trello board: {e}")
        return False

if __name__ == "__main__":
    setup_trello_board() 