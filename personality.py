"""
Crypto Personality Analyzer
Analyzes user's crypto personality based on their behavior
"""
from typing import Dict, List, Optional
import random
from enum import Enum


class RiskLevel(str, Enum):
    """Risk tolerance levels"""
    DIAMOND_HANDS = "diamond_hands"  # Never sells, HODL forever
    PAPER_HANDS = "paper_hands"      # Sells at first dip
    BALANCED = "balanced"             # Strategic trader


class PersonalityType(str, Enum):
    """Crypto personality types"""
    BITCOIN_MAXI = "bitcoin_maxi"
    DEFI_DEGEN = "defi_degen"
    NFT_COLLECTOR = "nft_collector"
    MEME_LORD = "meme_lord"
    STABLECOIN_SAFE = "stablecoin_safe"
    ALTCOIN_HUNTER = "altcoin_hunter"
    WHALE = "whale"
    SHITCOIN_SURFER = "shitcoin_surfer"


class PersonalityAnalyzer:
    """Analyzes and generates crypto personalities"""
    
    PERSONALITY_PROFILES = {
        PersonalityType.BITCOIN_MAXI: {
            "title": "Bitcoin Maximalist 🟠",
            "description": "BTC is the only true crypto. Everything else is a shitcoin!",
            "traits": ["Skeptical of altcoins", "Long-term HODLer", "Believes in sound money"],
            "tokens": ["BTC", "LIGHTNING"],
            "risk_level": RiskLevel.DIAMOND_HANDS,
            "emoji": "🟠",
            "tagline": "In Bitcoin we trust, everything else is just noise"
        },
        PersonalityType.DEFI_DEGEN: {
            "title": "DeFi Degenerate 🦄",
            "description": "Lives and breathes yield farming. APY is life!",
            "traits": ["Yield farming addict", "Gas fee complainer", "Protocol hopper"],
            "tokens": ["ETH", "UNI", "AAVE", "COMP", "CRV"],
            "risk_level": RiskLevel.PAPER_HANDS,
            "emoji": "🦄",
            "tagline": "If it's not earning 1000% APY, I'm not interested"
        },
        PersonalityType.NFT_COLLECTOR: {
            "title": "NFT Connoisseur 🎨",
            "description": "Appreciates digital art and exclusive communities",
            "traits": ["Art lover", "Community focused", "Status symbol seeker"],
            "tokens": ["ETH", "PUNK", "BAYC", "MAYC", "AZUKI"],
            "risk_level": RiskLevel.BALANCED,
            "emoji": "🎨",
            "tagline": "My PFP is worth more than your house"
        },
        PersonalityType.MEME_LORD: {
            "title": "Meme Coin King 🐕",
            "description": "Only invests based on Twitter hype and memes",
            "traits": ["Hype chaser", "Shitposter", "FOMO expert"],
            "tokens": ["DOGE", "SHIB", "PEPE", "BONK", "WIF"],
            "risk_level": RiskLevel.PAPER_HANDS,
            "emoji": "🐕",
            "tagline": "Wen moon? Wen Lambo? Wen 100x?"
        },
        PersonalityType.STABLECOIN_SAFE: {
            "title": "Stablecoin Safety Player 💵",
            "description": "Prefers stability over moonshots. Boring but safe!",
            "traits": ["Risk averse", "Stable yield seeker", "Crypto traditionalist"],
            "tokens": ["USDC", "USDT", "DAI"],
            "risk_level": RiskLevel.DIAMOND_HANDS,
            "emoji": "💵",
            "tagline": "3% APY is good enough for me"
        },
        PersonalityType.ALTCOIN_HUNTER: {
            "title": "Altcoin Adventurer 🚀",
            "description": "Searches for the next 100x gem in obscure chains",
            "traits": ["Research enthusiast", "Multi-chain user", "Early adopter"],
            "tokens": ["SOL", "ADA", "DOT", "AVAX", "ATOM"],
            "risk_level": RiskLevel.BALANCED,
            "emoji": "🚀",
            "tagline": "Bitcoin is boring, I want that 1000x!"
        },
        PersonalityType.WHALE: {
            "title": "Crypto Whale 🐋",
            "description": "Moves markets with a single transaction",
            "traits": ["Market mover", "Patient investor", "Big money player"],
            "tokens": ["BTC", "ETH", "BNB"],
            "risk_level": RiskLevel.DIAMOND_HANDS,
            "emoji": "🐋",
            "tagline": "My trades show up on the charts"
        },
        PersonalityType.SHITCOIN_SURFER: {
            "title": "Shitcoin Surfer 🏄",
            "description": "Rides every pump and dump wave. High risk, high reward!",
            "traits": ["Degen trader", "Quick profit seeker", "No research needed"],
            "tokens": ["RANDOM_TOKEN", "PUMP", "DUMP", "RUG", "SCAM"],
            "risk_level": RiskLevel.PAPER_HANDS,
            "emoji": "🏄",
            "tagline": "If it's not a rugpull, is it even crypto?"
        }
    }
    
    @classmethod
    def get_random_personality(cls) -> PersonalityType:
        """Get random personality type"""
        return random.choice(list(PersonalityType))
    
    @classmethod
    def get_personality_profile(cls, personality: PersonalityType) -> Dict:
        """Get full personality profile"""
        return cls.PERSONALITY_PROFILES.get(personality, cls.PERSONALITY_PROFILES[PersonalityType.BITCOIN_MAXI])
    
    @classmethod
    def analyze_user(cls, user_data: Optional[Dict] = None) -> Dict:
        """
        Analyze user and return personality profile
        In production, this would use real Farcaster data
        """
        # For now, generate random personality
        personality = cls.get_random_personality()
        profile = cls.get_personality_profile(personality)
        
        return {
            "personality_type": personality,
            "profile": profile,
            "metadata": {
                "analyzed_at": "2025-10-23",
                "confidence": random.randint(85, 99)
            }
        }
    
    @classmethod
    def get_compatibility_factors(cls, personality1: PersonalityType, personality2: PersonalityType) -> Dict:
        """
        Calculate compatibility factors between two personalities
        """
        profile1 = cls.get_personality_profile(personality1)
        profile2 = cls.get_personality_profile(personality2)
        
        # Calculate token overlap
        tokens1 = set(profile1["tokens"])
        tokens2 = set(profile2["tokens"])
        common_tokens = tokens1 & tokens2
        token_compatibility = (len(common_tokens) / max(len(tokens1), len(tokens2))) * 100
        
        # Risk level compatibility
        risk_match = 100 if profile1["risk_level"] == profile2["risk_level"] else 50
        
        # Personality compatibility matrix
        compatibility_matrix = {
            PersonalityType.BITCOIN_MAXI: {
                PersonalityType.BITCOIN_MAXI: 95,
                PersonalityType.DEFI_DEGEN: 30,
                PersonalityType.NFT_COLLECTOR: 25,
                PersonalityType.MEME_LORD: 10,
                PersonalityType.STABLECOIN_SAFE: 70,
                PersonalityType.ALTCOIN_HUNTER: 20,
                PersonalityType.WHALE: 85,
                PersonalityType.SHITCOIN_SURFER: 5
            },
            PersonalityType.DEFI_DEGEN: {
                PersonalityType.DEFI_DEGEN: 90,
                PersonalityType.NFT_COLLECTOR: 60,
                PersonalityType.ALTCOIN_HUNTER: 75,
                PersonalityType.SHITCOIN_SURFER: 80
            },
            PersonalityType.NFT_COLLECTOR: {
                PersonalityType.NFT_COLLECTOR: 95,
                PersonalityType.WHALE: 70
            },
            PersonalityType.MEME_LORD: {
                PersonalityType.MEME_LORD: 100,
                PersonalityType.SHITCOIN_SURFER: 90,
                PersonalityType.DEFI_DEGEN: 65
            }
        }
        
        # Get base compatibility from matrix
        base_compatibility = 50  # Default
        if personality1 in compatibility_matrix:
            if personality2 in compatibility_matrix[personality1]:
                base_compatibility = compatibility_matrix[personality1][personality2]
        elif personality2 in compatibility_matrix:
            if personality1 in compatibility_matrix[personality2]:
                base_compatibility = compatibility_matrix[personality2][personality1]
        
        return {
            "base_compatibility": base_compatibility,
            "token_compatibility": token_compatibility,
            "risk_compatibility": risk_match,
            "common_tokens": list(common_tokens),
            "personality1_profile": profile1,
            "personality2_profile": profile2
        }
