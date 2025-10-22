"""
AI-Powered Comedy Generator for Crypto Dating
Uses OpenAI GPT to generate funny, personalized match descriptions
"""
from typing import Dict, Optional
import random
from openai import AsyncOpenAI
from config import settings


class ComedyGenerator:
    """Generates funny, personalized match descriptions"""
    
    def __init__(self):
        try:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        except Exception:
            self.client = None
        self.fallback_templates = self._load_fallback_templates()
    
    def _load_fallback_templates(self) -> Dict:
        """Fallback comedy templates when OpenAI is not available"""
        return {
            "high_match": [
                "🔥 THIS IS IT! You two are like Bitcoin and blockchain - literally made for each other! Your portfolios are so aligned, even Satoshi would approve! 💕",
                "🚀 MOON MISSION CONFIRMED! You're both diamond hands HODLers who understand the sacred art of 'buying the dip'. True love = never selling! 💎",
                "⚡ ELECTRIC CONNECTION! You both know that gas fees are a love language. When ETH drops below $2000, you don't panic - you buy more together! 🔥",
                "💖 SOULMATE ALERT! While paper hands are panic selling, you two are busy planning your joint crypto empire. Warren Buffett is SHAKING! 🎯",
                "✨ COSMIC MATCH! You both understand the difference between 'wen moon?' and 'WAGMI'. This isn't just a match, it's a MOVEMENT! 🌙"
            ],
            "medium_match": [
                "👍 SOLID VIBES! You're like two different layer-2 solutions - different approaches, same goal! With a little compromise, you'll scale together! 📈",
                "💫 INTERESTING POTENTIAL! One of you HODLs BTC, the other is a DeFi degen... it's like opposites attract, but make it blockchain! 🎲",
                "🤝 GOOD CHEMISTRY! You both appreciate a quality project when you see one. Sure, your risk tolerances are different, but that's what stop-losses are for! 💚",
                "🎯 PROMISING MATCH! Your portfolios show complementary strengths. One plays it safe with blue chips, the other hunts for 100x gems. Teamwork! 🔍",
                "📊 COMPATIBLE ENERGY! While you don't agree on everything (BTC vs ETH debate incoming), you both know NEVER to talk about crypto at parties! 🎭"
            ],
            "low_match": [
                "⚡ CHAOS ENERGY! One of you is a Bitcoin maxi with trust issues, the other is yeeting life savings into dog coins. This could be... educational! 🎪",
                "🎭 EXTREME OPPOSITES! It's like matching a Coinbase user with a Binance degen. You'll either balance each other or argue about CEX vs DEX! 🔄",
                "🌗 YIN AND YANG! One researches whitepapers for months, the other buys based on Twitter hype. It's not a red flag, it's a LEARNING OPPORTUNITY! 📚",
                "🎪 CRYPTO CIRCUS! Your investment strategies are so different, they should teach a course about it. 'How to Disagree Without Selling Each Other's Bags 101' 🤡",
                "🔄 COMPLEMENTARY CHAOS! One is 'DYOR and HODL', the other is 'YOLO and pray'. Together, you might just... confuse each other completely! 😅"
            ]
        }
    
    async def generate_match_comedy(
        self,
        personality1: Dict,
        personality2: Dict,
        compatibility_score: int,
        match_level: str
    ) -> str:
        """
        Generate personalized funny match description
        Uses OpenAI if available, falls back to templates
        """
        # Try OpenAI first
        if self.client:
            try:
                return await self._generate_with_ai(personality1, personality2, compatibility_score, match_level)
            except Exception as e:
                print(f"OpenAI error: {e}, falling back to templates")
        
        # Fallback to templates
        return self._generate_from_template(match_level)
    
    async def _generate_with_ai(
        self,
        personality1: Dict,
        personality2: Dict,
        score: int,
        level: str
    ) -> str:
        """Generate comedy using OpenAI"""
        
        prompt = f"""You are a hilarious crypto dating expert. Generate a funny, 1-2 sentence match description for two crypto users.

Personality 1: {personality1['title']} - {personality1['description']}
Traits: {', '.join(personality1['traits'])}
Tokens: {', '.join(personality1['tokens'])}

Personality 2: {personality2['title']} - {personality2['description']}
Traits: {', '.join(personality2['traits'])}
Tokens: {', '.join(personality2['tokens'])}

Compatibility Score: {score}%
Match Level: {level}

Requirements:
- Use crypto slang (HODL, wen moon, diamond hands, paper hands, NGMI, WAGMI, degen, etc.)
- Be funny and slightly sarcastic
- Reference their specific traits and tokens
- Keep it under 200 characters
- Use emojis strategically (max 3)
- Make it shareable and viral-worthy

Generate ONE funny match description:"""

        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a witty crypto dating expert who makes people laugh."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_from_template(self, match_level: str) -> str:
        """Generate from fallback templates"""
        templates = self.fallback_templates.get(match_level, self.fallback_templates["medium_match"])
        return random.choice(templates)
    
    async def generate_date_idea(self, personality1: Dict, personality2: Dict) -> str:
        """Generate funny date idea"""
        
        date_ideas = [
            "💡 First Date Idea: Watch crypto charts together during a market dump and see who panics first! 📉",
            "🎯 Perfect Date: Calculate impermanent loss together while staking in a sketchy DeFi pool! 💧",
            "🌙 Romantic Evening: Compare NFT collections and passive-aggressively debate about utility vs art! 🎨",
            "⚡ Dream Date: Attend an NFT conference, complain about gas fees, and bond over shared FOMO! 🏛️",
            "💫 Ideal Night: Create a joint investment portfolio and argue about risk management! (Couple goals!) 📊",
            "🚀 Adventure Time: Go to a crypto meetup and pretend you're early to the next 100x project! 🎪",
            "💰 Fun Activity: Paper trade against each other and see whose strategy gets rekt first! 📈",
            "🎭 Cute Date: Visit a Bitcoin ATM together and discuss the meaning of decentralization! 🏦"
        ]
        
        # If both are same personality type
        if personality1['title'] == personality2['title']:
            date_ideas.extend([
                f"🔥 Since you're both {personality1['title']}s - have a competition to see who can HODL longer without checking prices! 💎",
                f"✨ Perfect match activity: Build a joint {personality1['tokens'][0]} position and never speak of selling! 🚫"
            ])
        
        return random.choice(date_ideas)
    
    async def generate_viral_share_text(
        self,
        user1_name: str,
        user2_name: str,
        score: int,
        comedy: str
    ) -> str:
        """Generate viral-worthy share text"""
        
        share_templates = [
            f"🎯 Just found my crypto soulmate! {user2_name} and I have {score}% compatibility! {comedy} Try it: ",
            f"💕 {score}% match with {user2_name}! {comedy} Find YOUR crypto match: ",
            f"🚀 BREAKING: {user2_name} and I are {score}% compatible in the crypto dating universe! {comedy} Your turn: ",
            f"⚡ Matched with {user2_name} at {score}%! {comedy} Who's YOUR perfect crypto match? ",
        ]
        
        return random.choice(share_templates)


# Singleton instance
comedy_generator = ComedyGenerator()
