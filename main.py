"""
CryptoMatch - AI-Powered Crypto Dating for Farcaster
Production-ready Farcaster Frame v2 implementation
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from typing import Dict, Optional
import random

from config import settings
from personality import PersonalityAnalyzer
from matchmaking import matchmaking_engine
from comedy_generator import comedy_generator

# Initialize FastAPI app
app = FastAPI(
    title="CryptoMatch",
    description="AI-Powered Crypto Dating for Farcaster",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory cache for demo (use Redis in production)
user_cache = {}


def generate_frame_html(
    image_url: str,
    buttons: list,
    post_url: str,
    title: str = "CryptoMatch",
    description: str = "Find your perfect crypto soulmate!"
) -> str:
    """Generate Farcaster Frame v2 compliant HTML"""
    
    button_tags = ""
    for idx, button in enumerate(buttons, 1):
        button_tags += f'<meta property="fc:frame:button:{idx}" content="{button["label"]}" />\n'
        if "action" in button:
            button_tags += f'<meta property="fc:frame:button:{idx}:action" content="{button["action"]}" />\n'
        if "target" in button:
            button_tags += f'<meta property="fc:frame:button:{idx}:target" content="{button["target"]}" />\n'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- OpenGraph Meta Tags -->
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:image" content="{image_url}" />
    
    <!-- Farcaster Frame v2 Meta Tags -->
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{image_url}" />
    <meta property="fc:frame:image:aspect_ratio" content="1.91:1" />
    <meta property="fc:frame:post_url" content="{post_url}" />
    {button_tags}
    
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            max-width: 600px;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            font-size: 48px;
            margin: 0 0 20px 0;
            font-weight: 800;
        }}
        p {{
            font-size: 20px;
            opacity: 0.9;
            line-height: 1.6;
        }}
        .emoji {{
            font-size: 64px;
            margin: 20px 0;
        }}
        .info {{
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 12px;
            margin-top: 30px;
        }}
        a {{
            color: #FFD93D;
            text-decoration: none;
            font-weight: 600;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">💕</div>
        <h1>CryptoMatch</h1>
        <p>{description}</p>
        <div class="info">
            <p><strong>How it works:</strong></p>
            <p>1️⃣ Click "Find My Match"<br>
            2️⃣ AI analyzes your crypto personality<br>
            3️⃣ Get matched with compatible users<br>
            4️⃣ Share your results!</p>
        </div>
    </div>
</body>
</html>"""
    
    return html


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the Mini App HTML"""
    with open("static/app.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.post("/match")
async def find_match(request: Request):
    """Process match request and return result frame"""
    
    try:
        # Parse Farcaster Frame POST data
        body = await request.json()
        
        # Extract user FID (Farcaster ID)
        untrusted_data = body.get("untrustedData", {})
        user_fid = untrusted_data.get("fid", f"user_{random.randint(1000, 9999)}")
        button_index = untrusted_data.get("buttonIndex", 1)
        
        # Handle "About" button
        if button_index == 2:
            return await show_about(request)
        
        # Check if user already has a recent match (cache)
        cache_key = f"match_{user_fid}"
        
        # Generate new match
        match_result = await matchmaking_engine.generate_match_result(
            user_fid=str(user_fid),
            match_fid=f"match_{random.randint(1000, 9999)}",
            user_name="You",
            match_name=f"User #{random.randint(100, 999)}"
        )
        
        # Cache result
        user_cache[cache_key] = match_result
        
        # Get compatibility data
        compatibility = match_result["compatibility"]
        
        # Use generated image
        result_image = compatibility["image_url"]
        
        # Create result frame buttons
        buttons = [
            {
                "label": "🔄 Find Another Match",
                "action": "post"
            },
            {
                "label": "🚀 Share Result",
                "action": "link",
                "target": f"https://warpcast.com/~/compose?text={match_result['share_text']}&embeds[]={settings.base_url}"
            },
            {
                "label": "📊 View Details",
                "action": "post"
            }
        ]
        
        description = f"💕 {compatibility['total_score']}% Match! {compatibility['comedy']}"
        
        html = generate_frame_html(
            image_url=result_image,
            buttons=buttons,
            post_url=f"{settings.base_url}/match",
            title=f"CryptoMatch Result: {compatibility['total_score']}% Compatible! 🎯",
            description=description
        )
        
        return HTMLResponse(content=html)
        
    except Exception as e:
        print(f"Error in find_match: {e}")
        return await error_frame(str(e))


@app.post("/details")
async def show_details(request: Request):
    """Show detailed match breakdown"""
    
    try:
        body = await request.json()
        untrusted_data = body.get("untrustedData", {})
        user_fid = untrusted_data.get("fid", "unknown")
        
        cache_key = f"match_{user_fid}"
        match_result = user_cache.get(cache_key)
        
        if not match_result:
            return await error_frame("No match found. Please try again!")
        
        compatibility = match_result["compatibility"]
        
        # Create detailed breakdown image (simplified for demo)
        detail_image = "https://images.unsplash.com/photo-1621504450181-5d356f61d307?w=1200&h=630&fit=crop"
        
        buttons = [
            {
                "label": "🔙 Back to Match",
                "action": "post"
            },
            {
                "label": "🔄 New Match",
                "action": "post"
            }
        ]
        
        description = f"""
        📊 Compatibility Breakdown:
        • Personality: {int(compatibility['breakdown']['personality_base'])}%
        • Tokens: {int(compatibility['breakdown']['token_overlap'])}%
        • Risk: {int(compatibility['breakdown']['risk_tolerance'])}%
        💡 {compatibility['date_idea']}
        """
        
        html = generate_frame_html(
            image_url=detail_image,
            buttons=buttons,
            post_url=f"{settings.base_url}/match",
            title="Match Details",
            description=description
        )
        
        return HTMLResponse(content=html)
        
    except Exception as e:
        return await error_frame(str(e))


async def show_about(request: Request):
    """Show about information"""
    
    about_image = "https://images.unsplash.com/photo-1605792657660-596af9009e82?w=1200&h=630&fit=crop"
    
    buttons = [
        {
            "label": "🔥 Try CryptoMatch",
            "action": "post"
        },
        {
            "label": "🌐 Learn More",
            "action": "link",
            "target": settings.base_url
        }
    ]
    
    description = """
    CryptoMatch uses AI to analyze your crypto personality and find compatible matches!
    
    🎯 Features:
    • AI personality analysis
    • Smart compatibility scoring
    • Funny, personalized results
    • Viral sharing tools
    
    Built with ❤️ for the Farcaster community!
    """
    
    html = generate_frame_html(
        image_url=about_image,
        buttons=buttons,
        post_url=f"{settings.base_url}/match",
        title="About CryptoMatch",
        description=description
    )
    
    return HTMLResponse(content=html)


async def error_frame(error_message: str = "Something went wrong!"):
    """Generate error frame"""
    
    error_image = "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=1200&h=630&fit=crop"
    
    buttons = [
        {
            "label": "🔄 Try Again",
            "action": "post"
        }
    ]
    
    html = generate_frame_html(
        image_url=error_image,
        buttons=buttons,
        post_url=f"{settings.base_url}/match",
        title="Oops! Error",
        description=f"😅 {error_message} Please try again!"
    )
    
    return HTMLResponse(content=html)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "CryptoMatch",
        "version": "2.0.0",
        "environment": settings.environment
    })


@app.get("/api/personalities")
async def list_personalities():
    """API endpoint to list all personality types"""
    personalities = []
    
    for personality_type in PersonalityAnalyzer.PERSONALITY_PROFILES:
        profile = PersonalityAnalyzer.get_personality_profile(personality_type)
        personalities.append({
            "type": personality_type,
            "profile": profile
        })
    
    return JSONResponse(content={
        "count": len(personalities),
        "personalities": personalities
    })


@app.get("/robots.txt")
async def robots():
    """Robots.txt for SEO"""
    content = """User-agent: *
Allow: /
Sitemap: {}/sitemap.xml
""".format(settings.base_url)
    return Response(content=content, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False,
        log_level="info"
    )
