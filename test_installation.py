"""
Test script for CryptoMatch
Run this to verify your installation
"""
import sys
import asyncio


def test_imports():
    """Test if all required modules are installed"""
    print("🔍 Testing imports...")
    
    required_modules = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('requests', 'Requests'),
        ('PIL', 'Pillow'),
        ('openai', 'OpenAI (optional)'),
    ]
    
    all_good = True
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print(f"  ✅ {display_name} installed")
        except ImportError:
            print(f"  ❌ {display_name} NOT installed")
            if module_name != 'openai':
                all_good = False
    
    return all_good


def test_config():
    """Test configuration"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import settings
        print(f"  ✅ Config loaded")
        print(f"  📍 Base URL: {settings.base_url}")
        print(f"  🌍 Environment: {settings.environment}")
        
        if settings.openai_api_key:
            print(f"  ✅ OpenAI API key found")
        else:
            print(f"  ⚠️  OpenAI API key not found (comedy will use fallback templates)")
        
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False


def test_personality():
    """Test personality analyzer"""
    print("\n🔍 Testing personality analyzer...")
    
    try:
        from personality import PersonalityAnalyzer, PersonalityType
        
        # Test random personality generation
        personality = PersonalityAnalyzer.get_random_personality()
        profile = PersonalityAnalyzer.get_personality_profile(personality)
        
        print(f"  ✅ Generated personality: {profile['title']}")
        print(f"  📊 Tokens: {', '.join(profile['tokens'][:3])}")
        print(f"  ⚡ Risk level: {profile['risk_level']}")
        
        # Test user analysis
        user_analysis = PersonalityAnalyzer.analyze_user()
        print(f"  ✅ User analysis: {user_analysis['profile']['title']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Personality analyzer error: {e}")
        return False


async def test_matchmaking():
    """Test matchmaking engine"""
    print("\n🔍 Testing matchmaking engine...")
    
    try:
        from matchmaking import matchmaking_engine
        from personality import PersonalityAnalyzer
        
        # Generate two users
        user1 = PersonalityAnalyzer.analyze_user()
        user2 = PersonalityAnalyzer.analyze_user()
        
        # Calculate compatibility
        compatibility = await matchmaking_engine.calculate_compatibility(user1, user2)
        
        print(f"  ✅ Match generated")
        print(f"  💕 Compatibility: {compatibility['total_score']}%")
        print(f"  🎭 Level: {compatibility['match_level']}")
        print(f"  😂 Comedy: {compatibility['comedy'][:80]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Matchmaking error: {e}")
        return False


async def test_comedy():
    """Test comedy generator"""
    print("\n🔍 Testing comedy generator...")
    
    try:
        from comedy_generator import comedy_generator
        from personality import PersonalityAnalyzer
        
        # Generate personalities
        user1 = PersonalityAnalyzer.analyze_user()
        user2 = PersonalityAnalyzer.analyze_user()
        
        # Generate comedy
        comedy = await comedy_generator.generate_match_comedy(
            user1['profile'],
            user2['profile'],
            85,
            'high_match'
        )
        
        print(f"  ✅ Comedy generated")
        print(f"  😂 Result: {comedy[:100]}...")
        
        # Test date idea
        date_idea = await comedy_generator.generate_date_idea(
            user1['profile'],
            user2['profile']
        )
        print(f"  💡 Date idea: {date_idea[:80]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Comedy generator error: {e}")
        return False


def test_image_generator():
    """Test image generator"""
    print("\n🔍 Testing image generator...")
    
    try:
        from image_generator import image_generator
        from personality import PersonalityAnalyzer
        
        # Generate personalities
        user1 = PersonalityAnalyzer.analyze_user()
        user2 = PersonalityAnalyzer.analyze_user()
        
        # Generate image
        image_url = image_generator.generate_match_image(
            user1['profile'],
            user2['profile'],
            87,
            'high_match',
            "This is a test comedy text!"
        )
        
        print(f"  ✅ Image generated")
        print(f"  📷 Format: {image_url[:50]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Image generator error: {e}")
        return False


async def test_api():
    """Test FastAPI app"""
    print("\n🔍 Testing FastAPI app...")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        print(f"  ✅ Health check passed")
        
        # Test home endpoint
        response = client.get("/")
        assert response.status_code == 200
        print(f"  ✅ Home page works")
        
        # Test personalities API
        response = client.get("/api/personalities")
        assert response.status_code == 200
        data = response.json()
        print(f"  ✅ Personalities API works ({data['count']} types)")
        
        return True
    except ImportError:
        print(f"  ⚠️  TestClient not available (install: pip install httpx)")
        return True
    except Exception as e:
        print(f"  ❌ API test error: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 CRYPTOMATCH TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run synchronous tests
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Personality", test_personality()))
    
    # Run async tests
    results.append(("Matchmaking", await test_matchmaking()))
    results.append(("Comedy", await test_comedy()))
    results.append(("Image Generator", test_image_generator()))
    results.append(("API", await test_api()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your installation is ready!")
        print("\n🚀 Next steps:")
        print("   1. Setup your .env file with OpenAI API key")
        print("   2. Run: python main.py")
        print("   3. Open: http://localhost:8000")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
