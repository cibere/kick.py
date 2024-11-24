import pytest
from kick import Client, Credentials

pytestmark = pytest.mark.asyncio

class TestCategorySearch:
    """Test suite for category search functionality"""

    async def test_search_minecraft_categories(self):
        """Test searching for Minecraft categories returns expected results"""
        # Perform the search
        client = Client()
        await client.login(Credentials(username="TestingKicker", password="TestingKicker123."))

        search_results = await client.search_categories("Minecraft")
        
        # Basic structure checks
        assert search_results.found > 0, "Should find at least one result"
        assert len(search_results.hits) > 0, "Should have at least one hit"
        
        # Get all category names from the results
        category_names = [hit.document.name.lower() for hit in search_results.hits]
        
        # Check for exact "Minecraft" category
        assert "minecraft" in category_names, "Should find the main Minecraft category"
        
        # Check for at least 2 additional Minecraft-related categories
        minecraft_categories = [name for name in category_names if "minecraft" in name]
        assert len(minecraft_categories) >= 3, (
            f"Should find at least 3 Minecraft-related categories. Found: {minecraft_categories}"
        )
        
        # Print found categories for debugging
        print("\nFound Minecraft categories:", minecraft_categories)
        await client.close()
